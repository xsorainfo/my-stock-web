# ============================================================
# config.py - 全球AI硬科技决策终端
# 完整版 | 更新日期：2026年6月
# ============================================================

# ============================================================
# 全局配置
# ============================================================

DEFAULT_STRATEGY = ["yfinance"]

# 只有需要特殊处理的标的才写在这里
SOURCE_MAP = {
    "NVDA": ["yfinance", "alphavantage"],
    "3110.T": ["yfinance"]
}

MACRO_LIST = [
    {"symbol": "^SOX", "name": "费城半导体指数"},
    {"symbol": "JPY=X", "name": "美元/日元 (汇率)"},
    {"symbol": "^N225", "name": "日经 225"},
    {"symbol": "^GSPC", "name": "标普 500"}
]

DEFAULT_STRATEGY = ["yfinance"]

# 只有需要特殊处理的标的才写在这里
SOURCE_MAP = {
    #"NVDA": ["yfinance", "alphavantage"],
    #"3110.T": ["yfinance"]
}

MACRO_LIST = [
    {"symbol": "^SOX", "name": "费城半导体指数"},
    {"symbol": "JPY=X", "name": "美元/日元 (汇率)"},
    {"symbol": "^N225", "name": "日经 225"},
    {"symbol": "^GSPC", "name": "标普 500"}
]

THEME_MAPPING = {
    # ============================================================
    # 1. 半导体设备（按细分领域）
    # ============================================================
    "1. 半导体设备": [
        "光刻机", "刻蚀设备", "CVD设备", "PVD设备", "ALD设备", "清洗设备", "CMP设备", 
        "离子注入机", "离子注入机", "热处理炉管", "检测设备", "量测设备", "晶圆搬运自动化", "ATE测试设备", "封装设备"
    ],

    # ============================================================
    # 2. 半导体材料（按细分领域）
    # ============================================================
    "2. 半导体材料": [
        "硅晶圆", "光刻胶", "光掩膜", "光刻基板", "高纯化学品", "电子特气", "靶材","磷化铟",
        "CMP浆料", "CMP抛光垫", "封装基板", "引线框架", "焊球", "焊料", "EMC塑封料", "ABF载板", "导电胶", "绝缘膜", "MLCC", "PCB"
    ],
    # ============================================================
    # 3-9. 其他赛道（保持不变）
    # ============================================================
    "3. 算力芯片": ["GPU", "ASIC", "CPU", "FPGA", "AI SoC"],
    "4. 高带宽内存": ["HBM", "GDDR6", "SRAM", "内存接口"],
    "5. 先进封装": ["2.5D封装", "3D封装", "Chiplet", "封装材料"],
    "6. 网络互联": ["NVLink/NVSwitch", "InfiniBand", "RoCE", "PCIe"],
    "7. 光通信": ["光模块", "光芯片", "光纤光缆", "硅光子"],
    "8. 电力・液冷・数据中心": ["电力系统", "液冷设备", "数据中心架构"],
    "9. 云・模型・应用": ["云服务IaaS", "基础模型", "AI应用", "智能体Agent"]
}


