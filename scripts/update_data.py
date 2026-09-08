# scripts/update_data.py

import sys
import os
import json
import yfinance as yf
import time
import random
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


# ⭐ 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MACRO_LIST, WATCHLIST, DEFAULT_STRATEGY, SOURCE_MAP
from theme_mapping import THEME_MAPPING  # ⭐ 从 theme_mapping.py 导入
from tag_display_map import TAG_DISPLAY_MAP  # ⭐ 导入显示映射
from portfolio_lists import PORTFOLIO_LISTS

# ============================================================
# ⭐ Tag 显示名称转换函数
# ============================================================
def get_display_tags(tags):
    """
    将原始 tags 转换为显示名称列表
    有映射就输出映射后的，没有就输出原始 tag
    """
    if not tags:
        return []
    result = []
    for tag in tags:
        display_tag = TAG_DISPLAY_MAP.get(tag, tag)
        if display_tag not in result:
            result.append(display_tag)
    return result


# ============================================================
# ⭐ 从 THEME_MAPPING 自动构建二级→三级映射（支持新格式）
# ============================================================
def build_level2_to_level3(theme_mapping):
    """
    从 THEME_MAPPING 自动构建二级标签 → 三级标签列表的映射
    同时保留注释信息
    支持新格式：{"tags": [...], "description": "..."}
    """
    level2_to_level3 = {}
    level2_descriptions = {}  # ⭐ 存储二级分类的注释
    
    if not theme_mapping:
        return level2_to_level3, level2_descriptions
    
    for level1_key, level1_value in theme_mapping.items():
        if isinstance(level1_value, dict):
            for level2_key, level2_value in level1_value.items():
                # ⭐ 检查新格式：如果是 dict 且有 tags 字段
                if isinstance(level2_value, dict):
                    level2_descriptions[level2_key] = level2_value.get("description", "")
                    level2_to_level3[level2_key] = level2_value.get("tags", [])
                elif isinstance(level2_value, list):
                    # 兼容旧格式
                    level2_to_level3[level2_key] = level2_value
                    level2_descriptions[level2_key] = ""
    
    return level2_to_level3, level2_descriptions


# ⭐ 自动生成展开映射
LEVEL2_TO_LEVEL3, LEVEL2_DESCRIPTIONS = build_level2_to_level3(THEME_MAPPING)


# ============================================================
# ⭐ Tag 合并函数
# ============================================================
def merge_tagsOld(tags):
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


def merge_tags(tags):
    """
    不再展开二级标签，直接返回原始 tags
    """
    if not tags:
        return []
    
    # 去重后直接返回
    result = []
    for tag in tags:
        if tag not in result:
            result.append(tag)
    return result


# ============================================================
# ⭐ 构建 tag → theme_path 映射（支持新格式）
# ============================================================
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
                # ⭐ 新格式：从 dict 中取 tags
                if isinstance(sub_theme_value, dict):
                    tags = sub_theme_value.get("tags", [])
                    for tag in tags:
                        if tag not in tag_map:
                            tag_map[tag] = [theme_name, sub_theme_name, tag]
                elif isinstance(sub_theme_value, list):
                    # 兼容旧格式
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
                # ⭐ 新格式：二级名称本身作为一个可匹配的 tag
                if sub_theme_name not in tag_map:
                    tag_map[sub_theme_name] = [theme_name, sub_theme_name]
                # 如果三级列表中有与二级名称相同的 tag，保持第三层匹配优先
    
    # 第三遍：匹配第一层（最低优先级）
    for theme_name, theme_value in theme_mapping.items():
        if theme_name not in tag_map:
            tag_map[theme_name] = [theme_name]
    
    return tag_map


# 全局构建 tag → theme_path 映射（在模块加载时执行一次）
TAG_THEME_MAP = build_tag_theme_mapping(THEME_MAPPING)


