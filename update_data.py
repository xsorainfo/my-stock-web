import json
import yfinance as yf
import time
import random

# 宏观风向标清单
MACRO_LIST = [
    {"symbol": "^SOX", "name": "费城半导体指数"},
    {"symbol": "JPY=X", "name": "美元/日元 (汇率)"},
    {"symbol": "^N225", "name": "日经 225"},
    {"symbol": "^GSPC", "name": "标普 500"}
]

# 核心自选股清单
WATCHLIST = [
    {"symbol": "NVDA", "name": "英伟达 (美)", "industry": "1. AI半导体与核心设备", "feature": "全球AI算力GPU绝对霸主，万亿AI生态的缔造者"},
    {"symbol": "ASML", "name": "阿斯麦 (美)", "industry": "1. AI半导体与核心设备", "feature": "全球高端光刻机独家垄断者，芯片制造的物理极限"},
    {"symbol": "8035.T", "name": "东京电子 (日)", "industry": "1. AI半导体与核心设备", "feature": "全球涂布/显影设备巨头，AI芯片制造的核心支柱"},
    {"symbol": "6857.T", "name": "爱德万测试 (日)", "industry": "1. AI半导体与核心设备", "feature": "全球HBM内存测试机霸主，深度绑定英伟达产业链"},
    {"symbol": "6146.T", "name": "迪斯科 (日)", "industry": "1. AI半导体与核心设备", "feature": "垄断晶圆精密减薄切割机，AI先进封装必用设备"},
    {"symbol": "MSFT", "name": "微软 (美)", "industry": "2. AI数据中心与光缆", "feature": "全球AI云服务与应用超级巨头，OpenAI最大底座"},
    {"symbol": "5803.T", "name": "フジクラ (日)", "industry": "2. AI数据中心与光缆", "feature": "AI数据中心核心部件「高密度光缆」核心供应商"},
    {"symbol": "5801.T", "name": "古河电工 (日)", "industry": "2. AI数据中心与光缆", "feature": "下一代光电共封装(CPO)技术与光电子器件先驱"},
    {"symbol": "5802.T", "name": "住友电工 (日)", "industry": "2. AI数据中心与光缆", "feature": "全球高带宽连接器与特种光通信线缆行业龙头"},
    {"symbol": "3110.T", "name": "日東紡績 (日)", "industry": "3. 半导体核心先进材料", "feature": "全球高频半导体基板用「超薄玻璃纤维布」垄断巨头"},
    {"symbol": "4063.T", "name": "信越化学 (日)", "industry": "3. 半导体核心先进材料", "feature": "全球大硅片 wiggle 与光刻胶绝对霸主，行业风向标"},
    {"symbol": "4186.T", "name": "东京应化 (日)", "industry": "3. 半导体核心先进材料", "feature": "先进EUV光刻胶全球隐形冠军，技术壁垒极高"},
    {"symbol": "CEG", "name": "星座能源 (美)", "industry": "4. AI核能与电力设施", "feature": "美国最大核电运营商，直接向微软数据中心独家供电"},
    {"symbol": "GE", "name": "通用电气 (美)", "industry": "4. AI核能与电力设施", "feature": "全球电网电缆与重型燃气轮机巨头，电力短缺直接受益者"},
    {"symbol": "6501.T", "name": "日立制作所 (日)", "industry": "4. AI核能与电力设施", "feature": "全球变压器与高压直流电网巨头，斩获海量海外数据中心订单"},
    {"symbol": "6503.T", "name": "三菱电机 (日)", "industry": "4. AI核能与电力设施", "feature": "重型电力设备与数据中心专属高效冷冻机核心供应商"},
    {"symbol": "QCOM", "name": "高通 (美)", "industry": "5. 边缘AI与智能终端", "feature": "移动端AI芯片霸主，统治AI手机与AI PC处理器市场"},
    {"symbol": "6758.T", "name": "索尼集团 (日)", "industry": "5. 边缘AI与智能终端", "feature": "全球图像传感器(CIS)绝对霸主，端侧机器人与智能视觉核心"},
    {"symbol": "6981.T", "name": "村田制作所 (日)", "industry": "5. 边缘AI与智能终端", "feature": "全球MLCC电容之王，AI终端硬件升级换代的刚需元器件"}
]

