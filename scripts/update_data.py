# scripts/update_data.py

import sys
import os
import json
import yfinance as yf
import time
import random
import requests

# ⭐ 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MACRO_LIST, WATCHLIST, DEFAULT_STRATEGY, SOURCE_MAP
from theme_mapping import THEME_MAPPING  # ⭐ 从 theme_mapping.py 导入

# ============================================================
# ⭐ 从 THEME_MAPPING 自动构建二级→三级映射
# ============================================================

def build_level2_to_level3(theme_mapping):
    """
    从 THEME_MAPPING 自动构建二级标签 → 三级标签列表的映射
    """
    level2_to_level3 = {}
    
    if not theme_mapping:
        return level2_to_level3
    
    for level1_key, level1_value in theme_mapping.items():
        if isinstance(level1_value, dict):
            for level2_key, level2_value in level1_value.items():
                if isinstance(level2_value, list):
                    level2_to_level3[level2_key] = level2_value
    
    return level2_to_level3


# ⭐ 自动生成展开映射
LEVEL2_TO_LEVEL3 = build_level2_to_level3(THEME_MAPPING)

# ============================================================
# ⭐ Tag 合并函数
# ============================================================
def merge_tags(tags):
    """
    将二级标签展开为三级标签列表
    例如: ["第三代半导体"] → ["SiC", "碳化硅", "GaN", ...]
    """
    if not tags:
        return []
    
    result = []
    for tag in tags:
        # 检查是否需要展开为三级标签
        if tag in LEVEL2_TO_LEVEL3:
            for expanded_tag in LEVEL2_TO_LEVEL3[tag]:
                if expanded_tag not in result:
                    result.append(expanded_tag)
        else:
            # 不需要展开，直接保留
            if tag not in result:
                result.append(tag)
    
    return result

def build_tag_theme_mapping(theme_mapping):
    """
    根据 THEME_MAPPING 构建 tag → theme_path 的映射字典
    
    匹配优先级：
    1. 优先匹配第三层（叶子节点）→ 返回 [一级, 二级, 三级]
    2. 匹配不到第三层时，匹配第二层 → 返回 [一级, 二级]
    3. 匹配不到第二层时，匹配第一层 → 返回 [一级]
    
    返回格式:
    {
        "SiC": ["2. 半导体材料", "第三代半导体", "SiC"],        # 第三层匹配
        "GPU": ["3. 算力芯片", "GPU"],                         # 第二层匹配
        "第三代半导体": ["2. 半导体材料", "第三代半导体"],       # 第二层匹配（二级名称本身）
        "半导体设备": ["1. 半导体设备"],                        # 第一层匹配
    }
    """
    tag_map = {}
    
    if not theme_mapping:
        return tag_map
    
    # 第一遍：匹配第三层（叶子节点）
    for theme_name, theme_value in theme_mapping.items():
        if isinstance(theme_value, dict):
            for sub_theme_name, sub_theme_value in theme_value.items():
                if isinstance(sub_theme_value, list):
                    for tag in sub_theme_value:
                        if tag not in tag_map:
                            tag_map[tag] = [theme_name, sub_theme_name, tag]
                elif isinstance(sub_theme_value, dict):
                    for tag, path in build_tag_theme_mapping({sub_theme_name: sub_theme_value}).items():
                        if tag not in tag_map:
                            tag_map[tag] = path
    
    # 第二遍：匹配第二层（不覆盖第三层）
    for theme_name, theme_value in theme_mapping.items():
        if isinstance(theme_value, list):
            for tag in theme_value:
                if tag not in tag_map:
                    tag_map[tag] = [theme_name, tag]
        elif isinstance(theme_value, dict):
            for sub_theme_name, sub_theme_value in theme_value.items():
                # ⭐ 二级名称本身作为一个可匹配的 tag
                if sub_theme_name not in tag_map:
                    # 返回 [一级, 二级]（不包含三级）
                    tag_map[sub_theme_name] = [theme_name, sub_theme_name]
                # 如果三级列表中有与二级名称相同的 tag，保持第三层匹配优先
    
    # 第三遍：匹配第一层（最低优先级）
    for theme_name, theme_value in theme_mapping.items():
        if theme_name not in tag_map:
            tag_map[theme_name] = [theme_name]
    
    return tag_map


