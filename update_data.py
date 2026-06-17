import json
import yfinance as yf
import akshare as ak
import time
import random
import os
import requests

from config import MACRO_LIST, WATCHLIST, DEFAULT_STRATEGY, A_STOCK_STRATEGY, SOURCE_MAP

class StockDataManager:
    def __init__(self, cache_file='stock_cache.json'):
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

    def get_a_stock_data_akshare(self, symbol):
        """使用 AkShare 获取 A 股数据（备用方案）"""
        try:
            clean_code = symbol.split('.')[0]
            print(f"🔄 [AkShare] 正在获取 {clean_code} 数据...")
            
            time.sleep(random.uniform(0.5, 1.0))
            df = ak.stock_zh_a_spot_em()
            
            stock_info = df[df['代码'] == clean_code]
            if stock_info.empty:
                print(f"⚠️ [AkShare] 未找到股票 {clean_code}")
                return None, "none"
            
            row = stock_info.iloc[0]
            data = {
                'regularMarketPrice': self.safe_float(row.get('最新价', 0)),
                'trailingPE': self.safe_float(row.get('市盈率-动态', row.get('市盈率(动态)', 0))),
                'priceToBook': self.safe_float(row.get('市净率', 0)),
                'name': row.get('名称', ''),
                'changePercent': self.safe_float(row.get('涨跌幅', 0)),
                'volume': self.safe_float(row.get('成交量', 0)),
                'high': self.safe_float(row.get('最高', 0)),
                'low': self.safe_float(row.get('最低', 0)),
                'open': self.safe_float(row.get('开盘', 0)),
                'prev_close': self.safe_float(row.get('昨收', 0)),
            }
            
            print(f"✅ [AkShare] 成功获取 {clean_code}")
            return data, "akshare"
            
        except Exception as e:
            print(f"❌ [AkShare] 抓取 {symbol} 异常: {e}")
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
        
        # 方案3：AkShare
        print(f"🔄 降级到 AkShare...")
        data, source = self.get_a_stock_data_akshare(symbol)
        if data is not None:
            return data, source
        
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

        is_a_stock = symbol.endswith(('.SS', '.SZ', '.SH'))
        strategy_order = A_STOCK_STRATEGY if is_a_stock else SOURCE_MAP.get(symbol, DEFAULT_STRATEGY)
        
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


def fetch_all_data():
    output_data = {"macro": [], "stocks": [], "ai_report": ""}
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    manager = StockDataManager()

    # 1. 抓取大盘数据
    for m in MACRO_LIST:
        try:
            stock = yf.Ticker(m["symbol"], session=session)
            h_df = stock.history(period="1mo")
            h_df = h_df.dropna(subset=['Close'])
            
            if len(h_df) >= 2:
                closes = h_df['Close'].tail(2).tolist()
                current = closes[1]
                prev_close = closes[0]
                
                diff = current - prev_close
                pct = (diff / prev_close) * 100
                sign = "+" if diff > 0 else ""
                output_data["macro"].append({
                    "name": m["name"], 
                    "price": f"{current:.2f}",
                    "change": f"{sign}{diff:.2f} ({sign}{pct:.2f}%)", 
                    "isUp": diff > 0
                })
            time.sleep(0.1)
        except Exception as e:
            print(f"大盘 {m['name']} 异常: {e}")

    # 2. 抓取自选个股数据
    for item in WATCHLIST:
        symbol = item["symbol"]

        # 判断市场类型
        if symbol.endswith('.T'):
            market_type = "日股"
            is_us = False
        elif symbol.endswith('.SS') or symbol.endswith('.SZ') or symbol.endswith('.SH') or ('.' not in symbol and len(symbol) == 6):
            market_type = "A股"
            is_us = False
        else:
            market_type = "美股"
            is_us = True

        # 核心分流
        if market_type == "A股":
            info, source = manager.get_a_stock_data(symbol)
            stock = None
        else:
            stock = yf.Ticker(symbol, session=session)
            info, source = manager.get_data(stock, symbol, is_us)
            
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

                        pbr = stock_info.get('priceToBook')
                        if pbr and isinstance(pbr, (int, float)): 
                            pbr_display = f"{pbr:.2f}"
                except Exception as inf_e:
                    print(f"获取 {item['name']} 基本面指标异常: {inf_e}")

            # 均线
            ma20 = h_df['Close'].tail(20).mean() if len(h_df) >= 20 else current_price
            trend_label = "牛市多头" if current_price >= ma20 else "熊市空头"

            output_data["stocks"].append({
                "code": symbol.split('.')[0] if '.' in symbol else symbol,
                "name": item["name"], 
                "sector": item.get("sector", "未分类板块"),
                "industry": item["industry"], 
                "feature": item["feature"],
                "market_type": market_type,
                "price": f"{current_price:.2f}", 
                "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)", 
                "isUp": diff > 0,
                "per": per_display, 
                "forward_per": forward_per_display, 
                "pbr": pbr_display, 
                "distHigh": dist_high_str,       
                "distWeek": dist_week_str,       
                "distMonth": dist_month_str,     
                "trend": trend_label,
                "source": source,
                "is_us": is_us
            })
            
            time.sleep(random.uniform(0.1, 0.2))
            
        except Exception as e:
            print(f"跳过 {item['name']}: {e}")
            import traceback
            traceback.print_exc()

    # 3. 注入 AI 简报
    output_data["ai_report"] = make_ai_news(output_data["stocks"])

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("🎉 数据打包成功！")

if __name__ == "__main__":
    fetch_all_data()
