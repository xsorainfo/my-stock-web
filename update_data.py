import json
import yfinance as yf
import time
import random
import os
import requests
import datetime

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
        return "💡 决策终端数据同步就绪。硬科技多头动能整体维持，建议紧盯高壁垒半导体先进封装设备及核心材料的盘面异动。"
    lines = [f"{s['name']}: {s['change']}" for s in stock_data[:6]]
    msg = f"你是一个顶级对冲基金经理，请用120字精炼点评今日全球AI硬科技板块整体动向。盘面数据：{', '.join(lines)}"
    try:
        hd = {"Authorization": f"Bearer {SEC_VAL}", "Content-Type": "application/json"}
        pl = {"model": "gemini-1.5-flash", "messages": [{"role": "user", "content": msg}], "temperature": 0.4}
        r = requests.post(END_POINT, headers=hd, json=pl, timeout=10)
        if r.status_code == 200:
            return r.json()['choices'][0]['message']['content'].strip()
    except:
        pass
    return "💡 盘后复盘：全球AI硬科技资产高位震荡，算力供应链及先进先进设备材料呈现明显的机构抱团和多头防御特征。"

def run_job():
    res = {"macro": [], "stocks": [], "ai_report": ""}
    ss = yf.utils.get_default_session()
    ss.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

    # 1. 抓取大盘
    for m in MACRO_LIST:
        try:
            tk = yf.Ticker(m["symbol"], session=ss)
            h_df = tk.history(period="2d")
            if not h_df.empty:
                cur = float(h_df['Close'].iloc[-1])
                prv = float(h_df['Open'].iloc[-1]) if len(h_df) == 1 else float(h_df['Close'].iloc[-2])
                df = cur - prv
                pc = (df / prv) * 100
                res["macro"].append({
                    "name": m["name"], "price": f"{cur:.2f}",
                    "change": f"{'+' if df>0 else ''}{df:.2f} ({'+' if df>0 else ''}{pc:.2f}%)", "isUp": df > 0
                })
        except:
            pass

    # 2. 抓取个股（不看任何详情和历史，只要最近两天的收盘价计算涨跌）
    for item in WATCHLIST:
        sb = item["symbol"]
        try:
            tk = yf.Ticker(sb, session=ss)
            h_df = tk.history(period="5d") # 抓5天确保跨越周末
            if h_df.empty or len(h_df) < 2:
                continue
                
            cur = float(h_df['Close'].iloc[-1])
            prv = float(h_df['Close'].iloc[-2])
            df = cur - prv
            pc = (df / prv) * 100

            res["stocks"].append({
                "code": sb.split('.')[0], 
                "symbol": sb, # 留给前端拼接K线链接使用
                "name": item["name"], 
                "industry": item["industry"], 
                "feature": item["feature"],
                "price": f"{cur:.2f}", 
                "change": f"{'+' if df>0 else ''}{df:.2f} ({'+' if df>0 else ''}{pc:.2f}%)", 
                "isUp": df > 0
            })
            time.sleep(0.2)
        except Exception as e:
            print(f"跳过 {sb}: {e}")

    # 3. 生成大模型快报
    res["ai_report"] = make_ai_news(res["stocks"])

    # 4. 稳妥写入
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("极简盘面数据同步成功！")

if __name__ == "__main__":
    run_job()
