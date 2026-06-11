import json
import yfinance as yf
import time
import random
import os

WATCHLIST = [
    # 1. AI半导体与核心设备
    {"symbol": "NVDA", "name": "英伟达 (美)", "industry": "1. AI半导体与核心设备", "subCategory": "GPU与计算平台", "feature": "全球AI算力GPU绝对霸主，万亿AI生态缔造者"},
    {"symbol": "ASML", "name": "阿斯麦 (美)", "industry": "1. AI半导体与核心设备", "subCategory": "晶圆制造设备", "feature": "全球高端光刻机独家垄断者，芯片制造的物理极限"},
    {"symbol": "8035.T", "name": "东京电子 (日)", "industry": "1. AI半导体与核心设备", "subCategory": "晶圆制造设备", "feature": "全球涂布/显影设备巨头，AI芯片制造的核心支柱"},
    {"symbol": "6857.T", "name": "爱德万测试 (日)", "industry": "1. AI半导体与核心设备", "subCategory": "测试与封装", "feature": "全球HBM内存测试机霸主，深度绑定英伟达产业链"},
    {"symbol": "6146.T", "name": "迪斯科 (日)", "industry": "1. AI半导体与核心设备", "subCategory": "测试与封装", "feature": "垄断晶圆精密减薄切割机，AI先进封装必用设备"},
    
    # 2. AI数据中心与光缆
    {"symbol": "MSFT", "name": "微软 (美)", "industry": "2. AI数据中心与光缆", "subCategory": "云服务与算力", "feature": "全球AI云服务与应用超级巨头，OpenAI最大底座"},
    {"symbol": "5803.T", "name": "フジクラ (日)", "industry": "2. AI数据中心与光缆", "subCategory": "光通信与连接", "feature": "AI数据中心核心部件「高密度光缆」核心供应商"},
    {"symbol": "5801.T", "name": "古河电工 (日)", "industry": "2. AI数据中心与光缆", "subCategory": "光通信与连接", "feature": "下一代光电共封装(CPO)技术与光电子器件先驱"},
    {"symbol": "5802.T", "name": "住友电工 (日)", "industry": "2. AI数据中心与光缆", "subCategory": "光通信与连接", "feature": "全球高带宽连接器与特种光通信线缆行业龙头"},
    
    # 3. 半导体核心先进材料
    {"symbol": "3110.T", "name": "日東紡績 (日)", "industry": "3. 半导体核心先进材料", "subCategory": "基板与薄膜材料", "feature": "全球高频半导体基板用「超薄玻璃纤维布」垄断巨头"},
    {"symbol": "4063.T", "name": "信越化学 (日)", "industry": "3. 半导体核心先进材料", "subCategory": "基板与晶圆材料", "feature": "全球大硅片与光刻胶绝对霸主，行业风向标"},
    {"symbol": "4186.T", "name": "东京应化 (日)", "industry": "3. 半导体核心先进材料", "subCategory": "光刻材料", "feature": "先进EUV光刻胶全球隐形冠军，技术壁垒极高"},
    
    # 4. AI核能与电力设施
    {"symbol": "CEG", "name": "星座能源 (美)", "industry": "4. AI核能与电力设施", "subCategory": "核能与能源供给", "feature": "美国最大核电运营商，直接向微软数据中心供电"},
    {"symbol": "GE", "name": "通用电气 (美)", "industry": "4. AI核能与电力设施", "subCategory": "电力传输设备", "feature": "全球电网电缆与重型燃气轮机巨头"},
    {"symbol": "6501.T", "name": "日立制作所 (日)", "industry": "4. AI核能与电力设施", "subCategory": "电力传输设备", "feature": "全球变压器与高压直流电网巨头"},
    {"symbol": "6503.T", "name": "三菱电机 (日)", "industry": "4. AI核能与电力设施", "subCategory": "温控与电力", "feature": "数据中心专属高效冷冻机核心供应商"},
    
    # 5. 边缘AI与智能终端
    {"symbol": "QCOM", "name": "高通 (美)", "industry": "5. 边缘AI与智能终端", "subCategory": "终端芯片", "feature": "移动端AI芯片霸主，统治AI手机与AI PC市场"},
    {"symbol": "6758.T", "name": "索尼集团 (日)", "industry": "5. 边缘AI与智能终端", "subCategory": "传感器与视觉", "feature": "全球图像传感器(CIS)绝对霸主，端侧机器人核心"},
    {"symbol": "6981.T", "name": "村田制作所 (日)", "industry": "5. 边缘AI与智能终端", "subCategory": "被动元器件", "feature": "全球MLCC电容之王，AI终端硬件升级换代刚需"}
]

# ... (fetch_all_data 函数内的逻辑保持不变，只需确保 append 时包含 subCategory)

# 在 fetch_all_data 的 for 循环中修改这行：
def fetch_all_data():
    # ... 省略中间代码 ...
    for item in WATCHLIST:
        # ... 数据抓取逻辑 ...
        output_data["stocks"].append({
            "code": symbol.split('.')[0] if '.' in symbol else symbol,
            "name": item["name"],
            "industry": item["industry"],
            "subCategory": item["subCategory"], # <--- 必须保留此行
            "feature": item["feature"],
            "price": f"{current_price:.2f}",
            "change": f"{sign}{diff:.2f} ({sign}{percent:.2f}%)",
            "isUp": diff > 0,
            "per": per_display,
            "pbr": pbr_display,
            "distHigh": dist_high_str,
            "distWeek": dist_week_str,
            "distMonth": dist_month_str,
            "trend": trend_label
        })
    # ... 其余保持不变