def fetch_all_data():
    output_data = {"macro": [], "stocks": []}
    
    session = yf.utils.get_default_session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

    # 1. 抓取宏观环境数据（使用最健壮的 history 接口，弃用废弃的 fast_info）
    for m in MACRO_LIST:
        try:
            stock = yf.Ticker(m["symbol"], session=session)
            h_df = stock.history(period="2d")
            if h_df.empty:
                continue
            
            current = float(h_df['Close'].iloc[-1])
            prev_close = float(h_df['Open'].iloc[-1]) if len(h_df) < 2 else float(h_df['Close'].iloc[-2])
            
            diff = current - prev_close
            pct = (diff / prev_close) * 100
            sign = "+" if diff > 0 else ""
            
            output_data["macro"].append({
                "name": m["name"],
                "price": f"{current:.2f}",
                "change": f"{sign}{diff:.2f} ({sign}{pct:.2f}%)",
                "isUp": diff > 0
            })
            time.sleep(random.uniform(0.5, 1.2))
        except Exception as e:
            print(f"宏观数据抓取跳过 {m['name']}: {e}")

    # 2. 抓取股票核心数据
    for item in WATCHLIST:
        symbol = item["symbol"]
        try:
            print(f"正在安全扫描资产： {item['name']}...")
            stock = yf.Ticker(symbol, session=session)
            
            # 使用 20 天历史确保完美计算价格与 15 日微型折线图数组
            h_df = stock.history(period="20d")
            if h_df.empty or len(h_df) < 2:
                print(f"警告：未取到 {item['name']} 的历史价格，跳过")
                continue
                
            current_price = float(h_df['Close'].iloc[-1])
            prev_close = float(h_df['Close'].iloc[-2])
            diff = current_price - prev_close
            percent = (diff / prev_close) * 100
            sign = "+" if diff > 0 else ""
            
            # 提取 15 天迷你趋势图序列
            cl_list = h_df['Close'].tolist()[-15:]
            cl_min, cl_max = min(cl_list), max(cl_list)
            trend_norm = [int((v - cl_min)/(cl_max - cl_min)*100) if cl_max != cl_min else 50 for v in cl_list]

            # 🌟【超级防御环】：将不稳定的 info 指标提取隔离开，防止单股缺失导致全盘崩溃
            per_display = "--"
            pbr_display = "--"
            dist_high_str = "--"
            trend_label = "多头防御"
            
            try:
                info = stock.info
                if isinstance(info, dict):
                    # 52周最高及回撤计算
                    high_52w = info.get('fiftyTwoWeekHigh')
                    if high_52w and float(high_52w) >= current_price:
                        dist_high = ((current_price - float(high_52w)) / float(high_52w)) * 100
                        dist_high_str = f"{dist_high:.1f}%"
                    
                    # 估值提取
                    per = info.get('forwardPE') or info.get('trailingPE')
                    if per and isinstance(per, (int, float)):
                        per_display = f"{per:.2f}"
                        
                    pbr = info.get('priceToBook')
                    if pbr and isinstance(pbr, (int, float)):
                        pbr_display = f"{pbr:.2f}"
            except Exception as info_err:
                print(f"提示：{item['name']} 基础财务指标未完全同步 (已跳过微调): {info_err}")

            # 趋势标签判定（使用20日均线代替废弃的 ma200，既防崩溃又更具高频灵敏度）
            ma20 = h_df['Close'].mean()
            trend_label = "牛市多头" if current_price >= ma20 else "熊市空头"

            output_data["stocks"].append({
                "code": symbol.split('.')[0] if '.' in symbol else symbol,
                "name": item["name"],
                "industry": item["industry"],
                "feature": item["feature"],
                "price": f"{current_price:.2f}",
                "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)",
                "isUp": diff > 0,
                "per": per_display,
                "pbr": pbr_display,
                "distHigh": dist_high_str,
                "trend": trend_label,
                "history": trend_norm
            })
            
            # 每次运行平稳歇息，规避反爬
            time.sleep(random.uniform(0.8, 1.8))
            
        except Exception as e:
            print(f"个股核心解析重大跳过 {item['name']}: {e}")

    # 3. 稳固安全写出
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("🎉 经典全财务数据流成功离线同步构建完毕！")

if __name__ == "__main__":
    fetch_all_data()
