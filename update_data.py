import json
import yfinance as yf

# 1. 全球硬科技顶级自选股清单（涵盖美股龙头与四大核心热门题材）
WATCHLIST = [
    # === 1. AI半导体与核心设备（全球算力总龙头） ===
    {"symbol": "NVDA", "name": "英伟达 (美)", "industry": "1. AI半导体与核心设备", "feature": "全球AI算力GPU绝对霸主，万亿AI生态的缔造者"},
    {"symbol": "ASML", "name": "阿斯麦 (美)", "industry": "1. AI半导体与核心设备", "feature": "全球高端光刻机独家垄断者，芯片制造的物理极限"},
    {"symbol": "8035.T", "name": "东京电子 (日)", "industry": "1. AI半导体与核心设备", "feature": "全球涂布/显影设备巨头，AI芯片制造的核心支柱"},
    {"symbol": "6857.T", "name": "爱德万测试 (日)", "industry": "1. AI半导体与核心设备", "feature": "全球HBM内存测试机霸主，深度绑定英伟达产业链"},
    {"symbol": "6146.T", "name": "迪斯科 (日)", "industry": "1. AI半导体与核心设备", "feature": "垄断晶圆精密减薄切割机，AI先进封装必用设备"},
    
    # === 2. AI数据中心与光缆（算力大动脉） ===
    {"symbol": "MSFT", "name": "微软 (美)", "industry": "2. AI数据中心与光缆", "feature": "全球AI云服务与应用超级巨头，OpenAI最大底座"},
    {"symbol": "5803.T", "name": "フジクラ (日)", "industry": "2. AI数据中心与光缆", "feature": "AI数据中心核心部件「高密度光缆」核心供应商"},
    {"symbol": "5801.T", "name": "古河电工 (日)", "industry": "2. AI数据中心与光缆", "feature": "下一代光电共封装(CPO)技术与光电子器件先驱"},
    {"symbol": "5802.T", "name": "住友电工 (日)", "industry": "2. AI数据中心与光缆", "feature": "全球高带宽连接器与特种光通信线缆行业龙头"},
    
    # === 3. 半导体核心先进材料（硬科技隐形冠军） ===
    {"symbol": "3110.T", "name": "日東紡績 (日)", "industry": "3. 半导体核心先进材料", "feature": "全球高频半导体基板用「超薄玻璃纤维布」垄断巨头"},
    {"symbol": "4063.T", "name": "信越化学 (日)", "industry": "3. 半导体核心先进材料", "feature": "全球大硅片与光刻胶绝对霸主，行业风向标"},
    {"symbol": "4186.T", "name": "东京应化 (日)", "industry": "3. 半导体核心先进材料", "feature": "先进EUV光刻胶全球隐形冠军，技术壁垒极高"},
    
    # === 4. 🔥 热门题材：AI核能与能源基础设施（AI的尽头是电力） ===
    {"symbol": "CEG", "name": "星座能源 (美)", "industry": "4. AI核能与电力设施", "feature": "美国最大核电运营商，直接向微软数据中心独家供电"},
    {"symbol": "GE", "name": "通用电气 (美)", "industry": "4. AI核能与电力设施", "feature": "全球电网电缆与重型燃气轮机巨头，电力短缺直接受益者"},
    {"symbol": "6501.T", "name": "日立制作所 (日)", "industry": "4. AI核能与电力设施", "feature": "全球变压器与高压直流电网巨头，斩获海量海外数据中心订单"},
    {"symbol": "6503.T", "name": "三菱电机 (日)", "industry": "4. AI核能与电力设施", "feature": "重型电力设备与数据中心专属高效冷冻机核心供应商"},

    # === 5. 🔥 热门题材：边缘AI与智能终端（端侧AI爆发） ===
    {"symbol": "QCOM", "name": "高通 (美)", "industry": "5. 边缘AI与智能终端", "feature": "移动端AI芯片霸主，统治AI手机与AI PC处理器市场"},
    {"symbol": "6758.T", "name": "索尼集团 (日)", "industry": "5. 边缘AI与智能终端", "feature": "全球图像传感器(CIS)绝对霸主，端侧机器人与智能视觉核心"},
    {"symbol": "6981.T", "name": "村田制作所 (日)", "industry": "5. 边缘AI与智能终端", "feature": "全球MLCC电容之王，AI终端硬件升级换代的刚需元器件"}
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
                "code": symbol.split('.')[0] if '.' in symbol else symbol, # 美股直接显示代号
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
