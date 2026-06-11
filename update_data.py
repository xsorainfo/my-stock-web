import json
import yfinance as yf
import time
import random
import os

# 定义带二级分类的观察名单
WATCHLIST = [
    # 行业：半导体
    {"symbol": "NVDA", "name": "英伟达 (美)", "industry": "1. AI半导体与核心设备", "subCategory": "核心计算芯片", "feature": "全球AI算力GPU绝对霸主"},
    {"symbol": "ASML", "name": "阿斯麦 (美)", "industry": "1. AI半导体与核心设备", "subCategory": "晶圆制造设备", "feature": "全球高端光刻机独家垄断者"},
    {"symbol": "8035.T", "name": "东京电子 (日)", "industry": "1. AI半导体与核心设备", "subCategory": "晶圆制造设备", "feature": "全球涂布/显影设备巨头"},
    {"symbol": "6857.T", "name": "爱德万测试 (日)", "industry": "1. AI半导体与核心设备", "subCategory": "测试与封装", "feature": "全球HBM内存测试机霸主"},
    {"symbol": "6146.T", "name": "迪斯科 (日)", "industry": "1. AI半导体与核心设备", "subCategory": "测试与封装", "feature": "垄断晶圆精密减薄切割机"},
    
    # 行业：数据中心与通信
    {"symbol": "MSFT", "name": "微软 (美)", "industry": "2. AI数据中心与光缆", "subCategory": "云服务与算力底座", "feature": "全球AI云服务超级巨头"},
    {"symbol": "5803.T", "name": "フジクラ (日)", "industry": "2. AI数据中心与光缆", "subCategory": "光通信与连接", "feature": "AI数据中心高密度光缆"},
    {"symbol": "5801.T", "name": "古河电工 (日)", "industry": "2. AI数据中心与光缆", "subCategory": "光通信与连接", "feature": "CPO技术与光电子器件先驱"},
    
    # 行业：材料与核能 (以此类推添加 subCategory)
    {"symbol": "4063.T", "name": "信越化学 (日)", "industry": "3. 半导体核心先进材料", "subCategory": "基板与晶圆材料", "feature": "全球大硅片行业风向标"},
    {"symbol": "CEG", "name": "星座能源 (美)", "industry": "4. AI核能与电力设施", "subCategory": "核能供应", "feature": "微软数据中心核电供应商"}
]

# ... (MACRO_LIST 保持不变)

def fetch_all_data():
    output_data = {"macro": [], "stocks": [], "ai_report": ""}
    # ... (保持原有的 session 和宏观数据抓取逻辑)

    for item in WATCHLIST:
        symbol = item["symbol"]
        try:
            print(f"终端同步：{item['name']}...")
            stock = yf.Ticker(symbol)
            h_df = stock.history(period="1mo").dropna(subset=['High', 'Close'])
            
            if h_df.empty: continue
            
            # 计算逻辑保持不变，重点是下面将 item 中的字段全数塞入
            current_price = h_df['Close'].iloc[-1]
            # ... (其他指标计算逻辑)

            output_data["stocks"].append({
                "code": symbol.split('.')[0],
                "name": item["name"], 
                "industry": item["industry"], 
                "subCategory": item["subCategory"], # 必须加上这行
                "feature": item["feature"],
                "price": f"{current_price:.2f}",
                # ... (其余字段保持不变)
                "trend": "牛市多头" if current_price >= h_df['Close'].mean() else "熊市空头"
            })
            time.sleep(random.uniform(0.1, 0.2))
        except Exception as e:
            print(f"Error {item['name']}: {e}")

    output_data["ai_report"] = "AI终端数据已完成多级分类对齐。"
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