# 全局构建 tag → theme_path 映射（在模块加载时执行一次）
TAG_THEME_MAP = build_tag_theme_mapping(THEME_MAPPING)


def get_theme_paths_for_tags(tags, tag_theme_map):
    """
    根据 tags 列表，返回每个 tag 对应的 theme_path
    
    返回格式:
    [
        {"tag": "光刻机", "theme_path": ["1. 半导体设备", "光刻机"]},
        {"tag": "GPU", "theme_path": []},
    ]
    """
    result = []
    if not tags:
        return result
    
    for tag in tags:
        theme_path = tag_theme_map.get(tag, [])
        result.append({
            "tag": tag,
            "theme_path": theme_path
        })
    
    return result


class StockDataManager:
    def __init__(self, cache_file='data/stock_cache.json'):
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f: 
                    return json.load(f)
            except: 
                return {}
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def safe_float(self, value, default=0.0):
        """安全转换为浮点数"""
        if value is None or value == '-' or value == '--' or value == '' or value == 'NaN':
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def get_a_stock_data_sina(self, symbol):
        """使用新浪财经 API 获取 A 股数据"""
        try:
            clean_code = symbol.split('.')[0]
            print(f"🔄 [新浪API] 正在获取 {clean_code} 数据...")
            
            # 判断市场
            market = 'sh' if symbol.endswith(('.SH', '.SS')) else 'sz'
            url = f"https://hq.sinajs.cn/list={market}{clean_code}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://finance.sina.com.cn'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'gbk'
            
            if response.status_code != 200:
                print(f"⚠️ 新浪API请求失败: {response.status_code}")
                return None, "none"
            
            data_str = response.text
            if not data_str or 'var hq_str_' not in data_str:
                print(f"⚠️ 新浪API返回空数据")
                return None, "none"
            
            parts = data_str.split('"')[1].split(',')
            if len(parts) < 10:
                print(f"⚠️ 新浪API数据格式错误")
                return None, "none"
            
            name = parts[0]
            current_price = self.safe_float(parts[3])
            prev_close = self.safe_float(parts[2])
            
            data = {
                'regularMarketPrice': current_price,
                'trailingPE': 0,  # 新浪不提供 PE
                'priceToBook': 0,  # 新浪不提供 PB
                'name': name,
                'changePercent': ((current_price - prev_close) / prev_close * 100) if prev_close else 0,
                'volume': self.safe_float(parts[8]) if len(parts) > 8 else 0,
                'high': self.safe_float(parts[4]) if len(parts) > 4 else 0,
                'low': self.safe_float(parts[5]) if len(parts) > 5 else 0,
                'open': self.safe_float(parts[1]) if len(parts) > 1 else 0,
                'prev_close': prev_close,
            }
            
            print(f"✅ [新浪API] 成功获取 {clean_code}")
            return data, "sina"
            
        except Exception as e:
            print(f"❌ [新浪API] 抓取 {symbol} 异常: {e}")
            return None, "none"

    def get_a_stock_data_tencent(self, symbol):
        """使用腾讯财经 API 获取 A 股数据"""
        try:
            clean_code = symbol.split('.')[0]
            print(f"🔄 [腾讯API] 正在获取 {clean_code} 数据...")
            
            url = f"https://qt.gtimg.cn/q={clean_code}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://finance.qq.com'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'gbk'
            
            if response.status_code != 200:
                print(f"⚠️ 腾讯API请求失败: {response.status_code}")
                return None, "none"
            
            data_str = response.text
            if not data_str or '~' not in data_str:
                print(f"⚠️ 腾讯API返回空数据")
                return None, "none"
            
            parts = data_str.split('~')
            if len(parts) < 30:
                print(f"⚠️ 腾讯API数据格式错误")
                return None, "none"
            
            name = parts[1] if len(parts) > 1 else ''
            current_price = self.safe_float(parts[3]) if len(parts) > 3 else 0
            prev_close = self.safe_float(parts[4]) if len(parts) > 4 else 0
            
            data = {
                'regularMarketPrice': current_price,
                'trailingPE': 0,
                'priceToBook': 0,
                'name': name,
                'changePercent': ((current_price - prev_close) / prev_close * 100) if prev_close else 0,
                'volume': self.safe_float(parts[9]) if len(parts) > 9 else 0,
                'high': self.safe_float(parts[6]) if len(parts) > 6 else 0,
                'low': self.safe_float(parts[7]) if len(parts) > 7 else 0,
                'open': self.safe_float(parts[5]) if len(parts) > 5 else 0,
                'prev_close': prev_close,
            }
            
            print(f"✅ [腾讯API] 成功获取 {clean_code}")
            return data, "tencent"
            
        except Exception as e:
            print(f"❌ [腾讯API] 抓取 {symbol} 异常: {e}")
            return None, "none"

    def get_a_stock_data(self, symbol):
        """
        A 股数据获取主入口：多数据源降级策略
        1. 新浪财经 API（最快）
        2. 腾讯财经 API（备用）
        3. AkShare（最后保障）
        """
        # 方案1：新浪财经 API
        data, source = self.get_a_stock_data_sina(symbol)
        if data is not None:
            return data, source
        
        # 方案2：腾讯财经 API
        print(f"🔄 切换到腾讯API...")
        data, source = self.get_a_stock_data_tencent(symbol)
        if data is not None:
            return data, source
        
        # 方案3：Yahoo
        
        print(f"❌ 所有 A 股数据源均失败: {symbol}")
        return None, "none"

    def get_a_stock_history(self, symbol, period="1mo"):
        """获取 A 股历史数据"""
        try:
            clean_code = symbol.split('.')[0]
            # 使用 yfinance 获取 A 股历史数据
            ticker = yf.Ticker(f"{clean_code}.SS")
            hist = ticker.history(period=period)
            if hist is not None and not hist.empty:
                return hist
            return None
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return None

    def get_data(self, stock, symbol, is_us):
        """美股/港股/日股数据获取（使用 yfinance）"""
        if is_us and symbol in self.cache:
            if time.time() - self.cache[symbol].get('timestamp', 0) < 3600:
                print(f"命中缓存: {symbol}")
                return self.cache[symbol]['data'], "cache"

        strategy_order = SOURCE_MAP.get(symbol, DEFAULT_STRATEGY)
        
        for source in strategy_order:
            try:
                print(f"尝试源 {source} 抓取 {symbol}...")
                info = stock.info
                if info and 'regularMarketPrice' in info:
                    if is_us:
                        self.cache[symbol] = {'data': info, 'timestamp': time.time()}
                        self._save_cache()
                    return info, source
            except Exception as e:
                print(f"源 {source} 抓取 {symbol} 失败: {e}")
        
        return None, "none"