WATCHLIST = [
    # ============================================================
    # 赛道1.1：算力芯片+存储（Compute & Memory）
    # ============================================================

    # --- 美股 AI处理器 ---
    {"symbol": "NVDA", "name": "NVIDIA(英伟达)", "market": "美股", "sector": "1.1", "industry": "1.1.1", "feature": "**全球AI芯片绝对霸主**，GPU市占率80%+，CUDA生态壁垒极高。Vera CPU进军CPU市场，成最危险新进入者", "tags": ["GPU", "CPU"]},
    {"symbol": "AMD", "name": "AMD(超威半导体)", "market": "美股", "sector": "1.1", "industry": "1.1.1", "feature": "**CPU大战最大赢家**，x86份额32.6%创历史新高，EPYC出货占比33.2%。MI300系列AI芯片对标NVIDIA", "tags": ["GPU", "CPU"]},
    {"symbol": "INTC", "name": "英特尔", "market": "美股", "sector": "1.1", "industry": "1.1.1", "feature": "**x86龙头触底反弹**，服务器CPU市占率59%。Gaudi3 AI加速器对标H100，IFS代工为第二增长曲线", "tags": ["CPU", "ASIC"]},
    {"symbol": "QCOM", "name": "高通", "market": "美股", "sector": "1.1", "industry": "1.1.1", "feature": "**ARM PC CPU赛道龙头**，骁龙X Elite对标苹果M系列，目标2029年占据非x86 AI笔记本30-50%份额", "tags": ["AI SoC", "CPU"]},
    {"symbol": "AVGO", "name": "博通", "market": "美股", "sector": "1.1", "industry": "1.1.1", "feature": "**AI网络芯片与ASIC龙头**，以太网芯片市占率70%+，谷歌TPU核心ASIC设计合作伙伴", "tags": ["ASIC"]},
    {"symbol": "MRVL", "name": "美满电子", "market": "美股", "sector": "1.1", "industry": "1.1.1", "feature": "**数据中心互联芯片核心玩家**，高速SerDes技术领先，AI互联芯片市占率全球前三", "tags": ["ASIC"]},
    {"symbol": "ARM", "name": "ARM Holdings", "market": "美股", "sector": "1.1", "industry": "1.1.1", "feature": "**全球芯片IP架构霸主**，指令集市占率90%+，服务器CPU市占率16%，2030年预计达27%", "tags": ["CPU"]},
    {"symbol": "AAPL", "name": "苹果", "market": "美股", "sector": "1.1", "industry": "1.1.1", "feature": "**ARM PC浪潮开启者**，M系列芯片证明ARM在PC端性能潜力，Mac全系已切换至自研ARM芯片", "tags": ["CPU"]},

    # --- 日股 AI处理器 ---
    {"symbol": "6723.T", "name": "ルネサス(瑞萨电子)", "market": "日股", "sector": "1.1", "industry": "1.1.1", "feature": "**车载与工业MCU龙头**，全球MCU市占率15%+，ARM生态重要伙伴，AI边缘计算芯片核心供应商", "tags": ["AI SoC", "GPU", "CPU"]},
    {"symbol": "6526.T", "name": "ソシオネクスト(Socionext)", "market": "日股", "sector": "1.1", "industry": "1.1.1", "feature": "**先进制程SoC设计龙头**，5nm/3nm定制芯片设计能力，AI边缘计算核心方案商", "tags": ["ASIC"]},
    {"symbol": "6963.T", "name": "ローム(罗姆)", "market": "日股", "sector": "1.1", "industry": "1.1.1", "feature": "**SiC功率模块先驱**，碳化硅功率器件市占率全球前三，AI服务器电源管理核心器件", "tags": ["碳化硅 (SiC)"]},

    # --- A股 AI处理器 ---
    {"symbol": "002049.SZ", "name": "紫光国微", "market": "A股", "sector": "1.1", "industry": "1.1.1", "feature": "**中国特种IC龙头**，FPGA芯片国内领先，智能卡芯片市占率超30%，国产替代核心标的", "tags": ["FPGA"]},
    {"symbol": "688802.SH", "name": "沐曦股份", "market": "A股", "sector": "1.1", "industry": "1.1.1", "feature": "**国产GPU营收第一**，2025年营收16.44亿元，毛利率56.5%，性能对标NVIDIA A100", "tags": ["GPU", "ASIC"]},
    {"symbol": "688795.SH", "name": "摩尔线程", "market": "A股", "sector": "1.1", "industry": "1.1.1", "feature": "**全功能GPU国产替代龙头**，2025年营收15.06亿元，毛利率69%，MTT S4000比肩国际主流", "tags": ["GPU"]},
    {"symbol": "688041.SH", "name": "海光信息", "market": "A股", "sector": "1.1", "industry": "1.1.1", "feature": "**A股国产CPU第一股**，x86（AMD Zen授权）生态兼容性最强，信创服务器CPU主力供应商", "tags": ["CPU"]},
    {"symbol": "688047.SH", "name": "龙芯中科", "market": "A股", "sector": "1.1", "industry": "1.1.1", "feature": "**完全自主指令集LoongArch CPU**，纯国产CPU代表，党政信创核心供应商，摆脱x86/ARM授权", "tags": ["CPU"]},
    {"symbol": "688262.SH", "name": "国芯科技", "market": "A股", "sector": "1.1", "industry": "1.1.1", "feature": "**三大指令集嵌入式CPU专家**，国内唯一同时掌握RISC-V/PowerPC/M*Core，车规/工控高可靠龙头", "tags": ["CPU"]},

    # --- 存储/HBM ---
    {"symbol": "MU", "name": "美光科技", "market": "美股", "sector": "1.1", "industry": "1.1.2", "feature": "**HBM核心供应商**，全球DRAM市占率约25%，AI训练HBM3E内存核心供应商", "tags": ["HBM"]},
    {"symbol": "CY", "name": "赛普拉斯半导体", "market": "美股", "sector": "1.1", "industry": "1.1.2", "feature": "**全球SRAM龙头**，已被英飞凌收购但独立运营，SRAM市占率全球领先，CPU缓存核心供应商", "tags": ["SRAM"]},
    {"symbol": "RGTI", "name": "Rambus", "market": "美股", "sector": "1.1", "industry": "1.1.2", "feature": "**内存接口与IP龙头**，DDR5内存接口IP全球领先，HBM内存控制器IP核心供应商，AI数据中心内存方案商", "tags": ["内存接口"]},
    {"symbol": "005930.KS", "name": "三星电子", "market": "韩股", "sector": "1.1", "industry": "1.1.2", "feature": "**全球存储芯片霸主**，DRAM/NAND市占率均超40%，HBM3技术领先，全产业链优势明显", "tags": ["HBM", "GDDR6"]},
    {"symbol": "000660.KS", "name": "SK海力士", "market": "韩股", "sector": "1.1", "industry": "1.1.2", "feature": "**HBM技术领导者**，HBM3全球市占率超50%，NVIDIA核心HBM供应商，AI训练内存绝对龙头", "tags": ["HBM"]},
    {"symbol": "285A.T", "name": "キオクシア(铠侠)", "market": "日股", "sector": "1.1", "industry": "1.1.2", "feature": "**全球闪存厂商之一**，NAND Flash市占率约15%，AI存储需求核心受益者", "tags": ["存储"]},
    {"symbol": "688008.SH", "name": "澜起科技", "market": "A股", "sector": "1.1", "industry": "1.1.2", "feature": "**全球内存接口芯片龙头**，DDR5内存接口芯片市占率全球领先，津逮服务器CPU国产替代核心标的", "tags": ["内存接口", "CPU"]},

    # ============================================================
    # 赛道1.2：先进制造与设备
    # ============================================================

    # --- 半导体材料 ---
    {"symbol": "DOW", "name": "陶氏化学", "market": "美股", "sector": "1.2", "industry": "1.2.1", "feature": "**CMP抛光垫全球霸主**，全球市占率超70%，半导体CMP工序核心材料供应商", "tags": ["CMP抛光垫"]},
    {"symbol": "LIN", "name": "林德集团", "market": "美股", "sector": "1.2", "industry": "1.2.1", "feature": "**全球工业气体与电子特气龙头**，全球最大工业气体供应商，半导体制造核心特种气体供应商", "tags": ["电子特气"]},
    {"symbol": "PLAB", "name": "Photronics(福尼克斯)", "market": "美股", "sector": "1.2", "industry": "1.2.1", "feature": "**全球光掩模龙头之一**，与TOPPAN/大日本印刷并列全球光掩模三巨头，先进制程光掩模核心供应商", "tags": ["光掩膜"]},
    {"symbol": "HOG", "name": "Hoya Corporation(豪雅)", "market": "美股", "sector": "1.2", "industry": "1.2.1", "feature": "**光刻基板全球龙头**，光掩膜基板(Mask Blank)市占率全球领先，EUV光刻核心材料供应商，与AGC并列双雄", "tags": ["光刻基板"]},
    {"symbol": "BAS.DE", "name": "巴斯夫", "market": "德股", "sector": "1.2", "industry": "1.2.1", "feature": "**全球高纯化学品龙头**，半导体级高纯试剂/电子化学品全球领先，晶圆清洗/刻蚀工序核心材料供应商", "tags": ["高纯化学品"]},
    {"symbol": "688126.SH", "name": "沪硅产业", "market": "A股", "sector": "1.2", "industry": "1.2.1", "feature": "**中国硅片龙头**，12英寸硅片国产替代核心标的，AI芯片制造关键材料供应商", "tags": ["硅晶圆"]},
    {"symbol": "4063.T", "name": "信越化学", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**半导体材料霸主**，全球硅片市占率超30%，光刻胶市占率超20%，半导体材料全方位布局", "tags": ["硅晶圆", "光刻胶"]},
    {"symbol": "3436.T", "name": "SUMCO", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**全球半导体硅片第二大供应商**，与信越化学构成行业双寡头，12英寸硅片核心供应商", "tags": ["硅晶圆"]},
    {"symbol": "4185.T", "name": "JSR", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**光刻胶全球霸主之一**，与东京应化等合计占据全球光刻胶约90%市场份额，ArF/EUV光刻胶核心供应商", "tags": ["光刻胶"]},
    {"symbol": "4186.T", "name": "東京応化工業(东京应化)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**高端光刻胶冠军**，ArF光刻胶市占率超30%，EUV光刻胶布局领先，全球光刻胶核心供应商", "tags": ["光刻胶"]},
    {"symbol": "7911.T", "name": "TOPPANホールディングス", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**光掩模全球双雄之一**，全球光掩模市占率领先，EUV光掩模技术布局深厚", "tags": ["光掩膜"]},
    {"symbol": "7912.T", "name": "大日本印刷(DNP)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**光掩模全球双雄之一**，与TOPPAN合计占据全球光掩模绝大部分市场份额，先进制程光掩模核心供应商", "tags": ["光掩膜"]},
    {"symbol": "5201.T", "name": "AGC(旭硝子)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**光刻基板全球龙头**，光掩膜基板(Mask Blank)市占率全球领先，半导体光刻核心材料供应商", "tags": ["光刻基板"]},
    {"symbol": "4092.T", "name": "関東化学(关东化学)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**超高纯半导体化学品龙头**，湿电子化学品/高纯试剂全球领先，半导体清洗/刻蚀工序核心材料供应商", "tags": ["高纯化学品"]},
    {"symbol": "4091.T", "name": "大陽日酸(大阳日酸)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**日本电子特气龙头**，高纯度电子特气市占率日本第一，半导体制造关键气体供应商", "tags": ["电子特气"]},
    {"symbol": "5727.T", "name": "日鉱金属(日矿金属)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**半导体靶材全球龙头**，高纯度溅射靶材市占率全球前列，半导体互连层制造核心材料供应商", "tags": ["靶材"]},
    {"symbol": "4901.T", "name": "富士フイルム(富士胶片)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**CMP浆料与光刻胶核心供应商**，半导体材料业务全球领先，CMP浆料市占率居前", "tags": ["CMP浆料"]},
    {"symbol": "4920.T", "name": "日本研磨材", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**CMP抛光材料核心供应商**，半导体CMP研磨材料技术领先，日本CMP材料领域核心厂商", "tags": ["CMP抛光垫"]},
    {"symbol": "4062.T", "name": "イビデン(揖斐电)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**数据中心级封装基板龙头**，CPU/GPU封装基板核心供应商，AI服务器基板市占率领先", "tags": ["封装基板"]},
    {"symbol": "6971.T", "name": "京セラ(京瓷)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**精密陶瓷元器件巨头**，半导体封装陶瓷材料核心供应商，市占率全球前三", "tags": ["封装基板"]},
    {"symbol": "6967.T", "name": "新光電気工業(新光电气)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**半导体封装基板龙头**，FC-BGA封装基板技术全球领先，CPU/GPU高端封装核心供应商", "tags": ["封装基板"]},
    {"symbol": "6914.T", "name": "三井ハイテック(三井高科技)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**引线框架全球龙头**，半导体封装引线框架市占率全球前列，功率器件/IC封装核心材料供应商", "tags": ["引线框架"]},
    {"symbol": "7955.T", "name": "千住金属", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**半导体焊接材料龙头**，焊球/焊料/助焊剂技术全球领先，BGA封装核心材料供应商", "tags": ["焊球", "焊料"]},
    {"symbol": "4005.T", "name": "Resonac Holdings", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**环氧塑封料(EMC)+ABF载板材料全球龙头**，半导体封装核心保护材料+AI服务器CPU/GPU封装关键材料供应商", "tags": ["EMC塑封料", "ABF载板"]},
    {"symbol": "4222.T", "name": "日立化成(Resonac)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**半导体封装用导电胶/绝缘膜龙头**，先进封装互连材料核心供应商", "tags": ["导电胶", "绝缘膜"]},
    {"symbol": "3110.T", "name": "日東紡績", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**高端玻璃纤维布核心供应商**，半导体封装基板材料市占率领先，AI芯片封装不可或缺材料", "tags": ["封装基板 (ABF/BT)"]},
    {"symbol": "6920.T", "name": "レーザーテック(激光技术)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**EUV光罩检测独家供应商**，市占率超90%，EUV光刻配套检测设备垄断地位", "tags": ["光掩膜"]},
    {"symbol": "6890.T", "name": "FERROTEC", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**真空密封与石英制品龙头**，半导体制造真空腔体核心供应商，技术壁垒极高", "tags": ["高纯化学品"]},
    {"symbol": "6965.T", "name": "浜松ホトニクス(浜松光子)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**光电器件全球龙头**，光电倍增管市占率超80%，半导体检测核心器件供应商", "tags": ["光刻基板"]},
    {"symbol": "6779.T", "name": "日本電波工業", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**频率控制元件龙头**，晶振市占率全球前列，AI服务器时钟器件核心供应商", "tags": ["MLCC"]},
    {"symbol": "6997.T", "name": "日本ケミコン(日本化工)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**铝电解电容龙头**，全球市占率超20%，AI服务器电源滤波核心器件", "tags": ["MLCC"]},
    {"symbol": "6479.T", "name": "ミネベアミツミ(美蓓亚三美)", "market": "日股", "sector": "1.2", "industry": "1.2.1", "feature": "**轴承与精密电机龙头**，微型轴承全球市占率超60%，半导体设备精密零部件供应商", "tags": ["封装基板"]},

    # --- 半导体设备 ---
    {"symbol": "ASML", "name": "ASML(阿斯麦)", "market": "美股", "sector": "1.2", "industry": "1.2.2", "feature": "**全球EUV光刻机绝对垄断**，市占率100%，先进制程（7nm以下）芯片制造核心设备供应商", "tags": ["光刻机"]},
    {"symbol": "AMAT", "name": "应用材料", "market": "美股", "sector": "1.2", "industry": "1.2.2", "feature": "**全球最大半导体设备商**，沉积(CVD/PVD)市占率超40%，CMP/离子注入/检测设备核心供应商", "tags": ["CVD设备", "PVD设备", "CMP设备", "离子注入机"]},
    {"symbol": "LRCX", "name": "泛林半导体", "market": "美股", "sector": "1.2", "industry": "1.2.2", "feature": "**刻蚀设备全球龙头**，刻蚀市占率超50%，薄膜沉积技术领先，与TEL直接竞争", "tags": ["刻蚀设备", "CVD设备"]},
    {"symbol": "KLAC", "name": "科磊", "market": "美股", "sector": "1.2", "industry": "1.2.2", "feature": "**晶圆检测设备绝对霸主**，过程控制市占率超50%，芯片良率控制核心设备供应商", "tags": ["检测设备", "量测设备"]},
    {"symbol": "TER", "name": "泰瑞达", "market": "美股", "sector": "1.2", "industry": "1.2.2", "feature": "**半导体测试设备龙头**，ATE自动测试设备市占率全球前三，AI芯片测试核心设备供应商", "tags": ["ATE测试设备"]},
    {"symbol": "ASMI", "name": "先晶半导体(ASM International)", "market": "美股", "sector": "1.2", "industry": "1.2.2", "feature": "**全球ALD设备龙头**，原子层沉积(ALD)技术全球领先，先进制程薄膜沉积核心设备供应商", "tags": ["ALD设备"]},
    {"symbol": "ACLS", "name": "Axcelis Technologies", "market": "美股", "sector": "1.2", "industry": "1.2.2", "feature": "**全球离子注入机龙头**，市占率仅次于应用材料，先进制程离子注入设备核心供应商，AI芯片制造关键设备", "tags": ["离子注入机"]},
    {"symbol": "8035.T", "name": "東京エレクトロン(Tokyo Electron)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**全球涂布显影设备龙头**，市占率超80%，刻蚀/沉积全球前三，半导体前道工序核心设备供应商", "tags": ["光刻机", "刻蚀设备", "CVD设备"]},
    {"symbol": "6857.T", "name": "アドバンテスト(爱德万)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**HBM测试机霸主**，DRAM测试设备市占率超50%，AI芯片测试核心设备供应商", "tags": ["ATE测试设备", "量测检测设备"]},
    {"symbol": "6146.T", "name": "ディスコ(迪斯科)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**晶圆切割设备龙头**，全球市占率超70%，先进封装切割设备核心供应商", "tags": ["封装设备"]},
    {"symbol": "7735.T", "name": "SCREENホールディングス(斯库林)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**晶圆清洗设备龙头**，全球市占率超40%，半导体制造清洗工序核心设备供应商", "tags": ["清洗设备", "检测设备"]},
    {"symbol": "6525.T", "name": "KOKUSAI ELECTRIC(国际电气)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**半导体成膜设备核心厂商**，CVD/ALD设备市占率全球前列，逻辑/存储芯片制造核心设备", "tags": ["CVD设备", "ALD设备"]},
    {"symbol": "6315.T", "name": "TOWA", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**压缩成型封装设备龙头**，全球市占率超60%，先进封装塑封设备核心供应商", "tags": ["封装设备"]},
    {"symbol": "6361.T", "name": "荏原製作所(Ebara)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**CMP设备全球第二**，市占率约37%，半导体平坦化工艺核心设备供应商，仅次于应用材料", "tags": ["CMP设备"]},
    {"symbol": "8036.T", "name": "日立ハイテク(日立高新)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**刻蚀设备全球第四**，市占率约5.7%，电子显微镜等测量/分析设备行业龙头", "tags": ["刻蚀设备", "检测设备", "量测设备"]},
    {"symbol": "7729.T", "name": "東京精密", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**晶圆探针台全球顶尖**，与东京电子共同主导探针台市场，晶圆测试关键设备供应商", "tags": ["量测设备"]},
    {"symbol": "6323.T", "name": "ローツェ(Rorze)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**晶圆搬运机器人系统全球No.1**，半导体工厂自动化(FA)核心设备，晶圆传输系统领先", "tags": ["晶圆搬运自动化"]},
    {"symbol": "6383.T", "name": "ダイフク(大福)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**半导体工厂自动化(FA)系统龙头**，晶圆搬运/AMHS系统全球市占率领先，半导体智能制造核心方案商", "tags": ["晶圆搬运自动化"]},
    {"symbol": "7995.T", "name": "新川(Shinkawa)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**半导体封装设备龙头**，固晶机/键合机市占率全球前列，先进封装设备核心供应商", "tags": ["封装设备"]},
    {"symbol": "7731.T", "name": "ニコン(尼康)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**全球光刻机双雄之一**，与ASML构成光刻机市场双寡头，先进光刻技术布局深厚，日本半导体设备核心厂商", "tags": ["光刻机"]},
    {"symbol": "6590.T", "name": "芝浦メカトロニクス(芝浦机电)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**晶圆处理与封装设备核心厂商**，先进封装湿制程设备市占率领先", "tags": ["封装设备"]},
    {"symbol": "6855.T", "name": "日本電子材料", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**半导体测试探针卡专业厂**，MEMS探针卡技术领先，AI芯片测试关键供应商", "tags": ["检测设备"]},
    {"symbol": "6871.T", "name": "日本マイクロニクス", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**晶圆测试探针卡专业厂**，高端探针卡市占率全球前列，AI芯片测试关键供应商", "tags": ["检测设备"]},
    {"symbol": "6754.T", "name": "アンリツ(安立)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**高速通信测试设备龙头**，400G/800G光通信测试市占率全球领先", "tags": ["ATE测试设备"]},
    {"symbol": "6834.T", "name": "ニューフレアテクノロジー(纽富来)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**光罩描画设备全球第二**，市占率约26.3%，先进光罩制造核心设备，EUV光罩关键供应商", "tags": ["检测设备"]},
    {"symbol": "6951.T", "name": "日本電子", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**电子束描画设备领先厂商**，市占率约8.4%，电子显微镜等分析测量领域技术实力雄厚", "tags": ["量测设备"]},
    {"symbol": "7751.T", "name": "キヤノン(佳能)", "market": "日股", "sector": "1.2", "industry": "1.2.2", "feature": "**纳米压印光刻技术布局者**，光刻技术第二路线，先进制程潜在替代方案", "tags": ["光刻机"]},
    {"symbol": "688012.SH", "name": "中微公司", "market": "A股", "sector": "1.2", "industry": "1.2.2", "feature": "**中国刻蚀设备龙头**，CCP刻蚀国内市占率超80%，5nm制程设备已进入台积电供应链", "tags": ["刻蚀设备"]},

    # ============================================================
    # 赛道1.3：封装测试（Packaging & Testing）
    # ============================================================
    {"symbol": "ASX", "name": "日月光", "market": "美股", "sector": "1.3", "industry": "1.3.1", "feature": "**全球封测绝对龙头**，全球市占率超30%，先进封装技术全球领先，AI芯片封装核心供应商", "tags": ["2.5D封装", "3D封装"]},
    {"symbol": "AMKR", "name": "安靠科技", "market": "美股", "sector": "1.3", "industry": "1.3.1", "feature": "**全球封测第二**，全球市占率约15%，先进封装技术领先，AI芯片封装核心供应商之一", "tags": ["2.5D封装", "3D封装"]},
    {"symbol": "600584.SH", "name": "长电科技", "market": "A股", "sector": "1.3", "industry": "1.3.1", "feature": "**中国封测龙头**，全球封测市占率约10%，先进封装技术布局完善，Chiplet封装核心供应商", "tags": ["Chiplet", "先进封装"]},
    {"symbol": "002156.SZ", "name": "通富微电", "market": "A股", "sector": "1.3", "industry": "1.3.1", "feature": "**中国封测第二极**，AMD核心封测合作伙伴，先进封装产能持续扩张", "tags": ["Chiplet", "先进封装"]},
    {"symbol": "6787.T", "name": "メイコー(MEIKO)", "market": "日股", "sector": "1.3", "industry": "1.3.2", "feature": "**高端PCB制造商**，高多层PCB技术领先，AI服务器电路板核心供应商", "tags": ["PCB"]},

    # ============================================================
    # 赛道1.4：互联与通信
    # ============================================================
    {"symbol": "COHR", "name": "Coherent", "market": "美股", "sector": "1.4", "industry": "1.4.2", "feature": "**全球光通信材料龙头**，光模块/光器件市占率全球前列，AI数据中心互联核心供应商", "tags": ["光模块", "光芯片"]},
    {"symbol": "LITE", "name": "Lumentum", "market": "美股", "sector": "1.4", "industry": "1.4.2", "feature": "**光通信器件龙头**，VCSEL/光芯片技术领先，CPO光电共封装核心方案商", "tags": ["光芯片", "硅光子"]},
    {"symbol": "300308.SZ", "name": "中际旭创", "market": "A股", "sector": "1.4", "industry": "1.4.2", "feature": "**全球高端光模块龙头**，400G/800G光模块市占率超30%，AI数据中心互联核心供应商", "tags": ["光模块"]},
    {"symbol": "300502.SZ", "name": "新易盛", "market": "A股", "sector": "1.4", "industry": "1.4.2", "feature": "**全球光模块核心供应商**，400G/800G光模块技术领先，AI数据中心互联核心供应商，中际旭创主要竞争对手", "tags": ["光模块"]},
    {"symbol": "688498.SH", "name": "源杰科技", "market": "A股", "sector": "1.4", "industry": "1.4.2", "feature": "**国产光芯片龙头**，高速激光器芯片技术领先，100G EML光芯片国产替代核心标的，AI数据中心互联上游", "tags": ["光芯片"]},
    {"symbol": "600487.SH", "name": "亨通光电", "market": "A股", "sector": "1.4", "industry": "1.4.2", "feature": "**全球光纤光缆核心供应商**，通信光缆市占率全球前三，AI数据中心传输基础建设者", "tags": ["光纤光缆"]},
    {"symbol": "5801.T", "name": "古河電気工業", "market": "日股", "sector": "1.4", "industry": "1.4.2", "feature": "**高性能光学互联方案商**，光通信器件技术领先，CPO光电共封装核心供应商", "tags": ["硅光子"]},
    {"symbol": "5802.T", "name": "住友電気工業", "market": "日股", "sector": "1.4", "industry": "1.4.2", "feature": "**精密连接器龙头**，高速连接器市占率全球前三，数据中心互联核心", "tags": ["光模块"]},
    {"symbol": "5803.T", "name": "フジクラ(藤仓)", "market": "日股", "sector": "1.4", "industry": "1.4.2", "feature": "**高速光缆与光纤龙头**，光纤预制棒技术领先，数据中心光缆核心供应商", "tags": ["光纤光缆"]},
    {"symbol": "6834.T", "name": "精工技研", "market": "日股", "sector": "1.4", "industry": "1.4.2", "feature": "**精密光学组件供应商**，光通信连接器与适配器技术领先", "tags": ["光模块"]},
    {"symbol": "6777.T", "name": "santec", "market": "日股", "sector": "1.4", "industry": "1.4.2", "feature": "**光通信测试先驱**，高性能光学元器件与测试设备供应商", "tags": ["光芯片"]},

    # ============================================================
    # 赛道1.5：基础设施与能源
    # ============================================================

    # --- 能源/电力 ---
    {"symbol": "CEG", "name": "星座能源", "market": "美股", "sector": "1.5", "industry": "1.5.1", "feature": "**AI数据中心核电直供商**，美国最大核电运营商，AI算力清洁能源核心供应商", "tags": ["电力系统"]},
    {"symbol": "SBGSF", "name": "施耐德电气", "market": "美股", "sector": "1.5", "industry": "1.5.1", "feature": "**数据中心电力管理龙头**，全球市占率超25%，AI数据中心配电与冷却方案核心供应商", "tags": ["电力系统", "液冷设备"]},
    {"symbol": "ETN", "name": "伊顿", "market": "美股", "sector": "1.5", "industry": "1.5.1", "feature": "**全球电力管理巨头**，数据中心UPS/配电系统市占率全球前列，AI数据中心电力基础设施核心供应商", "tags": ["电力系统"]},
    {"symbol": "VRT", "name": "Vertiv(维谛技术)", "market": "美股", "sector": "1.5", "industry": "1.5.1", "feature": "**数据中心液冷与热管理龙头**，全球数据中心热管理市占率领先，AI算力液冷方案核心供应商", "tags": ["液冷设备", "电力系统"]},
    {"symbol": "6501.T", "name": "日立製作所", "market": "日股", "sector": "1.5", "industry": "1.5.1", "feature": "**基础设施能源巨头**，电网/变压器市占率全球前列，AI数据中心电力基础设施核心", "tags": ["电力系统"]},
    {"symbol": "6367.T", "name": "ダイキン工業(大金)", "market": "日股", "sector": "1.5", "industry": "1.5.2", "feature": "**数据中心高效冷却龙头**，全球空调市占率超20%，液冷技术领先", "tags": ["液冷设备"]},
    {"symbol": "485A.T", "name": "PowerX", "market": "日股", "sector": "1.5", "industry": "1.5.1", "feature": "**新型储能电池先锋**，AI数据中心储能方案新锐供应商", "tags": ["电力系统"]},
    {"symbol": "6503.T", "name": "三菱電機", "market": "日股", "sector": "1.5", "industry": "1.5.1", "feature": "**重型电力设备巨头**，数据中心电力基础设施核心供应商，电力电子技术领先", "tags": ["电力系统"]},
    {"symbol": "6504.T", "name": "富士電機", "market": "日股", "sector": "1.5", "industry": "1.5.1", "feature": "**能源基础设施与变流设备龙头**，功率半导体与电源方案核心供应商", "tags": ["电力系统"]},

    # --- 被动元件/传感器（数据中心配套）---
    {"symbol": "6981.T", "name": "村田製作所", "market": "日股", "sector": "1.5", "industry": "1.5.3", "feature": "**全球被动元器件霸主**，MLCC市占率超40%，AI服务器核心元器件供应商", "tags": ["MLCC"]},
    {"symbol": "6762.T", "name": "TDK", "market": "日股", "sector": "1.5", "industry": "1.5.3", "feature": "**电子元器件巨头**，磁性材料与传感器全球领先，AI数据中心元器件核心供应商", "tags": ["MLCC"]},
    {"symbol": "6976.T", "name": "太陽誘電", "market": "日股", "sector": "1.5", "industry": "1.5.3", "feature": "**高端MLCC与电感龙头**，中高端MLCC市占率全球前五，AI服务器被动元件核心供应商", "tags": ["MLCC"]},
    {"symbol": "6996.T", "name": "ニチコン(尼吉康)", "market": "日股", "sector": "1.5", "industry": "1.5.3", "feature": "**储能与充电系统供应商**，薄膜电容器技术领先，数据中心电源方案商", "tags": ["电力系统"]},

    # ============================================================
    # 赛道1.6：云服务与AI应用
    # ============================================================
    {"symbol": "MSFT", "name": "微软", "market": "美股", "sector": "1.6", "industry": "1.6.1", "feature": "**全球云服务龙头之一**，Azure云市占率超20%，AI基础设施投资领先，OpenAI独家合作伙伴", "tags": ["云服务IaaS", "基础模型"]},
    {"symbol": "AMZN", "name": "亚马逊", "market": "美股", "sector": "1.6", "industry": "1.6.1", "feature": "**全球云服务龙头**，AWS云市占率超30%，AI训练芯片Trainium/Inferentia自研，云计算绝对霸主", "tags": ["云服务IaaS"]},
    {"symbol": "GOOGL", "name": "谷歌", "market": "美股", "sector": "1.6", "industry": "1.6.1", "feature": "**AI基础设施巨头**，GCP云+TPU自研芯片，Gemini大模型生态领先，AI算力集群核心建设者", "tags": ["云服务IaaS", "基础模型"]},
    {"symbol": "CRWV", "name": "CoreWeave", "market": "美股", "sector": "1.6", "industry": "1.6.1", "feature": "**AI算力云服务龙头**，NVIDIA GPU算力租赁核心提供商，2025年纳斯达克上市，年营收超62亿美元", "tags": ["云服务IaaS"]},
    {"symbol": "PLTR", "name": "Palantir", "market": "美股", "sector": "1.6", "industry": "1.6.3", "feature": "**AI数据分析龙头**，政府/企业级AI决策平台，AIP平台赋能企业AI转型，AI应用赛道标杆", "tags": ["AI应用"]},

    # ============================================================
    # 赛道2.1：工业自动化与机器人
    # ============================================================
    {"symbol": "ROK", "name": "罗克韦尔自动化", "market": "美股", "sector": "2.1", "industry": "2.1.1", "feature": "**工业自动化集成方案巨头**，美国工业自动化市占率前三，智能制造核心方案商", "tags": ["数据中心架构"]},
    {"symbol": "688037.SH", "name": "埃斯顿", "market": "A股", "sector": "2.1", "industry": "2.1.1", "feature": "**中国工业机器人龙头**，伺服系统与控制器核心技术自主可控，国产替代主力军", "tags": ["数据中心架构"]},
    {"symbol": "002008.SZ", "name": "大族激光", "market": "A股", "sector": "2.1", "industry": "2.1.1", "feature": "**激光加工设备龙头**，中国激光设备市占率超20%，智能制造激光加工核心方案商", "tags": ["数据中心架构"]},
    {"symbol": "6861.T", "name": "キーエンス(基恩士)", "market": "日股", "sector": "2.1", "industry": "2.1.1", "feature": "**高精度传感系统霸主**，全球传感器市占率超40%，盈利能力冠绝工业自动化行业", "tags": ["数据中心架构"]},
    {"symbol": "6954.T", "name": "ファナック(发那科)", "market": "日股", "sector": "2.1", "industry": "2.1.1", "feature": "**工业机器人四大家族之一**，全球CNC市占率超50%，工厂自动化绝对龙头", "tags": ["数据中心架构"]},
    {"symbol": "6273.T", "name": "SMC", "market": "日股", "sector": "2.1", "industry": "2.1.1", "feature": "**全球气动元件霸主**，市占率超30%，工业自动化核心零部件供应商", "tags": ["数据中心架构"]},
    {"symbol": "6324.T", "name": "ハーモニック(Harmonic)", "market": "日股", "sector": "2.1", "industry": "2.1.1", "feature": "**精密减速器标杆**，谐波减速器全球市占率超50%，机器人关节核心部件供应商", "tags": ["数据中心架构"]},
    {"symbol": "6506.T", "name": "安川電機", "market": "日股", "sector": "2.1", "industry": "2.1.1", "feature": "**伺服驱动与机器人巨头**，全球伺服电机市占率前三，工业机器人四大家族之一", "tags": ["数据中心架构"]},
    {"symbol": "6594.T", "name": "ニデック(尼得科)", "market": "日股", "sector": "2.1", "industry": "2.1.1", "feature": "**全球电机霸主**，微型电机全球市占率超50%，机器人关节电机核心供应商", "tags": ["数据中心架构"]},
    {"symbol": "6645.T", "name": "オムロン(欧姆龙)", "market": "日股", "sector": "2.1", "industry": "2.1.1", "feature": "**传感与控制技术巨头**，PLC/传感器市占率全球前列，工业自动化方案核心供应商", "tags": ["数据中心架构"]},
    {"symbol": "SIE.DE", "name": "西门子", "market": "德股", "sector": "2.1", "industry": "2.1.1", "feature": "**全球工业自动化巨头**，PLC/工控系统市占率全球第一，数字孪生技术领先，AI+工业制造标杆", "tags": ["数据中心架构"]},

    # ============================================================
    # 赛道4.1：前沿航天与深科技
    # ============================================================

    # --- 航天/卫星 ---
    {"symbol": "SPCX", "name": "SpaceX", "market": "美股", "sector": "4.1", "industry": "4.1.1", "feature": "**全球航天发射龙头**，Starlink在轨卫星超6000颗，商业航天估值超2000亿美元", "tags": ["AI应用"]},
    {"symbol": "RKLB", "name": "Rocket Lab", "market": "美股", "sector": "4.1", "industry": "4.1.1", "feature": "**轻型火箭发射龙头**，Electron火箭发射次数全球第二，端到端航天系统方案商", "tags": ["AI应用"]},
    {"symbol": "ASTS", "name": "AST SpaceMobile", "market": "美股", "sector": "4.1", "industry": "4.1.1", "feature": "**太空蜂窝通信网络先驱**，全球首家实现手机直连卫星通信的商业航天公司", "tags": ["AI应用"]},
    {"symbol": "IRDM", "name": "铱星通信", "market": "美股", "sector": "4.1", "industry": "4.1.1", "feature": "**全球卫星通信运营商**，66颗低轨卫星星座，全球卫星通信服务核心提供商", "tags": ["AI应用"]},
    {"symbol": "9348.T", "name": "ispace", "market": "日股", "sector": "4.1", "industry": "4.1.1", "feature": "**日本首家月球探测商业公司**，月球着陆器技术领先，NASA商业月球载荷计划核心合作伙伴", "tags": ["AI应用"]},
    {"symbol": "186A.T", "name": "Astroscale", "market": "日股", "sector": "4.1", "industry": "4.1.1", "feature": "**全球轨道碎片治理先驱**，ELSA-d技术领先，太空可持续性解决方案领导者", "tags": ["AI应用"]},
    {"symbol": "6613.T", "name": "QDレーザ(QD激光)", "market": "日股", "sector": "4.1", "industry": "4.1.1", "feature": "**半导体激光器先驱**，高功率激光二极管技术领先，航天通信与探测核心器件供应商", "tags": ["光芯片"]},

    # --- 航空航天 ---
    {"symbol": "GE", "name": "GE Aerospace", "market": "美股", "sector": "4.1", "industry": "4.1.2", "feature": "**全球航空发动机巨头**，商用航空发动机市占率超50%，国防航空动力核心供应商", "tags": ["AI应用"]},
    {"symbol": "RTX", "name": "RTX Corporation", "market": "美股", "sector": "4.1", "industry": "4.1.2", "feature": "**全球顶级防务与航天系统集成商**，导弹与雷达系统市占率全球领先", "tags": ["AI应用"]},
    {"symbol": "BA", "name": "波音", "market": "美股", "sector": "4.1", "industry": "4.1.2", "feature": "**全球航空制造双寡头之一**，737MAX/787核心机型制造商，NASA商业载人航天核心合作伙伴", "tags": ["AI应用"]},
    {"symbol": "EADSY", "name": "空客", "market": "美股", "sector": "4.1", "industry": "4.1.2", "feature": "**全球航空制造双寡头之一**，A320/A350核心机型制造商，欧洲航天产业链核心", "tags": ["AI应用"]},
    {"symbol": "601989.SH", "name": "中国重工", "market": "A股", "sector": "4.1", "industry": "4.1.2", "feature": "**中国高端装备制造平台**，航母与大型舰船核心制造商，航天配套装备供应商", "tags": ["AI应用"]},
    {"symbol": "7011.T", "name": "三菱重工", "market": "日股", "sector": "4.1", "industry": "4.1.2", "feature": "**日本航空航天重工巨头**，H-IIA火箭制造商，航空发动机与防务装备核心制造商", "tags": ["AI应用"]},
    {"symbol": "7013.T", "name": "IHI", "market": "日股", "sector": "4.1", "industry": "4.1.2", "feature": "**航空发动机核心厂商**，日本唯一航空发动机整机制造商，军用/民用推进系统领先", "tags": ["AI应用"]},
    {"symbol": "5631.T", "name": "日本製鋼所", "market": "日股", "sector": "4.1", "industry": "4.1.2", "feature": "**大型铸锻件专家**，核工业与航空航天锻件核心供应商，特种材料技术领先", "tags": ["AI应用"]},
]
