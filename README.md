# my-stock-web 

# 📊 全球 AI 硬科技决策终端

> 全球 AI 硬科技核心标的监控与决策平台


## 🚀 项目简介

本项目是一个面向全球 AI 硬科技赛道的**股票数据监控与决策终端**，覆盖美股、日股、A股、韩股、德股等市场的核心标的，提供实时数据展示、主题分类筛选、估值分析等功能。


## 📁 项目结构
```
my-stock-web/
├── .github/workflows/
│ └── auto_update.yml # GitHub Actions 自动更新数据
├── api/
│ └── refresh.js # Vercel Serverless 刷新中转 API
├── components/
│ ├── navbar.css # 导航栏样式
│ └── navbar.js # 导航栏组件（所有页面共用）
├── data/
│ ├── data.json # 股票数据（由 update_data.py 生成）
│ └── stock_cache.json # 数据缓存（加速 yfinance 请求）
├── docs/
│ ├── md.html # 通用 Markdown 渲染器
│ ├── index.json # 文档索引（标题映射）
│ ├── WATCHLIST_SUMMARY.md # 标的总结文档
│ └── SEMICONDUCTOR_INDUSTRY.md # 半导体产业链全景
├── pages/
│ ├── index.html # 首页（按 sector/industry 分组）
│ ├── sub_ai.html # テーマ別（按 THEME_MAPPING 分组）
│ └── settings.html # 策略配置（开发中）
├── scripts/
│ └── update_data.py # 数据采集脚本
├── config.py # 配置文件（WATCHLIST + THEME_MAPPING）
├── vercel.json # Vercel 路由配置
└── README.md
```


## 📊 数据分类系统（重要）

本项目使用**两套独立的分类系统**，分别服务于不同页面：

### 1. `index.html`（首页）：sector + industry

| 字段 | 用途 | 说明 |
|------|------|------|
| **sector** | 一级分组 | 大板块分类（如「1. 算力芯片+先进封装+存储」） |
| **industry** | 二级分组 | 细分领域（如「AI处理器/算力芯片」「半导体设备」） |

**数据流：**
```
WATCHLIST
↓
每个股票自带 sector + industry
↓
按 sector 分组 → 按 industry 分组
↓
在 index.html 显示股票卡片
```

**示例：**
```
📂 1. 算力芯片+先进封装+存储
└── 📁 AI处理器/算力芯片
├── NVIDIA (NVDA)
├── AMD (AMD)
└── 沐曦股份 (688802.SH)

```


### 2. `sub_ai.html`（テーマ別）：tags → THEME_MAPPING

| 字段 | 用途 | 说明 |
|------|------|------|
| **tags** | 标签列表 | 每个股票的打标签（如 `["GPU", "CPU"]`） |
| **THEME_MAPPING** | 主题映射 | 定义 tags 的分组规则（在 `config.py` 中配置） |

**数据流：**
```
THEME_MAPPING（硬编码分类）
↓
每个股票有 tags
↓
根据 tags 匹配到 THEME_MAPPING 中的分类
↓
在 sub_ai.html 按主题显示股票
```

**示例：**
```
📂 1. 半导体设备
├── 🏷️ 光刻机
│ ├── ASML
│ └── 尼康
├── 🏷️ 刻蚀设备
│ ├── 泛林半导体
│ └── 东京电子
└── ...
```


### 3. 两套系统的对应关系

| 页面 | 分类依据 | 数据来源 | 用途 |
|------|---------|----------|------|
| `index.html` | `sector` + `industry` | WATCHLIST 自带字段 | 按行业板块浏览 |
| `sub_ai.html` | `tags` → `THEME_MAPPING` | tags 匹配主题映射 | 按技术主题筛选 |

> ⚠️ **注意**：新增标的时，**必须同时填写** `sector`、`industry` 和 `tags` 三个字段，才能在两个页面都正确显示。


## 🔧 配置说明

### `config.py` 核心配置

| 配置项 | 说明 |
|--------|------|
| `MACRO_LIST` | 宏观指数列表（大盘数据） |
| `WATCHLIST` | 核心标的池（所有股票数据） |
| `THEME_MAPPING` | 主题分类映射（用于 sub_ai.html） |
| `DEFAULT_STRATEGY` | 默认数据源策略 |
| `SOURCE_MAP` | 特定股票的数据源配置 |

### `WATCHLIST` 字段说明

```python
{
    "symbol": "NVDA",           # 股票代码
    "name": "NVIDIA(英伟达)",    # 公司名称
    "market": "美股",            # 市场：美股/日股/A股/韩股/德股
    "sector": "1. 算力芯片+先进封装+存储",  # 首页一级分组
    "industry": "AI处理器/算力芯片",        # 首页二级分组
    "feature": "**全球AI芯片绝对霸主**...", # 公司简介（**加粗**）
    "tags": ["GPU", "CPU"]      # 标签（用于 sub_ai 主题匹配）
}

```
数据自动更新

通过 GitHub Actions 定时执行（工作日每 15 分钟一次）：

    早盘：北京时间 08:00 - 10:30（UTC 00:00 - 02:30）

    午盘：北京时间 11:30 - 14:30（UTC 03:30 - 06:30）

也可通过页面「🔄 召唤云端强刷」按钮手动触发。
🛠️ 技术栈
组件	技术
前端	原生 HTML/CSS/JavaScript
数据采集	Python + yfinance + Requests
自动化	GitHub Actions
部署	Vercel
数据源	Yahoo Finance、新浪财经、腾讯财经
📝 文档

    标的总结 - 全部标的分类汇总

    半导体产业链全景 - 产业链深度梳理

📄 License

MIT License
```

---

## ✅ 主要新增内容

| 新增章节 | 说明 |
|---------|------|
| 数据分类系统（重要） | 详细说明两套分类系统的区别和使用方法 |
| 项目结构 | 更新了最新的目录结构 |
| 配置说明 | 说明 `config.py` 和 `WATCHLIST` 字段 |
| 文档链接 | 添加了在线文档的访问链接 |

直接复制替换你的 `README.md` 即可！🎯