def make_ai_news(stock_data):
    if not stock_data: 
        return "暂无数据"
    up_count = sum(1 for s in stock_data if s['isUp'])
    market_breadth = "多头回补" if up_count > (len(stock_data) / 2) else "弱势震荡"
    return (f"【盘后策略官·自动决策】：今日全球硬科技标的整体呈现 {market_breadth} 态势。 "
            f"当前重点观察：PER TTM 估值在 {stock_data[0]['per']} 附近的垄断类资产， "
            f"配合距52周高位的 {stock_data[0]['distHigh']} 回撤，市场已进入结构性调仓阶段。")


def get_market_type(symbol):
    if symbol.endswith('.T'):
        return "日股"
    elif symbol.endswith(('.SS', '.SZ', '.SH')):
        return "A股"
    elif symbol.endswith('.HK'):  # ⭐ 新增港股支持
        return "港股"
    elif symbol.endswith('.KS'):
        return "韩股"
    elif symbol.endswith('.DE'):
        return "德股"
    else:
        return "美股"


def fetch_all_data():
    output_data = {
        "macro": [],
        "stocks": [],
        "ai_report": "",
        "theme_mapping": THEME_MAPPING  # ⭐ 新增：把主题映射写入 data.json
    }
        
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    manager = StockDataManager()

    # 在 fetch_all_data 函数中，修改大盘数据抓取部分
    # ⭐ 类型对应的标签文字和CSS类
    BADGE_MAP = {
        "index": {"label": "", "class": "index"},
        "forex": {"label": "FX", "class": "forex"},
        "futures": {"label": "期货", "class": "futures"},
        "etf": {"label": "ETF", "class": "etf"},
        "j-etf": {"label": "J-ETF", "class": "j-etf"},
        "commodity": {"label": "商品", "class": "commodity"},
        "bond": {"label": "债券", "class": "bond"},
        "sentiment": {"label": "情绪", "class": "sentiment"},
        "crypto": {"label": "加密", "class": "crypto"},
    }
    
    # 1. 抓取大盘数据
    for m in MACRO_LIST:
        try:
            symbol = m["symbol"]
            name = m["name"]
            print(f"🔄 正在获取大盘数据: {symbol} ({name})")
            data_type = m.get("type", "index")  # 默认为 index
            
            
            stock = yf.Ticker(symbol, session=session)
            h_df = stock.history(period="1mo")
            h_df = h_df.dropna(subset=['Close'])
            # 打印数据行数
            print(f"   📊 {symbol} 获取到 {len(h_df)} 行数据")
        
            if len(h_df) >= 2:
                closes = h_df['Close'].tail(2).tolist()
                current = closes[1]
                prev_close = closes[0]
                
                diff = current - prev_close
                pct = (diff / prev_close) * 100
                sign = "+" if diff > 0 else ""
                
                # ⭐ 根据类型生成标签
                badge_info = BADGE_MAP.get(data_type, {"label": "", "class": "index"})
                
                output_data["macro"].append({
                    "name": name,  # ✅ 修复：不再使用未定义的 label
                    "price": f"{current:.2f}",
                    "change": f"{sign}{diff:.2f} ({sign}{pct:.2f}%)",
                    "isUp": diff > 0,
                    "type": data_type,  # 前端可用
                    "badge_label": badge_info["label"],  # 标签文字
                    "badge_class": badge_info["class"],  # CSS 类名
                })
            else:
                print(f"⚠️ {symbol} 数据不足: {len(h_df)} 行")            
            time.sleep(0.1)
        except Exception as e:
            print(f"大盘 {m['name']} 异常: {e}")

    # 2. 抓取自选个股数据
    for item in WATCHLIST:
        symbol = item["symbol"]
        market_type = get_market_type(symbol)

        # 核心分流
        if market_type == "A股":
            info, source = manager.get_a_stock_data(symbol)
            stock = None
        else:
            stock = yf.Ticker(symbol, session=session)
            info, source = manager.get_data(stock, symbol, market_type == "美股")
            
        if not info: 
            print(f"⚠️ 跳过 {item['name']}: 无法获取数据")
            continue
        
        try:
            print(f"处理 {item['name']}...")
            
            # 获取历史数据
            if market_type == "A股":
                h_df = manager.get_a_stock_history(symbol)
                if h_df is None or h_df.empty:
                    print(f"⚠️ {item['name']} 历史数据为空")
                    continue
                closes = h_df['Close'].tail(2).tolist()
                if len(closes) < 2:
                    continue
                current_price = closes[1]
                prev_close = closes[0]
                high_1w = h_df['High'].tail(5).max()
                high_1m = h_df['High'].max()
                
                # 年初以来变化率（A股：使用全年数据）
                ytd_first_close = h_df.iloc[0]['Close']
                ytd_change = ((current_price - ytd_first_close) / ytd_first_close) * 100 if ytd_first_close else 0
            
            else:
                h_df = stock.history(period="1mo")
                h_df = h_df.dropna(subset=['High', 'Close'])
                if h_df.empty or len(h_df) < 2:
                    continue
                closes = h_df['Close'].tail(2).tolist()
                current_price = closes[1]
                prev_close = closes[0]
                high_1w = h_df['High'].tail(5).max()
                high_1m = h_df['High'].max()
                
                # 年初以来变化率（美股/日股/韩股：使用 yfinance ytd 数据）
                h_df_ytd = stock.history(period="ytd")
                if not h_df_ytd.empty and len(h_df_ytd) > 0:
                    ytd_first_close = h_df_ytd.iloc[0]['Close']
                    ytd_change = ((current_price - ytd_first_close) / ytd_first_close) * 100 if ytd_first_close else 0
                else:
                    ytd_change = 0
            
            # 计算涨跌幅
            diff = current_price - prev_close
            percent = (diff / prev_close) * 100 if prev_close != 0 else 0
            sign = "+" if diff > 0 else ""
            
            # 回撤计算
            dist_high_str = "--"
            dist_week_str = "--"
            dist_month_str = "--"
            
            if high_1w and high_1w >= current_price:
                dist_week = ((current_price - high_1w) / high_1w) * 100
                dist_week_str = f"{dist_week:.1f}%"
                
            if high_1m and high_1m >= current_price:
                dist_month = ((current_price - high_1m) / high_1m) * 100
                dist_month_str = f"{dist_month:.1f}%"

            # 基本面指标
            per_display, forward_per_display, pbr_display = "--", "--", "--"
            roe_display = "--"
            
            if market_type == "A股":
                per = info.get('trailingPE', 0)
                if per and per > 0:
                    per_display = f"{per:.2f}"
                pbr = info.get('priceToBook', 0)
                if pbr and pbr > 0:
                    pbr_display = f"{pbr:.2f}"
            else:
                try:
                    stock_info = stock.info
                    if isinstance(stock_info, dict):
                        high_52w = stock_info.get('fiftyTwoWeekHigh')
                        if high_52w and float(high_52w) >= current_price:
                            dist_high = ((current_price - float(high_52w)) / float(high_52w)) * 100
                            dist_high_str = f"{dist_high:.1f}%"
                        
                        per = stock_info.get('trailingPE') or stock_info.get('forwardPE') or stock_info.get('regularMarketTrailingPE')
                        if per and isinstance(per, (int, float)): 
                            per_display = f"{per:.2f}"

                        forward_per = stock_info.get('forwardPE') 
                        if forward_per and isinstance(forward_per, (int, float)): 
                            forward_per_display = f"{forward_per:.2f}"
                            
                        # ⭐ ROE（自己資本利益率）
                        roe = stock_info.get('returnOnEquity')
                        if roe and isinstance(roe, (int, float)):
                            roe_display = f"{roe * 100:.1f}%"
                        else:
                            roe_display = "--"

                        pbr = stock_info.get('priceToBook')
                        if pbr and isinstance(pbr, (int, float)): 
                            pbr_display = f"{pbr:.2f}"
                except Exception as inf_e:
                    print(f"获取 {item['name']} 基本面指标异常: {inf_e}")

            # 均线
            ma20 = h_df['Close'].tail(20).mean() if len(h_df) >= 20 else current_price
            trend_label = "牛市多头" if current_price >= ma20 else "熊市空头"

            # ⭐ 获取原始 tags 并合并
            raw_tags = item.get("tags", [])
            tag_theme_list = get_theme_paths_for_tags(raw_tags, TAG_THEME_MAP)
            # 调试输出
            if tag_theme_list:
                for t in tag_theme_list:
                    if t["theme_path"]:
                        print(f"  ✅ {item['name']} → {t['tag']} → {' > '.join(t['theme_path'])}")
                    else:
                        print(f"  ⚠️ {item['name']} → {t['tag']} → 未找到主题映射")

            # 构建股票数据对象
            stock_entry = {
                "code": symbol.split('.')[0] if '.' in symbol else symbol,
                "name": item["name"],
                "sector": item.get("sector", "未分类板块"),
                "industry": item.get("industry", "其他"),
                "feature": item["feature"],
                "tags": raw_tags,                    # 原始 tags
                "tag_themes": tag_theme_list,        # 原始 tags 对应的 theme_path
                "market_type": market_type,
                "price": f"{current_price:.2f}",
                "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)",
                "isUp": diff > 0,
                "per": per_display,
                "roe": roe_display,
                "forward_per": forward_per_display,
                "pbr": pbr_display,
                "distHigh": dist_high_str,
                "ytdChange": f"{ytd_change:.2f}%",
                "distWeek": dist_week_str,
                "distMonth": dist_month_str,
                "trend": trend_label,
                "source": source,
            }
            
            output_data["stocks"].append(stock_entry)
            
            time.sleep(random.uniform(0.1, 0.2))
            
        except Exception as e:
            print(f"跳过 {item['name']}: {e}")
            import traceback
            traceback.print_exc()

    # 3. 注入 AI 简报
    output_data["ai_report"] = make_ai_news(output_data["stocks"])

    with open('data/data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("🎉 数据打包成功！")


if __name__ == "__main__":
    fetch_all_data()
