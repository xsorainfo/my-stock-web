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
    # ============================================================
    # 1. 算力芯片+先进封装+存储 (Compute, HBM, Packaging)
    # ============================================================
    # --- 美股 ---
    {"symbol": "NVDA", "name": "NVIDIA(英伟达)", "market": "美股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "全球AI算力芯片霸主"},
    {"symbol": "AMD", "name": "AMD(超威半导体)", "market": "美股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "GPU算力第二极"},
    {"symbol": "ASML", "name": "ASML(阿斯麦)", "market": "美股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "全球EUV光刻机垄断者"},
    {"symbol": "QCOM", "name": "高通", "market": "美股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "AI手机与AI PC处理器龙头"},
    
    # --- A股 ---
    {"symbol": "600584.SH", "name": "长电科技", "market": "A股", "sector": "1. 算力芯片+先进封装+存储", "industry": "封测/封装", "feature": "中国先进封装制造核心"},
    {"symbol": "002049.SZ", "name": "紫光国微", "market": "A股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "核心芯片研发"},
    
    # --- 日股 ---
    {"symbol": "8035.T", "name": "東京エレクトロン(东京电子)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "AI芯片制造设备"},
    {"symbol": "6857.T", "name": "アドバンテスト(爱德万测试)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "HBM测试机霸主"},
    {"symbol": "4063.T", "name": "信越化学", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "半导体材料霸主"},
    {"symbol": "3110.T", "name": "日東紡績", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "基板材料核心供应商"},
    {"symbol": "6920.T", "name": "レーザーテック(激光技术)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "EUV检测独家"},
    {"symbol": "6146.T", "name": "ディスコ(迪斯科)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "先进封装切割设备"},
    {"symbol": "4186.T", "name": "東京応化", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "高端光刻胶冠军"},
    {"symbol": "4062.T", "name": "イビデン(揖斐电)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "封测/封装", "feature": "数据中心级基板"},
    {"symbol": "6971.T", "name": "京セラ(京瓷)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "封测/封装", "feature": "陶瓷元器件制造"},
    {"symbol": "6315.T", "name": "TOWA", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "压缩成型封装"},
    {"symbol": "6963.T", "name": "ローム(罗姆)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "SiC功率模块"},
    {"symbol": "6525.T", "name": "KOKUSAI ELECTRIC", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "半导体成膜设备核心厂商"},
    {"symbol": "6723.T", "name": "ルネサス(瑞萨电子)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "车载与工业芯片龙头"},
    {"symbol": "7735.T", "name": "SCREENホールディングス", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "全球晶圆清洗设备领先厂商"},
    {"symbol": "6526.T", "name": "ソシオネクスト(Socionext)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "先进制程SoC设计"},
    {"symbol": "6871.T", "name": "日本マイクロニクス(日本微米尼克斯)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "晶圆测试探针卡厂商"},
    {"symbol": "6890.T", "name": "FERROTEC", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "真空密封与石英制品"},
    {"symbol": "6590.T", "name": "芝浦メカトロニクス(芝浦机电)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "晶圆处理与封装设备"},
    {"symbol": "6855.T", "name": "日本電子材料", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "半导体测试探针卡专业厂"},
    {"symbol": "6754.T", "name": "アンリツ(安立)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "高速通信测试设备"},
    {"symbol": "285A.T", "name": "キオクシア(铠侠)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "存储/HBM", "feature": "全球闪存厂商"},
    {"symbol": "6976.T", "name": "太陽誘電", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "存储/HBM", "feature": "高性能电子元件"},
    {"symbol": "6752.T", "name": "パナソニック(松下)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "工业电池与电子方案"},
    {"symbol": "6701.T", "name": "NEC(日本电气)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "AI系统与网络基础设施"},
    {"symbol": "6702.T", "name": "富士通", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "高性能计算与企业AI"},
    {"symbol": "6965.T", "name": "浜松ホトニクス(浜松光子)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "光传感器与光探测设备"},
    {"symbol": "6779.T", "name": "日本電波工業", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "频率控制元件龙头"},
    {"symbol": "6787.T", "name": "メイコー(MEIKO)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "封测/封装", "feature": "高端印刷电路板制造商"},
    {"symbol": "6479.T", "name": "ミネベアミツミ(美蓓亚三美)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "轴承与精密电机龙头"},
    {"symbol": "7751.T", "name": "キヤノン(佳能)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "纳米压印光刻技术布局"},
    {"symbol": "6740.T", "name": "ジャパンディスプレイ(日本显示器)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI芯片/算力", "feature": "车载与中小尺寸显示"},
    {"symbol": "6997.T", "name": "日本ケミコン(日本化工)", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体设备/材料", "feature": "铝电解电容龙头"},

    # ============================================================
    # 2. 工业自动化与机器人 (Factory Automation)
    # ============================================================
    # --- 美股 ---
    {"symbol": "ROK", "name": "罗克韦尔自动化", "market": "美股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "工业自动化集成方案"},
    
    # --- A股 ---
    {"symbol": "688037.SH", "name": "埃斯顿", "market": "A股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "中国工业机器人龙头"},
    {"symbol": "002008.SZ", "name": "大族激光", "market": "A股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "精密制造与激光自动化"},
    
    # --- 日股 ---
    {"symbol": "6861.T", "name": "キーエンス(基恩士)", "market": "日股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "高精度传感系统"},
    {"symbol": "6954.T", "name": "ファナック(发那科)", "market": "日股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "自动化机器人核心"},
    {"symbol": "6273.T", "name": "SMC", "market": "日股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "全球气动元件霸主"},
    {"symbol": "6324.T", "name": "ハーモニック(Harmonic)", "market": "日股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "精密减速器标杆"},
    {"symbol": "6506.T", "name": "安川電機", "market": "日股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "电机与运动控制"},
    {"symbol": "6594.T", "name": "ニデック(尼得科)", "market": "日股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "电机驱动技术龙头"},
    {"symbol": "6645.T", "name": "オムロン(欧姆龙)", "market": "日股", "sector": "2. 工业自动化与机器人", "industry": "工业自动化", "feature": "工业自动化方案"},

    # ============================================================
    # 3. 高速通信与数据中心基础设施 (Optics, CPO, Power, Data Center)
    # ============================================================
    # --- 美股 ---
    {"symbol": "MSFT", "name": "微软", "market": "美股", "sector": "3. 高速通信与数据中心", "industry": "云计算/AI底座", "feature": "全球最大的云与AI基础设施"},
    {"symbol": "CEG", "name": "星座能源", "market": "美股", "sector": "3. 高速通信与数据中心", "industry": "能源/电力", "feature": "AI数据中心核电直供"},
    
    # --- A股 ---
    {"symbol": "300308.SZ", "name": "中际旭创", "market": "A股", "sector": "3. 高速通信与数据中心", "industry": "光通信/CPO", "feature": "全球高端光模块龙头"},
    {"symbol": "600487.SH", "name": "亨通光电", "market": "A股", "sector": "3. 高速通信与数据中心", "industry": "光通信/CPO", "feature": "全球光纤光缆核心供应"},
    
    # --- 日股 ---
    {"symbol": "5801.T", "name": "古河電気工業", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "光通信/CPO", "feature": "高性能光学互联"},
    {"symbol": "5802.T", "name": "住友電気工業", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "光通信/CPO", "feature": "精密连接器龙头"},
    {"symbol": "5803.T", "name": "フジクラ(藤仓)", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "光通信/CPO", "feature": "数据中心光缆核心"},
    {"symbol": "6501.T", "name": "日立製作所", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "能源/电力", "feature": "基础设施能源巨头"},
    {"symbol": "6367.T", "name": "ダイキン工業(大金)", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "能源/电力", "feature": "数据中心高效冷却技术"},
    {"symbol": "6834.T", "name": "精工技研", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "光通信/CPO", "feature": "精密光学组件"},
    {"symbol": "6777.T", "name": "santec", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "光通信/CPO", "feature": "光通信组件先驱"},
    {"symbol": "6981.T", "name": "村田製作所", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "被动元件/传感器", "feature": "全球被动元器件霸主"},
    {"symbol": "6762.T", "name": "TDK", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "被动元件/传感器", "feature": "电子元器件巨头"},
    {"symbol": "485A.T", "name": "PowerX", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "能源/电力", "feature": "新型储能电池与能源管理"},
    {"symbol": "6996.T", "name": "ニチコン(尼吉康)", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "能源/电力", "feature": "储能/充电系统"},
    {"symbol": "6503.T", "name": "三菱電機", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "能源/电力", "feature": "重型电力设备与数据中心基础设施"},
    {"symbol": "6504.T", "name": "富士電機", "market": "日股", "sector": "3. 高速通信与数据中心", "industry": "能源/电力", "feature": "能源基础设施与变流设备"},

    # ============================================================
    # 4. 前沿航天与深科技 (Space & Deep Tech)
    # ============================================================
    # --- 美股 ---
    {"symbol": "SPCX", "name": "SpaceX", "market": "美股", "sector": "4. 前沿航天与深科技", "industry": "航天/卫星", "feature": "**全球航天龙头**，Starlink底座"},
    {"symbol": "RKLB", "name": "Rocket Lab", "market": "美股", "sector": "4. 前沿航天与深科技", "industry": "航天/卫星", "feature": "**轻型火箭发射龙头**，端到端空间系统"},
    {"symbol": "GE", "name": "GE Aerospace", "market": "美股", "sector": "4. 前沿航天与深科技", "industry": "航空航天", "feature": "**全球航空动力巨头**，商用航空核心"},
    {"symbol": "RTX", "name": "RTX Corporation", "market": "美股", "sector": "4. 前沿航天与深科技", "industry": "航空航天", "feature": "全球顶级航空航天系统集成商"},
    {"symbol": "ASTS", "name": "AST SpaceMobile", "market": "美股", "sector": "4. 前沿航天与深科技", "industry": "航天/卫星", "feature": "太空蜂窝通信网络先驱"},
    
    # --- A股 ---
    {"symbol": "601989.SH", "name": "中国重工", "market": "A股", "sector": "4. 前沿航天与深科技", "industry": "航空航天", "feature": "高端重型制造平台"},
    
    # --- 日股 ---
    {"symbol": "9348.T", "name": "ispace", "market": "日股", "sector": "4. 前沿航天与深科技", "industry": "航天/卫星", "feature": "月球商业探测"},
    {"symbol": "186A.T", "name": "Astroscale", "market": "日股", "sector": "4. 前沿航天与深科技", "industry": "航天/卫星", "feature": "轨道治理先驱"},
    {"symbol": "7011.T", "name": "三菱重工", "market": "日股", "sector": "4. 前沿航天与深科技", "industry": "航空航天", "feature": "重型装备制造"},
    {"symbol": "7013.T", "name": "IHI", "market": "日股", "sector": "4. 前沿航天与深科技", "industry": "航空航天", "feature": "喷气推进系统"},
    {"symbol": "5631.T", "name": "日本製鋼所", "market": "日股", "sector": "4. 前沿航天与深科技", "industry": "航空航天", "feature": "大型工业铸锻件"},
    {"symbol": "6613.T", "name": "QDレーザ( QD激光)", "market": "日股", "sector": "4. 前沿航天与深科技", "industry": "航天/卫星", "feature": "半导体激光器先驱"}
]