# ============================================================
# ⭐ 获取 tag 对应的 theme_path（使用映射后的名称匹配）
# ============================================================
def get_theme_paths_for_tags(tags, tag_theme_map):
    """
    根据 tags 列表，返回每个 tag 对应的 theme_path
    
    匹配逻辑：
    1. 先在 TAG_DISPLAY_MAP 中查找映射后的名称
    2. 用映射后的名称去 tag_theme_map 中匹配
    3. tag 字段存储映射后的统一名称（用于前端匹配）
    
    返回格式:
    [
        {"tag": "EUV (极紫外光刻)", "theme_path": ["1. 半导体设备", "光刻机", "EUV (极紫外光刻)"]},
        {"tag": "GPU", "theme_path": ["3. 算力芯片", "GPU"]},
    ]
    """
    result = []
    if not tags:
        return result
    
    for tag in tags:
        # ⭐ 先通过 TAG_DISPLAY_MAP 获取映射后的名称
        mapped_tag = TAG_DISPLAY_MAP.get(tag, tag)
        
        # ⭐ 用映射后的名称去匹配 THEME_MAPPING
        theme_path = tag_theme_map.get(mapped_tag, [])
        
        # 如果映射后的名称也找不到，再用原始 tag 尝试
        if not theme_path and mapped_tag != tag:
            theme_path = tag_theme_map.get(tag, [])
            # 如果原始 tag 找到了，使用原始 tag 作为统一名称
            unified_tag = tag
        else:
            # 使用映射后的名称作为统一名称
            unified_tag = mapped_tag
        
        result.append({
            "tag": unified_tag,  # ⭐ 存储映射后的统一名称！
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
            # 使用 yfinance 获取 A 股历史数据
            yahoo_symbol = symbol[:-3] + ".SS" if symbol.endswith(".SH") else symbol
            ticker = yf.Ticker(yahoo_symbol)
            hist = ticker.history(period=period)
            if hist is not None and not hist.empty:
                return hist
            return None
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return None

    def get_a_stock_ytd_change(self, symbol, current_price):
        """Calculate YTD from the last available close of the previous year."""
        try:
            year = datetime.now().year
            yahoo_symbol = symbol[:-3] + ".SS" if symbol.endswith(".SH") else symbol
            history = yf.Ticker(yahoo_symbol).history(start=f"{year - 1}-12-01")
            if history is None or history.empty:
                return None
            closes = history['Close'].dropna()
            previous_year = closes[closes.index.year < year]
            if previous_year.empty:
                return None
            baseline = float(previous_year.iloc[-1])
            if baseline <= 0:
                return None
            return (current_price - baseline) / baseline * 100
        except Exception as e:
            print(f"获取 {symbol} 年初基准失败: {e}")
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



def _extract_ai_text(payload):
    """Extract text from the Responses API while tolerating minor response shape changes."""
    if not isinstance(payload, dict):
        return ""
    if payload.get("output_text"):
        return str(payload["output_text"]).strip()
    for item in payload.get("output", []):
        for part in item.get("content", []) if isinstance(item, dict) else []:
            if isinstance(part, dict) and part.get("text"):
                return str(part["text"]).strip()
    return ""


def _market_snapshot(stock_data, macro_data, update_status):
    """Keep the model input compact while covering all supported markets."""
    def change_abs(item):
        try:
            return abs(float(str(item.get("change", "0")).split("(")[-1].replace("%)", "")))
        except (TypeError, ValueError):
            return 0.0

    ranked = sorted(stock_data, key=change_abs, reverse=True)
    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "update_status": update_status,
        "macro": macro_data,
        "stocks": [
            {
                key: item.get(key)
                for key in (
                    "symbol", "name", "market_type", "price", "change", "trend",
                    "per", "forward_per", "roe", "pbr", "ytdChange",
                    "distHigh", "sector", "industry", "display_tags",
                )
            }
            for item in ranked[:80]
        ],
        "market_counts": {
            market: sum(1 for item in stock_data if item.get("market_type") == market)
            for market in ("美股", "A股", "日股", "港股", "韩股", "德股")
        },
    }


def generate_ai_strategy_report(stock_data, macro_data, update_status):
    """Generate a data-grounded report through Gemini or OpenAI with safe fallback."""
    fallback = make_ai_news(stock_data)
    api_key = os.getenv("AI_API_KEY", "").strip()
    if not api_key:
        return fallback, {"source": "fallback", "error": "AI_API_KEY 未配置"}

    snapshot = _market_snapshot(stock_data, macro_data, update_status)
    prompt = (
        "你是一个中文量化投研助理。仅依据下面行情快照生成简洁的盘后/盘前策略简报。"
        "不要编造新闻、财报或宏观事件；数据不足时明确写“数据不足”。"
        "必须覆盖全球市场环境、美股/A股/日股观察、下一交易时段观察清单、"
        "重点关注行业或标的及触发条件、失效条件和风险。避免保证收益或无条件买卖指令。"
        "用中文纯文本输出，分成5个短段，每段以“【】”开头，控制在600字以内。\\n\\n"
        "行情快照：\\n" + json.dumps(snapshot, ensure_ascii=False)
    )
    provider = "gemini"
    model = os.getenv("AI_MODEL", "").strip()

    try:
        if provider == "gemini":
            model = model or "gemini-flash-latest"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            body = {
                "contents": [{"parts": [{"text": prompt}]}],
            }
            response = None
            for attempt in range(3):
                response = requests.post(
                    url,
                    headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
                    json=body,
                    timeout=45,
                )
                if response.status_code not in (429, 500, 502, 503, 504) or attempt == 2:
                    break
                wait_seconds = 2 ** attempt
                print(f"Gemini 暂时不可用（HTTP {response.status_code}），{wait_seconds} 秒后重试...")
                time.sleep(wait_seconds)
            if not response.ok:
                detail = response.text.replace(api_key, "[REDACTED]")[:400]
                raise RuntimeError(f"Gemini HTTP {response.status_code}: {detail}")
            data = response.json()
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            if not text:
                raise ValueError("Gemini API 未返回文本")
            return text, {"source": "gemini", "model": model}
        model = model or "gpt-5.5"
        body = {
            "model": model, "store": False,
            "input": [
                {"role": "system", "content": [{"type": "input_text", "text": "你输出的是供个人复盘使用的研究摘要，不构成投资建议。"}]},
                {"role": "user", "content": [{"type": "input_text", "text": prompt}]},
            ],
        }
        response = requests.post(
            os.getenv("AI_API_BASE_URL", "https://api.openai.com/v1/responses"),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=body, timeout=45,
        )
        response.raise_for_status()
        text = _extract_ai_text(response.json())
        if not text:
            raise ValueError("Responses API 未返回文本")
        return text, {"source": "openai", "model": model}
    except Exception as exc:
        print(f"⚠️ AI策略生成失败，使用备用策略: {exc}")
        safe_error = str(exc).replace(api_key, "[REDACTED]")[:400]
        raise RuntimeError(f"Gemini策略生成失败: {safe_error}") from exc


def make_ai_news(stock_data):
    if not stock_data: 
        return "暂无数据"
    up_count = sum(1 for s in stock_data if s['isUp'])
    market_breadth = "多头回补" if up_count > (len(stock_data) / 2) else "弱势震荡"
    return (f"【盘后策略官·自动决策】：今日全球硬科技标的整体呈现 {market_breadth} 态势。 "
            f"当前重点观察：PER TTM 估值在 {stock_data[0]['per']} 附近的垄断类资产， "
            f"配合距52周高位的 {stock_data[0]['distHigh']} 回撤，市场已进入结构性调仓阶段。")


def build_intraday_signal(percent, trend_label, rsi, volume_ratio):
    """Combine daily move, trend, RSI and volume into a transparent score."""
    score = 50
    score += 15 if trend_label == "牛市多头" else -15
    score += 15 if percent >= 1 else -15 if percent <= -1 else 0
    score += 10 if rsi >= 55 else -10 if rsi <= 45 else 0
    score += 10 if volume_ratio >= 1.2 and percent > 0 else -10 if volume_ratio >= 1.2 and percent < 0 else 0
    score = max(0, min(100, score))
    if score >= 70:
        label, css = "日内偏强", "signal-up"
    elif score >= 55:
        label, css = "偏强观察", "signal-up"
    elif score <= 30:
        label, css = "日内偏弱", "signal-down"
    elif score <= 45:
        label, css = "偏弱观察", "signal-down"
    else:
        label, css = "震荡观察", "signal-flat"
    reason = f"综合分 {score}/100 · RSI {rsi:.0f} · 量比 {volume_ratio:.1f}x"
    return {"label": label, "class": css, "reason": reason, "score": score, "rsi": round(rsi, 1), "volume_ratio": round(volume_ratio, 2)}

def build_flow_proxy(percent, trend_label, volume_ratio):
    """Estimate price-volume flow; this is not institutional order data."""
    if volume_ratio >= 1.5 and percent > 0.5:
        label, css, reason = "疑似流入", "signal-up", "上涨伴随明显放量"
    elif volume_ratio >= 1.5 and percent < -0.5:
        label, css, reason = "疑似流出", "signal-down", "下跌伴随明显放量"
    elif volume_ratio >= 1.2 and trend_label == "牛市多头":
        label, css, reason = "偏流入", "signal-up", "多头趋势且量能高于均值"
    elif volume_ratio >= 1.2 and trend_label == "熊市空头":
        label, css, reason = "偏流出", "signal-down", "空头趋势且量能高于均值"
    else:
        label, css, reason = "资金观望", "signal-flat", "量能未出现明显异常"
    return {"label": label, "class": css, "reason": reason, "volume_ratio": round(volume_ratio, 2)}

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


def portfolio_watchlist():
    """Include symbols added through the portfolio editor in the data pipeline."""
    result = list(WATCHLIST)
    normalize = lambda symbol: symbol.upper().replace('.SH', '.SS')
    seen = {normalize(item["symbol"]) for item in result}
    for portfolio in PORTFOLIO_LISTS.values():
        for symbol in portfolio.get("symbols", []):
            symbol = normalize(symbol)
            if symbol not in seen:
                result.append({
                    "symbol": symbol, "name": symbol,
                    "sector": "自选追加", "industry": "自选追加",
                    "feature": "从投资组合手动追加", "tags": []
                })
                seen.add(symbol)
    return result


def fetch_macro_item(m, session, badge_map):
    """Fetch one macro series; failures stay isolated from the batch."""
    symbol, name = m["symbol"], m["name"]
    try:
        print(f"🔄 正在获取大盘数据: {symbol} ({name})")
        stock = yf.Ticker(symbol, session=session)
        h_df = stock.history(period="1mo").dropna(subset=["Close"])
        if len(h_df) < 2:
            print(f"⚠️ {symbol} 数据不足: {len(h_df)} 行")
            return None
        current, previous = h_df["Close"].tail(2).tolist()
        diff = current - previous
        pct = (diff / previous) * 100 if previous else 0
        sign = "+" if diff > 0 else ""
        badge = badge_map.get(m.get("type", "index"), {"label": "", "class": "index"})
        return {"name": name, "price": f"{current:.2f}", "change": f"{sign}{diff:.2f} ({sign}{pct:.2f}%)", "isUp": diff > 0, "type": m.get("type", "index"), "badge_label": badge["label"], "badge_class": badge["class"]}
    except Exception as e:
        print(f"大盘 {name} 异常: {e}")
        return None


def fetch_all_data():
    output_data = {
        "macro": [],
        "stocks": [],
        "ai_report": "",
        "theme_mapping": THEME_MAPPING,  # ⭐ 把主题映射写入 data.json
        "tag_display_map": TAG_DISPLAY_MAP,  # ⭐ 把显示映射写入 data.json
        "theme_descriptions": {},  # ⭐ 新增：存储二级分类的注释
        "portfolio_lists": PORTFOLIO_LISTS,
        "generated_at": datetime.now().astimezone().isoformat(),
        "update_status": {"expected": 0, "success": 0, "failed": 0, "failed_symbols": []}
    }
    
    # ⭐ 构建二级分类注释映射
    _, level2_descriptions = build_level2_to_level3(THEME_MAPPING)
    output_data["theme_descriptions"] = level2_descriptions
        
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
    
    # 1. 并发抓取大盘数据（上限 8，避免压垮外部数据源）
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(fetch_macro_item, m, session, BADGE_MAP) for m in MACRO_LIST]
        for future in as_completed(futures):
            result = future.result()
            if result:
                output_data["macro"].append(result)

    # 2. 抓取自选个股数据
    watchlist_items = portfolio_watchlist()
    expected_symbols = {item['symbol'] for item in watchlist_items}
    for item in watchlist_items:
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
                ytd_change = manager.get_a_stock_ytd_change(symbol, current_price)
            
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
            ma5 = h_df["Close"].tail(5).mean() if len(h_df) >= 5 else current_price
            delta = h_df["Close"].diff().dropna().tail(14)
            gains = delta[delta > 0].sum()
            losses = -delta[delta < 0].sum()
            rsi = 100 if losses == 0 and gains > 0 else (100 - (100 / (1 + gains / losses)) if losses else 50)
            avg_volume = h_df["Volume"].tail(5).mean() if "Volume" in h_df and h_df["Volume"].tail(5).mean() else 0
            latest_volume = float(h_df["Volume"].iloc[-1]) if "Volume" in h_df and len(h_df) else 0
            volume_ratio = latest_volume / avg_volume if avg_volume else 1.0
            intraday_signal = build_intraday_signal(percent, trend_label, rsi, volume_ratio)
            flow_proxy = build_flow_proxy(percent, trend_label, volume_ratio)

            # ⭐ 获取原始 tags 并合并
            raw_tags = item.get("tags", [])
            display_tags = get_display_tags(raw_tags)  # ⭐ 转换显示名称
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
                "symbol": symbol,
                "code": symbol.split('.')[0] if '.' in symbol else symbol,
                "name": item["name"],
                "sector": item.get("sector", "未分类板块"),
                "industry": item.get("industry", "其他"),
                "feature": item["feature"],
                "tags": raw_tags,                    # 原始 tags（用于前端匹配）
                "display_tags": display_tags,        # 映射后的 tags（用于前端显示）
                "tag_themes": tag_theme_list,        # 用映射后的名称匹配的 theme_path
                "market_type": market_type,
                "price": f"{current_price:.2f}",
                "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)",
                "isUp": diff > 0,
                "per": per_display,
                "roe": roe_display,
                "forward_per": forward_per_display,
                "pbr": pbr_display,
                "distHigh": dist_high_str,
                "ytdChange": f"{ytd_change:.2f}%" if ytd_change is not None else "--",
                "distWeek": dist_week_str,
                "distMonth": dist_month_str,
                "trend": trend_label,
                "intraday_signal": intraday_signal,
                "flow_proxy": flow_proxy,
                "source": source,
            }
            
            output_data["stocks"].append(stock_entry)
            
            time.sleep(random.uniform(0.1, 0.2))
            
        except Exception as e:
            print(f"跳过 {item['name']}: {e}")
            import traceback
            traceback.print_exc()

    # 3. 注入更新状态
    success_symbols = {stock.get("symbol") or stock.get("code") for stock in output_data["stocks"]}
    failed_symbols = sorted(expected_symbols - success_symbols)
    output_data["update_status"] = {
        "expected": len(expected_symbols),
        "success": len(success_symbols),
        "failed": len(failed_symbols),
        "failed_symbols": failed_symbols
    }
    output_data["generated_at"] = datetime.now().astimezone().isoformat()

    # 4. 注入 AI 简报
    try:
        output_data["ai_report"], ai_meta = generate_ai_strategy_report(
            output_data["stocks"], output_data["macro"], output_data["update_status"]
        )
    except Exception as exc:
        print(f"⚠️ AI策略失败，但股票数据继续提交: {exc}")
        output_data["ai_report"] = make_ai_news(output_data["stocks"])
        ai_meta = {
            "source": "fallback",
            "error": "AI策略暂时不可用，股票数据已正常更新",
        }
    output_data["ai_report_meta"] = ai_meta

    # ⭐ 确保 data 目录存在
    os.makedirs('data', exist_ok=True)
    
    with open('data/data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("🎉 数据打包成功！")


if __name__ == "__main__":
    fetch_all_data()
