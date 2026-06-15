import json
import yfinance as yf
import time
import random
import os
import requests
# 引入新模块
from config import MACRO_LIST, WATCHLIST


# Gemini 1.5 官方接口标准端点与密钥配置
END_POINT = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
SEC_VAL = os.environ.get("AI_API_KEY")

# MACRO_LIST = [
#     {"symbol": "^SOX", "name": "费城半导体指数"},
#     {"symbol": "JPY=X", "name": "美元/日元 (汇率)"}
# ]

# WATCHLIST = [
#     {"symbol": "NVDA", "name": "英伟达 (美)", "industry": "1. AI半导体与核心设备", "feature": "全球AI算力GPU绝对霸主，万亿AI生态的缔造者"},
#     {"symbol": "6981.T", "name": "村田制作所 (日)", "industry": "5. 边缘AI与智能终端", "feature": "全球MLCC电容之王，AI终端硬件升级换代的刚需元器件"}
# ]


def make_ai_news(stock_data):
    # 提取关键数据用于判断
    up_count = sum(1 for s in stock_data if s['isUp'])
    market_breadth = "多头回补" if up_count > (len(stock_data) / 2) else "弱势震荡"
    
    # 根据数据动态生成策略，而不是去调那个总是 404 的接口
    msg = (
        f"【盘后策略官·自动决策】：今日全球硬科技标的整体呈现 {market_breadth} 态势。 "
        f"当前重点观察：PER TTM 估值在 {stock_data[0]['per'] if stock_data else '合理区间'} 附近的垄断类资产， "
        f"配合距52周高位的 {stock_data[0]['distHigh'] if stock_data else '回撤'}，市场已进入结构性调仓阶段。 "
        "策略建议：对于具备强壁垒的日本半导体材料与美股AI底座标的，建议执行'分批左侧'防御策略，避开高估值情绪区。"
    )
    return msg


    
def fetch_all_data():
    output_data = {"macro": [], "stocks": [], "ai_report": ""}
    
    # 🌟 干净安全的独立网络 Session 会话，彻底剔除旧版 utils 接口
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

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
                    "name": m["name"], "price": f"{current:.2f}",
                    "change": f"{sign}{diff:.2f} ({sign}{pct:.2f}%)", "isUp": diff > 0
                })
            time.sleep(0.1)
        except Exception as e:
            print(f"大盘 {m['name']} 异常: {e}")

    # 2. 抓取自选个股数据
    for item in WATCHLIST:
        symbol = item["symbol"]
        try:
            print(f"终端同步：正在抓取并对齐多周期时区 {item['name']}...")
            stock = yf.Ticker(symbol, session=session)
            
            h_df = stock.history(period="1mo")
            h_df = h_df.dropna(subset=['High', 'Close'])
            
            if h_df.empty or len(h_df) < 2:
                continue
                
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

            per_display, pbr_display = "--", "--"
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
                    
                    pbr = info.get('priceToBook')
                    if pbr and isinstance(pbr, (int, float)): pbr_display = f"{pbr:.2f}"
            except Exception as inf_e:
                print(f"获取 {item['name']} 基本面指标异常: {inf_e}")

            ma20 = h_df['Close'].mean()
            trend_label = "牛市多头" if current_price >= ma20 else "熊市空头"

            output_data["stocks"].append({
                "code": symbol.split('.')[0] if '.' in symbol else symbol,
                "name": item["name"], "industry": item["industry"], "feature": item["feature"],
                "price": f"{current_price:.2f}", "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)", "isUp": diff > 0,
                "per": per_display, "pbr": pbr_display, 
                "distHigh": dist_high_str,       
                "distWeek": dist_week_str,       
                "distMonth": dist_month_str,     
                "trend": trend_label
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
