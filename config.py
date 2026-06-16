# config.py
DEFAULT_STRATEGY = ["yfinance"]

# 只有需要特殊处理的标的才写在这里
SOURCE_MAP = {
    "NVDA": ["yfinance", "alphavantage"],  # 美股对比源
    "3110.T": ["yfinance"]                 # 日股目前只用 yfinance
}

MACRO_LIST = [
    {"symbol": "^SOX", "name": "费城半导体指数"},
    {"symbol": "JPY=X", "name": "美元/日元 (汇率)"},
    {"symbol": "^N225", "name": "日经 225"},
    {"symbol": "^GSPC", "name": "标普 500"}
]

WATCHLIST = [
    # 1. AI半导体与核心设备
    {"symbol": "NVDA", "name": "英伟达 (美)", "industry": "1. AI半导体与核心设备", "feature": "全球AI算力GPU绝对霸主，万亿AI生态的缔造者"},
    {"symbol": "ASML", "name": "阿斯麦 (美)", "industry": "1. AI半导体与核心设备", "feature": "全球高端光刻机独家垄断者，芯片制造的物理极限"},
    {"symbol": "8035.T", "name": "东京电子 (東京エレクトロン - 日)", "industry": "1. AI半导体与核心设备", "feature": "全球涂布/显影设备巨头，AI芯片制造的核心支柱"},
    {"symbol": "6857.T", "name": "爱德万测试 (アドバンテスト - 日)", "industry": "1. AI半导体与核心设备", "feature": "全球HBM内存测试机霸主，深度绑定英伟达产业链"},
    {"symbol": "6146.T", "name": "迪斯科 (ディスコ - 日)", "industry": "1. AI半导体与核心设备", "feature": "垄断晶圆精密减薄切割机，AI先进封装必用设备"},
    {"symbol": "6920.T", "name": "激光技术 (レーザーテック - 日)", "industry": "1. AI半导体与核心设备", "feature": "**EUV光罩检测**设备全球独家，技术壁垒极高"},
    {"symbol": "6525.T", "name": "KOKUSAI ELECTRIC (KOKUSAI ELECTRIC - 日)", "industry": "1. AI半导体与核心设备", "feature": "半导体**薄膜沉积设备**关键厂商"},
    {"symbol": "6723.T", "name": "瑞萨电子 (ルネサスエレクトロニクス - 日)", "industry": "1. AI半导体与核心设备", "feature": "车载/工业MCU与模拟芯片主力"},
    {"symbol": "7735.T", "name": "SCREEN控股 (SCREENホールディングス - 日)", "industry": "1. AI半导体与核心设备", "feature": "**晶圆清洗**设备全球领先"},
    {"symbol": "6526.T", "name": "Socionext (ソシオネクスト - 日)", "industry": "1. AI半导体与核心设备", "feature": "定制化SoC设计与先进制程方案"},
    {"symbol": "6871.T", "name": "日本微米尼克斯 (日本マイクロニクス - 日)", "industry": "1. AI半导体与核心设备", "feature": "晶圆探针测试设备厂商"},
    {"symbol": "6963.T", "name": "罗姆 (ローム - 日)", "industry": "1. AI半导体与核心设备", "feature": "功率半导体(SiC)技术核心供应商"},
    {"symbol": "6890.T", "name": "FERROTEC (フェローテック - 日)", "industry": "1. AI半导体与核心设备", "feature": "半导体真空密封与石英制品核心供应商"},
    {"symbol": "6590.T", "name": "芝浦机电 (芝浦メカトロニクス - 日)", "industry": "1. AI半导体与核心设备", "feature": "先进封装与晶圆处理制造设备"},
    {"symbol": "6855.T", "name": "日本电子材料 (日本電子材料 - 日)", "industry": "1. AI半导体与核心设备", "feature": "半导体晶圆测试探针卡专业厂"},
    {"symbol": "6754.T", "name": "安立 (アンリツ - 日)", "industry": "1. AI半导体与核心设备", "feature": "高速数字通信与射频测试测量仪器"},

    # 2. AI数据中心与光缆
    {"symbol": "MSFT", "name": "微软 (美)", "industry": "2. AI数据中心与光缆", "feature": "全球AI云服务与应用超级巨头，OpenAI最大底座"},
    {"symbol": "5803.T", "name": "藤仓 (フジクラ - 日)", "industry": "2. AI数据中心与光缆", "feature": "AI数据中心核心部件「高密度光缆」核心供应商"},
    {"symbol": "5801.T", "name": "古河电工 (古河電工 - 日)", "industry": "2. AI数据中心与光缆", "feature": "下一代光电共封装(CPO)技术与光电子器件先驱"},
    {"symbol": "5802.T", "name": "住友电工 (住友電工 - 日)", "industry": "2. AI数据中心与光缆", "feature": "全球高带宽连接器与特种光通信线缆行业龙头"},
    {"symbol": "6834.T", "name": "精工技研 (精工技研 - 日)", "industry": "2. AI数据中心与光缆", "feature": "精密光连接器与光学组件供应商"},
    {"symbol": "6777.T", "name": "santec (santec Holdings - 日)", "industry": "2. AI数据中心与光缆", "feature": "光学测量系统与光通信组件先驱"},

    # 3. 半导体核心先进材料
    {"symbol": "3110.T", "name": "日东纺绩 (日東紡績 - 日)", "industry": "3. 半导体核心先进材料", "feature": "全球高频半导体基板用「超薄玻璃纤维布」垄断巨头"},
    {"symbol": "4063.T", "name": "信越化学 (信越化学工業 - 日)", "industry": "3. 半导体核心先进材料", "feature": "全球大硅片与光刻胶绝对霸主，行业风向标"},
    {"symbol": "4186.T", "name": "东京应化 (東京応化工業 - 日)", "industry": "3. 半导体核心先进材料", "feature": "先进EUV光刻胶全球隐形冠军，技术壁垒极高"},
    {"symbol": "4062.T", "name": "揖斐电 (イビデン - 日)", "industry": "3. 半导体核心先进材料", "feature": "高端IC封装基板核心供应商"},
    {"symbol": "6971.T", "name": "京瓷 (京セラ - 日)", "industry": "3. 半导体核心先进材料", "feature": "半导体封装与陶瓷元器件制造"},

    # 4. AI核能与电力设施
    {"symbol": "CEG", "name": "星座能源 (美)", "industry": "4. AI核能与电力设施", "feature": "美国最大核电运营商，直接向微软数据中心独家供电"},
    {"symbol": "GE", "name": "通用电气 (美)", "industry": "4. AI核能与电力设施", "feature": "全球电网电缆与重型燃气轮机巨头，电力短缺直接受益者"},
    {"symbol": "6501.T", "name": "日立制作所 (日立製作所 - 日)", "industry": "4. AI核能与电力设施", "feature": "全球变压器与高压直流电网巨头，斩获海量海外数据中心订单"},
    {"symbol": "6503.T", "name": "三菱电机 (三菱電機 - 日)", "industry": "4. AI核能与电力设施", "feature": "重型电力设备与数据中心专属高效冷冻机核心供应商"},
    {"symbol": "485A.T", "name": "PowerX (パワーエックス - 日)", "industry": "4. AI核能与电力设施", "feature": "新型储能电池系统与绿色能源管理"},
    {"symbol": "6504.T", "name": "富士电机 (富士電機 - 日)", "industry": "4. AI核能与电力设施", "feature": "电力电子设备与能源基础设施专家"},
    {"symbol": "6996.T", "name": "尼吉康 (ニチコン - 日)", "industry": "4. AI核能与电力设施", "feature": "铝电解电容器与储能/充电系统巨头"},

    # 5. 边缘AI与智能终端及其他
    {"symbol": "QCOM", "name": "高通 (美)", "industry": "5. 边缘AI与智能终端", "feature": "移动端AI芯片霸主，统治AI手机与AI PC处理器市场"},
    {"symbol": "6758.T", "name": "索尼集团 (ソニーグループ - 日)", "industry": "5. 边缘AI与智能终端", "feature": "全球图像传感器(CIS)绝对霸主，端侧机器人与智能视觉核心"},
    {"symbol": "6981.T", "name": "村田制作所 (村田製作所 - 日)", "industry": "5. 边缘AI与智能终端", "feature": "全球**MLCC**电容之王，AI终端硬件升级换代的刚需元器件"},
    {"symbol": "285A.T", "name": "铠侠控股 (キオクシアホールディングス - 日)", "industry": "5. 边缘AI与智能终端", "feature": "全球存储芯片核心供应商"},
    {"symbol": "6976.T", "name": "太阳诱电 (太陽誘電 - 日)", "industry": "5. 边缘AI与智能终端", "feature": "高性能电子元器件与陶瓷电容重要厂商"},
    {"symbol": "6762.T", "name": "TDK (TDK - 日)", "industry": "5. 边缘AI与智能终端", "feature": "全球被动元器件与传感器巨头"},
    {"symbol": "6752.T", "name": "松下控股 (パナソニック ホールディングス - 日)", "industry": "5. 边缘AI与智能终端", "feature": "电池技术与工业解决方案巨头"},
    {"symbol": "6701.T", "name": "日本电气 (日本電気 - 日)", "industry": "5. 边缘AI与智能终端", "feature": "AI系统集成与算力基础设施服务"},
    {"symbol": "6702.T", "name": "富士通 (富士通 - 日)", "industry": "5. 边缘AI与智能终端", "feature": "高性能AI计算与软件服务供应商"},
    {"symbol": "6613.T", "name": "QD激光 (QDレーザ - 日)", "industry": "5. 边缘AI与智能终端", "feature": "半导体激光器与光子学技术先驱"},
    {"symbol": "6965.T", "name": "滨松光子 (浜松ホトニクス - 日)", "industry": "5. 边缘AI与智能终端", "feature": "高性能光学传感器与光探测设备"},
    {"symbol": "6779.T", "name": "日本电波工业 (日本電波工業 - 日)", "industry": "5. 边缘AI与智能终端", "feature": "频率控制元器件全球核心厂商"},
    {"symbol": "6787.T", "name": "MEIKO (メイコー - 日)", "industry": "5. 边缘AI与智能终端", "feature": "高端印制电路板(PCB)专业制造"},
    {"symbol": "6479.T", "name": "美蓓亚三美 (ミネベアミツミ - 日)", "industry": "5. 边缘AI与智能终端", "feature": "高精密零部件与电机驱动技术"},
    {"symbol": "7751.T", "name": "佳能 (キヤノン - 日)", "industry": "5. 边缘AI与智能终端", "feature": "纳米压印光刻技术(NIL)探索者"},
    {"symbol": "6740.T", "name": "日本显示器 (ジャパンディスプレイ - 日)", "industry": "5. 边缘AI与智能终端", "feature": "高端车载与中小型显示面板供应"},
    {"symbol": "6997.T", "name": "日本化工 (日本ケミコン - 日)", "industry": "5. 边缘AI与智能终端", "feature": "高性能铝电解电容器行业领导者"},
    {"symbol": "6861.T", "name": "基恩士 (キーエンス - 日)", "industry": "6. 工业自动化与检测", "feature": "全球高精度传感器与机器视觉系统龙头"},
    {"symbol": "6954.T", "name": "发那科 (ファナック - 日)", "industry": "6. 工业自动化与检测", "feature": "全球工厂自动化机器人核心"},
    {"symbol": "6506.T", "name": "安川电机 (安川電機 - 日)", "industry": "6. 工业自动化与检测", "feature": "伺服电机与运动控制行业领跑者"},
    {"symbol": "6645.T", "name": "欧姆龙 (オムロン - 日)", "industry": "6. 工业自动化与检测", "feature": "工业传感控制与自动化解决方案"},
    {"symbol": "6594.T", "name": "尼得科 (ニデック - 日)", "industry": "6. 工业自动化与检测", "feature": "全球电机与驱动控制技术龙头"}
]
