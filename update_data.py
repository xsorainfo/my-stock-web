import json
import yfinance as yf
import time
import random
import os
import requests



# 如果用 Gemini，请把顶部的两个配置改成这样：
AI_API_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
# 模型的名字建议用速度飞快且免费的 flash
payload = {
    "model": "gemini-1.5-flash", 
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3
}

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

def generate_ai_report(macro_data, stock_data):
    """把今天的数据打包塞给大模型，让大模型生成犀利的首席简报"""
    if not AI_KEY:
        return "⚠️ AI_API_KEY 未配置，无法生成盘后智能简报。"
    
    # 将今日的异动股票进行简单文字罗列
    stock_summary = []
    for s in stock_data:
        stock_summary.append(f"{s['name']}({s['code']}): 涨跌幅 {s['change']}, 趋势:{s['trend']}, 距新高:{s['distHigh']}")
    
    prompt = f"""
    你是一位顶级的对冲基金宏观策略师，说话一针见血、逻辑严密。请根据今天最新的美日AI产业链市况数据，为我生成一份300字以内的【盘后首席指引】。
    
    【今日宏观天气】：{json.dumps(macro_data, ensure_ascii=False)}
    【核心个股异动】：{', '.join(stock_summary[:10])} （仅展示部分核心）
    
    要求：
    1. 不要讲废话。直接指出今天哪个题材（如：半导体设备、数据中心电力、先进材料）表现最强或遭遇危机。
    2. 结合美元日元汇率，用极度精炼的语言给出一个明天盯着哪个方向的交易建议。
    3. 语言要专业、犀利、充满洞察力。
    """
    
    try:
        headers = {"Authorization": f"Bearer {AI_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-chat", # 根据你的AI型号换名字，比如 gemini-1.5-flash 等
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        response = requests.post(AI_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return f"AI 秘书今天罢工了，错误码: {response.status_code}"
    except Exception as e:
        return f"召唤 AI 策略师失败: {str(e)}"

def fetch_all_data():
    output_data = {"macro": [], "stocks": [], "ai_report": "暂无今日简报"}
    session = yf.utils.get_default_session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})

    # 1. 抓取宏观环境数据
    for m in MACRO_LIST:
        try:
            stock = yf.Ticker(m["symbol"], session=session)
            fast = stock.fast_info
            current = fast.last_price
            prev_close = fast.previous_close
            diff = current - prev_close
            pct = (diff / prev_close) * 100
            sign = "+" if diff > 0 else ""
            output_data["macro"].append({
                "name": m["name"],
                "price": f"{current:.2f}",
                "change": f"{sign}{diff:.2f} ({sign}{pct:.2f}%)",
                "isUp": diff > 0
            })
            time.sleep(random.uniform(0.3, 1.0))
        except:
            pass

    # 2. 抓取股票数据 + 历史30天趋势图数据
    for item in WATCHLIST:
        symbol = item["symbol"]
        try:
            print(f"正在高频安全扫描及提取历史K线: {item['name']}...")
            stock = yf.Ticker(symbol, session=session)
            info = stock.info
            fast = stock.fast_info
            
            current_price = fast.last_price
            prev_close = fast.previous_close
            diff = current_price - prev_close
            percent = (diff / prev_close) * 100
            sign = "+" if diff > 0 else ""
            
            # --- 核心：提取过去30天的历史价格列表用来画小趋势图 ---
            hist = stock.history(period="1mo")
            history_prices = []
            if not hist.empty:
                # 提取最近20-22个交易日的收盘价，保留2位小数
                history_prices = [round(float(p), 2) for p in hist['Close'].tolist()]

            high_52w = info.get('fiftyTwoWeekHigh')
            dist_high_str = f"{((current_price - high_52w) / high_52w) * 100:.1f}%" if high_52w else "--"
            ma200 = fast.get('twoHundredDayAverage') or info.get('twoHundredDayAverage')
            trend_label = "牛市多头" if ma200 and current_price > ma200 else ("熊市左侧" if ma200 else "趋势未知")

            per = info.get('forwardPE') or info.get('trailingPE') or "--"
            per_display = f"{per:.2f}" if isinstance(per, (int, float)) else str(per)
            pbr = info.get('priceToBook') or "--"
            pbr_display = f"{pbr:.2f}" if isinstance(pbr, (int, float)) else str(pbr)

            output_data["stocks"].append({
                "code": symbol.split('.')[0] if '.' in symbol else symbol,
                "name": item["name"],
                "industry": item["industry"],
                "feature": item["feature"],
                "price": f"{current_price:.2f}" if isinstance(current_price, (int,float)) else str(current_price),
                "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)",
                "isUp": diff > 0,
                "per": per_display,
                "pbr": pbr_display,
                "distHigh": dist_high_str,
                "trend": trend_label,
                "history": history_prices # 把这串历史价格数组塞进数据包里！
            })
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            print(f"失败: {e}")

    # 3. 核心：在收盘或者刷数据时，顺便生成AI深度复盘
    print("正在连线云端 AI 策略师生成今日复盘简报...")
    output_data["ai_report"] = generate_ai_report(output_data["macro"], output_data["stocks"])

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print("全部多维决策数据更新完毕！")

if __name__ == "__main__":
    fetch_all_data()
