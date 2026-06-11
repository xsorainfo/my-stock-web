import json
import yfinance as yf
import time
import random
import os
import requests

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
    {"symbol": "6146.T", "name": "迪斯科 (日)", "industry": "1. AI半导体与核心设备", "feature": "垄an晶圆精密减薄切割机，AI先进封装必用设备"},
    {"symbol": "MSFT", "name": "微软 (美)", "industry": "2. AI数据中心与光缆", "feature": "全球AI云服务与应用超级巨头，OpenAI最大底座"},
    {"symbol": "5803.T", "name": "フジクラ (日)", "industry": "2. AI数据中心与光缆", "feature": "AI数据中心核心部件「高密度光缆」核心供应商"},
    {"symbol": "5801.T", "name": "古河电工 (日)", "industry": "2. AI数据中心与光缆", "feature": "下一代光电共封装(CPO)技术与光电子器件先驱"},
    {"symbol": "5802.T", "name": "住友电工 (日)", "industry": "2. AI数据中心与光缆", "feature": "全球高带宽连接器与特种光通信线缆行业龙头"},
    {"symbol": "3110.T", "name": "日東紡績 (日)", "industry": "3. 半导体核心先进材料", "feature": "全球高频半导体基板用「超薄玻璃纤维布」垄an巨头"},
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
        return "💡 终端同步就绪。全球多头防御格局整体维持，保持结构性跟踪。"
    
    # 1. 先尝试获取可用模型列表 (ListModels)
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={SEC_VAL}"
    try:
        r_list = requests.get(list_url, timeout=10)
        if r_list.status_code == 200:
            models = [m['name'] for m in r_list.json().get('models', [])]
            # 自动挑选一个支持 generateContent 的模型
            target_model = next((m for m in models if "gemini" in m and "1.5" in m), "models/gemini-1.5-flash")
            print(f"终端探测：检测到可用模型 -> {target_model}")
        else:
            target_model = "models/gemini-1.5-flash"
    except:
        target_model = "models/gemini-1.5-flash"

    # 2. 使用探测到的模型进行调用
    msg = f"顶级基金经理，请用100字精简复盘这些资产：{stock_data[:5]}。从多头防御、估值消化视角切入，指出核心标的是抱团还是黄金坑。"
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={SEC_VAL}"
    
    try:
        payload = {"contents": [{"parts": [{"text": msg}]}]}
        r = requests.post(gen_url, json=payload, timeout=15)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            print(f"❌ 最终调用失败: {r.text}")
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    return "💡 盘后多头思维：核心资产高位震荡消化 TTM 估值，部分上游垄断材料回撤提供中线左侧安全边际，保持结构性买入防御。"


    
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
