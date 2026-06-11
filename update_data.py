import json
import yfinance as yf

# 1. 扩容版自选股清单（严格按照你想要的行业顺序排列，AI半导体置顶）
WATCHLIST = [
    # --- 1. AI半导体与核心设备 ---
    {"symbol": "8035.T", "name": "东京电子", "industry": "1. AI半导体与核心设备", "feature": "全球涂布/显影设备巨头，AI芯片制造的核心支柱"},
    {"symbol": "6857.T", "name": "爱德万测试", "industry": "1. AI半导体与核心设备", "feature": "全球HBM内存测试机霸主，深度绑定英伟达产业链"},
    {"symbol": "6146.T", "name": "迪斯科", "industry": "1. AI半导体与核心设备", "feature": "垄断晶圆精密减薄切割机，AI先进封装必用设备"},
    
    # --- 2. AI数据中心与光缆 ---
    {"symbol": "5803.T", "name": "フジクラ", "industry": "2. AI数据中心与光缆", "feature": "AI数据中心核心部件「高密度光缆」核心供应商"},
    {"symbol": "5801.T", "name": "古河电工", "industry": "2. AI数据中心与光缆", "feature": "下一代光电共封装(CPO)技术与光电子器件先驱"},
    {"symbol": "5802.T", "name": "住友电工", "industry": "2. AI数据中心与光缆", "feature": "全球高带宽连接器与特种光通信线缆行业龙头"},
    
    # --- 3. 半导体核心先进材料 ---
    {"symbol": "3110.T", "name": "日東紡績", "industry": "3. 半导体核心先进材料", "feature": "全球高频半导体基板用「超薄玻璃纤维布」垄断巨头"},
    {"symbol": "4063.T", "name": "信越化学", "industry": "3. 半导体核心先进材料", "feature": "全球大硅片与光刻胶绝对霸主，行业风向标"},
    {"symbol": "4186.T", "name": "东京应化", "industry": "3. 半导体核心先进材料", "feature": "先进EUV光刻胶全球隐形冠军，技术壁垒极高"},
    
    # --- 其他自选（你之前的JMACS也可以放在这里） ---
    {"symbol": "5817.T", "name": "JMACS", "industry": "4. 工业自动化与图像AI", "feature": "主攻AI图像识别与工业自动化控制系统"}
]

def fetch_stock_data():
    updated_list = []
    
    for item in WATCHLIST:
        symbol = item["symbol"]
        name = item["name"]
        industry = item["industry"]
        feature = item["feature"]
        
        try:
            print(f"正在抓取 {name} ({symbol})...")
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # 价格与涨跌
            current_price = info.get('currentPrice') or info.get('regularMarketPrice') or "--"
            prev_close = info.get('previousClose')
            
            if current_price != "--" and prev_close:
                diff = current_price - prev_close
                percent = (diff / prev_close) * 100
                sign = "+" if diff > 0 else ""
                change_str = f"{sign}{diff:.2f} ({sign}{percent:.2f}%)"
                is_up = diff > 0
            else:
                change_str = "--"
                is_up = False
                
            # PER 标签逻辑
            per = info.get('forwardPE') or info.get('trailingPE') or "--"
            per_display = f"{per:.2f}" if isinstance(per, (int, float)) else str(per)
            if isinstance(per, (int, float)):
                if per < 0: per_display += " (亏损)"
                elif per < 15.0: per_display += " (低估)"
                elif per < 35.0: per_display += " (合理)"
                else: per_display += " (偏高)"
                
            # PBR 标签逻辑
            pbr = info.get('priceToBook') or "--"
            pbr_display = f"{pbr:.2f}" if isinstance(pbr, (int, float)) else str(pbr)
            if isinstance(pbr, (int, float)):
                if pbr < 1.0: pbr_display += " (低估)"
                elif pbr <= 3.0: pbr_display += " (合理)"
                else: pbr_display += " (偏高)"

            updated_list.append({
                "code": symbol.split('.')[0],
                "name": name,
                "industry": industry,
                "feature": feature,
                "price": current_price,
                "change": change_str,
                "isUp": is_up,
                "per": per_display,
                "pbr": pbr_display
            })
        except Exception as e:
            print(f"{name} 抓取失败: {e}")
            
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(updated_list, f, ensure_ascii=False, indent=2)
    print("全部数据更新成功！")

if __name__ == "__main__":
    fetch_stock_data()
