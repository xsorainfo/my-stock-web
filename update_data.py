import json
import yfinance as yf
import time
import random
import os
import requests


from config import MACRO_LIST, WATCHLIST, DEFAULT_STRATEGY, SOURCE_MAP

class StockDataManager:
    def __init__(self, cache_file='stock_cache.json'):
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def get_data(self, stock, symbol, is_us):
        """统一的数据获取入口，优先使用缓存"""
        # 1. 缓存查询
        if is_us and symbol in self.cache:
            if time.time() - self.cache[symbol].get('timestamp', 0) < 3600:
                print(f"命中缓存: {symbol}")
                return self.cache[symbol]['data'], "cache"

        # 2. 策略调度
        strategy_order = SOURCE_MAP.get(symbol, DEFAULT_STRATEGY)
        for source in strategy_order:
            try:
                print(f"尝试源 {source} 抓取 {symbol}...")
                info = stock.info # 利用传入的 stock 对象
                if info and 'regularMarketPrice' in info:
                    # 3. 写入缓存 (仅美股)
                    if is_us:
                        self.cache[symbol] = {'data': info, 'timestamp': time.time()}
                        self._save_cache()
                    return info, source
            except Exception as e:
                print(f"源 {source} 抓取 {symbol} 失败: {e}")
        
        return None, "none"


# MACRO_LIST = [
#     {"symbol": "^SOX", "name": "费城半导体指数"},
#     {"symbol": "JPY=X", "name": "美元/日元 (汇率)"}
# ]

# WATCHLIST = [
#     {"symbol": "NVDA", "name": "英伟达 (美)", "industry": "1. AI半导体与核心设备", "feature": "全球AI算力GPU绝对霸主，万亿AI生态的缔造者"},
#     {"symbol": "6981.T", "name": "村田制作所 (日)", "industry": "5. 边缘AI与智能终端", "feature": "全球MLCC电容之王，AI终端硬件升级换代的刚需元器件"}
# ]




def make_ai_news(stock_data):
    if not stock_data: return "暂无数据"
    up_count = sum(1 for s in stock_data if s['isUp'])
    market_breadth = "多头回补" if up_count > (len(stock_data) / 2) else "弱势震荡"
    return (f"【盘后策略官·自动决策】：今日全球硬科技标的整体呈现 {market_breadth} 态势。 "
            f"当前重点观察：PER TTM 估值在 {stock_data[0]['per']} 附近的垄断类资产， "
            f"配合距52周高位的 {stock_data[0]['distHigh']} 回撤，市场已进入结构性调仓阶段。")

    
def fetch_all_data():
    output_data = {"macro": [], "stocks": [], "ai_report": ""}
    
    # 🌟 干净安全的独立网络 Session 会话，彻底剔除旧版 utils 接口
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    manager = StockDataManager()

    # 1. 抓取大盘数据
    for m in MACRO_LIST:
        try:
            stock = yf.Ticker(m["symbol"], session=session)
            h_df = stock.history(period="1mo").dropna(subset=['Close'])
            if len(h_df) >= 2:
                curr, prev = h_df['Close'].iloc[-1], h_df['Close'].iloc[-2]
                diff = curr - prev
                pct = (diff / prev) * 100
                output_data["macro"].append({"name": m["name"], "price": f"{curr:.2f}", "change": f"{diff:+.2f} ({pct:+.2f}%)", "isUp": diff > 0})
        except: pass
            print(f"大盘 {m['name']} 异常: {e}")

    # 2. 抓取自选个股数据
    for item in WATCHLIST:
        symbol = item["symbol"]
        is_us = not symbol.endswith('.T')
        # 统一初始化 ticker
        stock = yf.Ticker(symbol, session=session)
        
        # 通过 manager 获取 info
        info, source = manager.get_data(stock, symbol, is_us)
        if not info: continue
        
        try:
            print(f"终端同步：正在抓取并对齐多周期时区 {item['name']}...")
            
            h_df = stock.history(period="1mo")
            h_df = h_df.dropna(subset=['High', 'Close'])
            

            if h_df.empty or len(h_df) < 2:
                continue
            curr = h_df['Close'].iloc[-1]      
            closes = h_df['Close'].tail(2).tolist()
            current_price = closes[1]
            prev_close = closes[0]
                
            diff = current_price - prev_close
            percent = (diff / prev_close) * 100
            sign = "+" if diff > 0 else ""
            
            # 多周期回撤比例计算
            dist_high_str = "--"  # 52周
            dist_week_str = "--"  # 1周
            dist_month_str = "--" # 1个月
            
            # 最近1周最高回撤
            high_1w = h_df['High'].tail(5).max()
            if high_1w and high_1w >= current_price:
                dist_week = ((current_price - high_1w) / high_1w) * 100
                dist_week_str = f"{dist_week:.1f}%"
                
            # 最近1个月最高回撤
            high_1m = h_df['High'].max()
            if high_1m and high_1m >= current_price:
                dist_month = ((current_price - high_1m) / high_1m) * 100
                dist_month_str = f"{dist_month:.1f}%"

            per_display, forward_per_display, pbr_display = "--", "--", "--"
            try:
                info = stock.info
                if isinstance(info, dict):
                    # 52周最高回撤
                    high_52w = info.get('fiftyTwoWeekHigh')
                    if high_52w and float(high_52w) >= current_price:
                        dist_high = ((current_price - float(high_52w)) / float(high_52w)) * 100
                        dist_high_str = f"{dist_high:.1f}%"
                    
                    # 🎯 核心修正：优先提取代表滚动市盈率的 trailingPE (TTM口径)
                    # 如果不存在（比如刚上市或高增长导致无前四季度对比），则采用 forwardPE 进行防御对齐
                    per = info.get('trailingPE') or info.get('forwardPE') or info.get('regularMarketTrailingPE')
                    if per and isinstance(per, (int, float)): per_display = f"{per:.2f}"

                    # 增加预想 PER (Forward PE)
                    forward_per = info.get('forwardPE') 
                    if forward_per and isinstance(forward_per, (int, float)): forward_per_display = f"{forward_per:.2f}"

                    pbr = info.get('priceToBook')
                    if pbr and isinstance(pbr, (int, float)): pbr_display = f"{pbr:.2f}"
            except Exception as inf_e:
                print(f"获取 {item['name']} 基本面指标异常: {inf_e}")

            ma20 = h_df['Close'].mean()
            trend_label = "牛市多头" if current_price >= ma20 else "熊市空头"

            
            # 存入数据字典
            output_data["stocks"].append({
                "code": symbol.split('.')[0] if '.' in symbol else symbol,
                "name": item["name"], "industry": item["industry"], "feature": item["feature"],
                "price": f"{current_price:.2f}", "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)", "isUp": diff > 0,
                "per": per_display, 
                "forward_per": forward_per_display, 
                "pbr": pbr_display, 
                "distHigh": dist_high_str,       
                "distWeek": dist_week_str,       
                "distMonth": dist_month_str,     
                "trend": trend_label,
                "source": source, # 🌟 来源标记
                "is_us": is_us，
                "isUp": curr >= prev
            })
            time.sleep(random.uniform(0.1, 0.2))
        except Exception as e:
            print(f"跳过 {item['name']}: {e}")

    # 3. 注入 AI 简报
    output_data["ai_report"] = make_ai_news(output_data["stocks"])

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("🎉 TTM高参考性数据源打包成功！")

if __name__ == "__main__":
    fetch_all_data()
