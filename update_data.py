import json
import yfinance as yf
import time
import random
import os
import requests
import traceback

# Gemini 1.5 官方接口标准端点与密钥配置
END_POINT = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
SEC_VAL = os.environ.get("AI_API_KEY")

MACRO_LIST = [
    {"symbol": "^SOX", "name": "费城半导体指数"},
    {"symbol": "JPY=X", "name": "美元/日元 (汇率)"},
    {"symbol": "^N225", "name": "日经 225"},
    {"symbol": "^GSPC", "name": "标普 500"}
]

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
    {"symbol": "4063.T", "name": "信越化学 (日)", "industry": "3. 半导体核心先进材料", "feature": "全球大硅片与光刻胶绝对霸主，行业风向标"},
    {"symbol": "4186.T", "name": "东京应化 (日)", "industry": "3. 半导体核心先进材料", "feature": "先进EUV光刻胶全球隐形冠军，技术壁垒极高"},
    {"symbol": "CEG", "name": "星座能源 (美)", "industry": "4. AI核能与电力设施", "feature": "美国最大核电运营商，直接向微软数据中心独家供电"},
    {"symbol": "GE", "name": "通用电气 (美)", "industry": "4. AI核能与电力设施", "feature": "全球电网电缆与重型燃气轮机巨头，电力短缺直接受益者"},
    {"symbol": "6501.T", "name": "日立制作所 (日)", "industry": "4. AI核能与电力设施", "feature": "全球变压器与高压直流电网巨头，斩获海量海外数据中心订单"},
    {"symbol": "6503.T", "name": "三菱电机 (日)", "industry": "4. AI核能与电力设施", "feature": "重型电力设备与数据中心专属高效冷冻机核心供应商"},
    {"symbol": "QCOM", "name": "高通 (美)", "industry": "5. 边缘AI与智能终端", "feature": "移动端AI芯片霸主，统治AI手机与AI PC处理器市场"},
    {"symbol": "6758.T", "name": "索尼集团 (日)", "industry": "5. 边缘AI与智能终端", "feature": "全球图像传感器(CIS)绝对霸主，端侧机器人与智能视觉核心"},
    {"symbol": "6981.T", "name": "村田制作所 (日)", "industry": "5. 边缘AI与智能终端", "feature": "全球MLCC电容之王，AI终端硬件升级换代的刚需元器件"}
]

def make_ai_news(stock_data):
    if not SEC_VAL:
        return "💡 终端同步就绪。全球多头防御格局整体维持，AI芯片、先进材料与数据中心电网异动显著，保持跟踪。"
    
    # 筛选出有有效变动数据的个股作为AI素材
    valid_stocks = [s for s in stock_data if "nan" not in s['change']]
    if not valid_stocks:
        valid_stocks = stock_data
        
    lines = [f"{s['name']}: {s['change']}" for s in valid_stocks[:6]]
    msg = f"你是一个顶级宏观对冲基金经理，请用120字精炼复盘今日全球AI硬科技动向，语气要专业老练。数据参考：{', '.join(lines)}"
    
    try:
        hd = {"Authorization": f"Bearer {SEC_VAL}", "Content-Type": "application/json"}
        pl = {
            "model": "gemini-1.5-flash", 
            "messages": [{"role": "user", "content": msg}], 
            "temperature": 0.4
        }
        r = requests.post(END_POINT, headers=hd, json=pl, timeout=12)
        if r.status_code == 200:
            return r.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"AI 生成遇到微调跳过: {e}")
    return "💡 盘后策略：核心资产呈现机构抱团和多头防御特征，建议密切关注产业链高壁垒标的盘面结构表现。"

def fetch_all_data():
    output_data = {"macro": [], "stocks": [], "ai_report": ""}
    
    # 使用标准会话，确保不产生阻塞
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

    # 1. 抓取大盘
    for m in MACRO_LIST:
        try:
            stock = yf.Ticker(m["symbol"], session=session)
            h_df = stock.history(period="5d") # 扩大取样周期，防止周未或节假日切片越界
            if h_df.empty: continue
            
            # 双保险提取：取最后一行和倒数第二行有效数据
            current = float(h_df['Close'].iloc[-1])
            prev_close = float(h_df['Close'].iloc[-2])
            
            diff = current - prev_close
            pct = (diff / prev_close) * 100
            sign = "+" if diff > 0 else ""
            output_data["macro"].append({
                "name": m["name"], "price": f"{current:.2f}",
                "change": f"{sign}{diff:.2f} ({sign}{pct:.2f}%)", "isUp": diff > 0
            })
            time.sleep(0.2)
        except Exception as e:
            print(f"大盘 {m['name']} 抓取微调: {e}")

    # 2. 抓取自选个股
    for item in WATCHLIST:
        symbol = item["symbol"]
        try:
            print(f"正在同步决策面：{item['name']}...")
            stock = yf.Ticker(symbol, session=session)
            h_df = stock.history(period="7d") # 扩大范围确保拿到至少两日有效收盘价
            if h_df.empty or len(h_df) < 2: continue
                
            current_price = float(h_df['Close'].iloc[-1])
            prev_close = float(h_df['Close'].iloc[-2])
            diff = current_price - prev_close
            percent = (diff / prev_close) * 100
            sign = "+" if diff > 0 else ""
            
            per_display, pbr_display, dist_high_str = "--", "--", "--"
            
            try:
                info = stock.info
                if isinstance(info, dict):
                    high_52w = info.get('fiftyTwoWeekHigh')
                    if high_52w and float(high_52w) >= current_price:
                        dist_high = ((current_price - float(high_52w)) / float(high_52w)) * 100
                        dist_high_str = f"{dist_high:.1f}%"
                    per = info.get('forwardPE') or info.get('trailingPE')
                    if per and isinstance(per, (int, float)): per_display = f"{per:.2f}"
                    pbr = info.get('priceToBook')
                    if pbr and isinstance(pbr, (int, float)): pbr_display = f"{pbr:.2f}"
            except:
                pass

            ma20 = h_df['Close'].mean()
            trend_label = "牛市多头" if current_price >= ma20 else "熊市空头"

            output_data["stocks"].append({
                "code": symbol.split('.')[0] if '.' in symbol else symbol,
                "name": item["name"], "industry": item["industry"], "feature": item["feature"],
                "price": f"{current_price:.2f}", "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)", "isUp": diff > 0,
                "per": per_display, "pbr": pbr_display, "distHigh": dist_high_str, "trend": trend_label
            })
            time.sleep(random.uniform(0.3, 0.6))
        except Exception as e:
            print(f"跳过 {item['name']}: {e}")

    # 3. 实时注入 AI 简报
    print("正在召集 AI 首席复盘官编写策略简报...")
    output_data["ai_report"] = make_ai_news(output_data["stocks"])

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("🎉 全财务指标 + AI 策略简报数据流打包完成！")

if __name__ == "__main__":
    fetch_all_data()
