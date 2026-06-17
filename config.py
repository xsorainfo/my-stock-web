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
    # --- 1. 算力芯片+先进封装+存储 (Compute, HBM, Packaging) ---
    # 美股龙头
    {"symbol": "NVDA", "name": "英伟达", "market": "美股", "sector": "1. 算力芯片+先进封装+存储", "industry": "AI核心计算GPU", "feature": "全球AI算力芯片霸主"},
    {"symbol": "AMD", "name": "超威半导体", "market": "美股", "sector": "1. 算力芯片+先进封装+存储", "industry": "高性能计算芯片", "feature": "GPU算力第二极"},
    {"symbol": "ASML", "name": "阿斯麦", "market": "美股", "sector": "1. 算力芯片+先进封装+存储", "industry": "EUV光刻机", "feature": "全球EUV光刻机垄断者"},
    # 中国龙头
    {"symbol": "600584.SH", "name": "长电科技", "market": "A股", "sector": "1. 算力芯片+先进封装+存储", "industry": "先进封装/封测", "feature": "中国先进封装制造核心"},
    {"symbol": "002049.SZ", "name": "紫光国微", "market": "A股", "sector": "1. 算力芯片+先进封装+存储", "industry": "特种集成电路", "feature": "核心芯片研发"},
    # 日股 (原有补充)
    {"symbol": "8035.T", "name": "东京电子", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "涂布/显影设备", "feature": "AI芯片制造设备"},
    {"symbol": "6857.T", "name": "爱德万测试", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "HBM测试系统", "feature": "HBM测试机霸主"},
    {"symbol": "4063.T", "name": "信越化学", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "硅片/光刻胶", "feature": "半导体材料霸主"},
    {"symbol": "3110.T", "name": "日东纺绩", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "高端玻璃纤维布", "feature": "基板材料核心供应商"},
    {"symbol": "6920.T", "name": "激光技术", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "EUV光罩检测", "feature": "EUV检测独家"},
    {"symbol": "6146.T", "name": "迪斯科", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "精密加工", "feature": "先进封装切割设备"},
    {"symbol": "4186.T", "name": "东京应化", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "EUV光刻胶", "feature": "高端光刻胶冠军"},
    {"symbol": "4062.T", "name": "揖斐电", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "封装基板", "feature": "数据中心级基板"},
    {"symbol": "6971.T", "name": "京瓷", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "精密陶瓷/封装", "feature": "陶瓷元器件制造"},
    {"symbol": "6315.T", "name": "TOWA", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "封装设备", "feature": "压缩成型封装"},
    {"symbol": "6963.T", "name": "罗姆", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "功率半导体", "feature": "SiC功率模块"},
    {"symbol": "6525.T", "name": "KOKUSAI ELECTRIC", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "薄膜沉积设备", "feature": "半导体成膜设备核心厂商"},
    {"symbol": "6723.T", "name": "瑞萨电子", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "MCU/模拟芯片", "feature": "车载与工业芯片龙头"},
    {"symbol": "7735.T", "name": "SCREEN控股", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "晶圆清洗设备", "feature": "全球晶圆清洗设备领先厂商"},
    {"symbol": "6526.T", "name": "Socionext", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "定制SoC", "feature": "先进制程SoC设计"},
    {"symbol": "6871.T", "name": "日本微米尼克斯", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "探针卡", "feature": "晶圆测试探针卡厂商"},
    {"symbol": "6890.T", "name": "FERROTEC", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "半导体零部件", "feature": "真空密封与石英制品"},
    {"symbol": "6590.T", "name": "芝浦机电", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "先进封装设备", "feature": "晶圆处理与封装设备"},
    {"symbol": "6855.T", "name": "日本电子材料", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "探针卡", "feature": "半导体测试探针卡专业厂"},
    {"symbol": "6754.T", "name": "安立", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "测试测量", "feature": "高速通信测试设备"},

    {"symbol": "285A.T", "name": "铠侠控股", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "NAND存储", "feature": "全球闪存厂商"},
    {"symbol": "6976.T", "name": "太阳诱电", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "MLCC", "feature": "高性能电子元件"},
    {"symbol": "6752.T", "name": "松下控股", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "电池/电子", "feature": "工业电池与电子方案"},
    {"symbol": "6701.T", "name": "日本电气", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "IT基础设施", "feature": "AI系统与网络基础设施"},
    {"symbol": "6702.T", "name": "富士通", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "IT服务", "feature": "高性能计算与企业AI"},
    {"symbol": "6965.T", "name": "滨松光子", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "光电器件", "feature": "光传感器与光探测设备"},
    {"symbol": "6779.T", "name": "日本电波工业", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "晶振", "feature": "频率控制元件龙头"},
    {"symbol": "6787.T", "name": "MEIKO", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "PCB", "feature": "高端印刷电路板制造商"},
    {"symbol": "6479.T", "name": "美蓓亚三美", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "精密零部件", "feature": "轴承与精密电机龙头"},
    {"symbol": "7751.T", "name": "佳能", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "光学设备", "feature": "纳米压印光刻技术布局"},
    {"symbol": "6740.T", "name": "日本显示器", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "显示面板", "feature": "车载与中小尺寸显示"},
    {"symbol": "6997.T", "name": "日本化工", "market": "日股", "sector": "1. 算力芯片+先进封装+存储", "industry": "电容器", "feature": "铝电解电容龙头"},
    {"symbol": "QCOM", "name": "高通", "market": "美股", "sector": "1. 算力芯片+先进封装+存储", "industry": "移动AI芯片", "feature": "AI手机与AI PC处理器龙头"},

    # --- 2. 工业自动化与机器人 (Factory Automation) ---
    # 美股龙头
    {"symbol": "ROK", "name": "罗克韦尔自动化", "market": "美股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "工业控制", "feature": "工业自动化集成方案"},
    # 中国龙头
    {"symbol": "688037.SH", "name": "埃斯顿", "market": "A股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "工业机器人", "feature": "中国工业机器人龙头"},
    {"symbol": "002008.SZ", "name": "大族激光", "market": "A股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "激光加工设备", "feature": "精密制造与激光自动化"},
    # 日股 (原有补充)
    {"symbol": "6861.T", "name": "基恩士", "market": "日股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "机器视觉", "feature": "高精度传感系统"},
    {"symbol": "6954.T", "name": "发那科", "market": "日股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "工业机器人", "feature": "自动化机器人核心"},
    {"symbol": "6273.T", "name": "SMC", "market": "日股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "气动元件", "feature": "全球气动元件霸主"},
    {"symbol": "6324.T", "name": "Harmonic", "market": "日股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "精密减速器", "feature": "精密减速器标杆"},
    {"symbol": "6506.T", "name": "安川电机", "market": "日股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "伺服驱动", "feature": "电机与运动控制"},
    {"symbol": "6594.T", "name": "尼得科", "market": "日股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "精密电机", "feature": "电机驱动技术龙头"},
    {"symbol": "6645.T", "name": "欧姆龙", "market": "日股", "sector": "2. 工业自动化与机器人 (Factory Automation)", "industry": "传感控制", "feature": "工业自动化方案"},



    # --- 3. 高速通信与基础设施 (Optics, CPO, Power, Data Center) ---
    # 美股龙头
    {"symbol": "MSFT", "name": "微软", "market": "美股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "云计算/AI底座", "feature": "全球最大的云与AI基础设施"},
    {"symbol": "CEG", "name": "星座能源", "market": "美股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "核能电力", "feature": "AI数据中心核电直供"},
    # 中国龙头
    {"symbol": "300308.SZ", "name": "中际旭创", "market": "A股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "光模块/CPO", "feature": "全球高端光模块龙头"},
    {"symbol": "600487.SH", "name": "亨通光电", "market": "A股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "光通信/海缆", "feature": "全球光纤光缆核心供应"},
    # 日股 (原有补充)

    {"symbol": "5801.T", "name": "古河电工", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "CPO光电共封装", "feature": "高性能光学互联"},
    {"symbol": "5802.T", "name": "住友电工", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "高带宽互联", "feature": "精密连接器龙头"},
    {"symbol": "5803.T", "name": "藤仓", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "高速光缆", "feature": "数据中心光缆核心"},
    {"symbol": "6501.T", "name": "日立制作所", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "电网/变压器", "feature": "基础设施能源巨头"},
    {"symbol": "6367.T", "name": "大金工业", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "液冷/温控", "feature": "数据中心高效冷却技术"},
    {"symbol": "6834.T", "name": "精工技研", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "光学连接器", "feature": "精密光学组件"},
    {"symbol": "6777.T", "name": "santec", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "光学测量", "feature": "光通信组件先驱"},
    {"symbol": "6981.T", "name": "村田制作所", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "MLCC电容", "feature": "全球被动元器件霸主"},
    {"symbol": "6762.T", "name": "TDK", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "被动元件/传感器", "feature": "电子元器件巨头"},
    {"symbol": "CEG", "name": "星座能源", "market": "美股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "核能电力", "feature": "AI算力核电直供"},
    {"symbol": "485A.T", "name": "PowerX", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "储能系统", "feature": "新型储能电池与能源管理"},
    {"symbol": "6996.T", "name": "尼吉康", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "电力电子", "feature": "储能/充电系统"},
    {"symbol": "6503.T", "name": "三菱电机", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "电力设备", "feature": "重型电力设备与数据中心基础设施"},
    {"symbol": "6504.T", "name": "富士电机", "market": "日股", "sector": "3. 高速通信与基础设施 (Optics, CPO, Power, Data Center)", "industry": "电力电子", "feature": "能源基础设施与变流设备"},
    # --- 4. 前沿航天与深科技 (Space & Deep Tech)---
    # 美股龙头
    {"symbol": "SPCX", "name": "SpaceX", "market": "美股(未上市)", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "航天发射/卫星通信", "feature": "**全球航天龙头**，Starlink底座"},
    {"symbol": "RKLB", "name": "Rocket Lab", "market": "美股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "航天发射/航天系统", "feature": "**轻型火箭发射龙头**，端到端空间系统"},
    {"symbol": "GE", "name": "GE Aerospace", "market": "美股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "航空发动机", "feature": "**全球航空动力巨头**，商用航空核心"},
    {"symbol": "RTX", "name": "RTX Corporation", "market": "美股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "航空航天/防务", "feature": "全球顶级航空航天系统集成商"},
    {"symbol": "ASTS", "name": "AST SpaceMobile", "market": "美股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "卫星通信", "feature": "太空蜂窝通信网络先驱"},
    # 中国龙头
    {"symbol": "601989.SH", "name": "中国重工", "market": "A股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "航天/重型装备", "feature": "高端重型制造平台"},
    # 日股 (原有补充)
    {"symbol": "9348.T", "name": "ispace", "market": "日股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "航天开发", "feature": "月球商业探测"},
    {"symbol": "186A.T", "name": "Astroscale", "market": "日股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "太空碎片清理", "feature": "轨道治理先驱"},
    {"symbol": "7011.T", "name": "三菱重工", "market": "日股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "航空航天", "feature": "重型装备制造"},
    {"symbol": "7013.T", "name": "IHI", "market": "日股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "航空发动机", "feature": "喷气推进系统"},
    {"symbol": "5631.T", "name": "日本制钢所", "market": "日股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "特种材料", "feature": "大型工业铸锻件"},
    {"symbol": "6613.T", "name": "QD激光", "market": "日股", "sector": "4. 前沿航天与深科技 (Space & Deep Tech)", "industry": "光子学", "feature": "半导体激光器先驱"}
]


