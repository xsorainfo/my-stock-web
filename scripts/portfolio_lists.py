# scripts/portfolio_lists.py
# リスト別　ポートフォリオ定義（銘柄リスト）

PORTFOLIO_LISTS = {
    "HuaQi": {
        "name": "花期",
        "icon": "🇯🇵",
        "description": "花期",
        "symbols": [
            "285A.T", "8058.T", "8802.T", "6758.T", "7261.T",
            "6264.T", "5016.T", "7014.T", "6055.T", "6752.T",
            "5706.T", "7003.T", "8309.T", "5802.T", "6976.T",
            "1812.T", "1570.T", "1357.T", "546A.T","8410.T"
        ]
    },
    "JiuWanli": {
        "name": "九万里",
        "icon": "🇯🇵",
        "description": "九万里",
        "symbols": [
            "285A.T", "8058.T", "8802.T", "6758.T", "7261.T",
            "6264.T", "5016.T", "7014.T", "6055.T", "6752.T",
            "5706.T", "7003.T", "8309.T", "5802.T", "6976.T",
            "1812.T", "1570.T", "1357.T", "546A.T"
        ]
    },
    "DongTao": {
        "name": "东涛",
        "icon": "🇯🇵",
        "description": "东涛",
        "symbols": [
            "6340.T", "8058.T", "8802.T", "6758.T", "7261.T",
            "6264.T", "5016.T", "7014.T", "6055.T", "6752.T",
            "5706.T", "7003.T", "8309.T", "5802.T", "6976.T",
            "1812.T", "1570.T", "1357.T", "546A.T"
        ]
    },
    # ===== 著名投資家 =====
    "buffett": {
        "name": "バフェット",
        "icon": "🧔",
        "description": "Warren Buffett バークシャー・ハサウェイ",
        "symbols": [
            "AAPL", "BAC", "AXP", "KO", "CVX",
            "OXY", "KHC", "MCO", "TMO", "DVA"
        ]
    },
    "blackrock": {
        "name": "ブラックロック",
        "icon": "🏛️",
        "description": "BlackRock 世界最大の資産運用会社",
        "symbols": [
            "AAPL", "MSFT", "NVDA", "AMZN", "META",
            "GOOGL", "BRK.B", "LLY", "VTI", "IVV"
        ]
    },
    "vanguard": {
        "name": "バンガード",
        "icon": "📈",
        "description": "Vanguard 世界最大のインデックス運用会社",
        "symbols": [
            "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL",
            "META", "BRK.B", "JPM", "VTI", "BND"
        ]
    },
    "softbank": {
        "name": "ソフトバンク",
        "icon": "🗼",
        "description": "SoftBank Group ビジョンファンド",
        "symbols": [
            "9984.T", "ARM", "NVDA", "TCEHY",
            "Uber", "CMCSA", "ALNY", "PACB"
        ]
    },

    # ===== AIハードウェア =====
    "ai_semiconductor": {
        "name": "AI半導体",
        "icon": "🧠",
        "description": "AI半導体関連（GPU・HBM・製造設備）",
        "symbols": [
            "NVDA", "AMD", "INTC", "TSM", "AVGO",
            "MU", "AMAT", "LRCX", "KLAC", "ASML"
        ]
    },
    "ai_data_center": {
        "name": "AIデータセンター",
        "icon": "☁️",
        "description": "AIデータセンター・クラウド基盤",
        "symbols": [
            "AMZN", "MSFT", "GOOGL", "META", "ORCL",
            "SNOW", "CRWD", "PLTR", "DELL", "SMCI"
        ]
    },

    # ===== 日本株 =====
    "japan_semiconductor": {
        "name": "日本半導体",
        "icon": "🇯🇵",
        "description": "日本半導体・電子部品",
        "symbols": [
            "4062.T", "6857.T", "8035.T", "6762.T", "6981.T",
            "6954.T", "6506.T", "6324.T", "3110.T", "5803.T"
        ]
    },
    "japan_robotics": {
        "name": "日本ロボット",
        "icon": "🤖",
        "description": "日本ロボット・FA関連",
        "symbols": [
            "6954.T", "6506.T", "6324.T", "6594.T", "6479.T",
            "6273.T", "6481.T", "6501.T", "6503.T", "6383.T"
        ]
    },

    # ===== ユーザー追加用 =====
    # "my_watchlist": {
    #     "name": "マイリスト",
    #     "icon": "⭐",
    #     "description": "自分が注目している銘柄",
    #     "symbols": ["NVDA", "TSM", "4062.T", "6857.T"]
    # },
}
