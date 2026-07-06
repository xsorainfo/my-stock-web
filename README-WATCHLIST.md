如何正确地增加 `WATCHLIST`。

---

## 📊 三个配置文件的关系图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         数据流转全景图                               │
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │   config.py         │  ← 你在这里添加 WATCHLIST
                    │   WATCHLIST = [...] │
                    └──────────┬──────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         scripts/update_data.py                      │
│  1. 读取 WATCHLIST                                                  │
│  2. 读取 theme_mapping.py (主题层级)                                │
│  3. 读取 tag_display_map.py (标签映射)                              │
│  4. 读取 sector_mapping.json (板块名称/注释)                        │
│  5. 抓取数据 → 合并 → 生成 data/data.json                          │
└──────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   data/data.json    │  ← 前端读取这个文件
                    └─────────────────────┘

┌──────────────┬──────────────────┬───────────────────────────────────┐
│  配置文件    │   作用           │   谁使用                          │
├──────────────┼──────────────────┼───────────────────────────────────┤
│ config.py    │ 定义 WATCHLIST   │ update_data.py 读取              │
│              │ (股票池+原始tags) │                                   │
├──────────────┼──────────────────┼───────────────────────────────────┤
│ theme_       │ 定义主题树结构   │ update_data.py 读取               │
│ mapping.py   │ (一级→二级→三级) │ → 用于匹配 tag → theme_path       │
│              │ + 二级注释       │ → 输出 theme_mapping + theme_descriptions │
├──────────────┼──────────────────┼───────────────────────────────────┤
│ tag_display_ │ 定义标签统一名   │ update_data.py 读取               │
│ map.py       │ (原始tag→显示名) │ → 用于转换 display_tags           │
│              │                  │ → 输出 tag_display_map            │
├──────────────┼──────────────────┼───────────────────────────────────┤
│ sector_      │ 定义板块显示名   │ index.html 读取                   │
│ mapping.json │ + 板块注释       │ → 用于显示 sector/industry 名称   │
│              │                  │ → 前端直接读取                    │
└──────────────┴──────────────────┴───────────────────────────────────┘
```

---

## 🔗 详细逻辑关系

### 1. `tag_display_map.py` → 标签统一化

```python
# tag_display_map.py
TAG_DISPLAY_MAP = {
    "EUV": "EUV (极紫外光刻)",      # 原始tag → 显示名
    "极紫外光刻": "EUV (极紫外光刻)", # 统一所有变体
    "Mask": "光掩膜 (Mask)",
    "光掩模": "光掩模",
    # ...
}
```

**作用**：把 `config.py` 中 `WATCHLIST` 里各种不统一的 `tags` 统一成标准名称。

**数据流**：
```
config.py 中的 tags: ["EUV", "光掩模", "Mask"]
        ↓
tag_display_map.py 转换
        ↓
display_tags: ["EUV (极紫外光刻)", "光掩模", "光掩膜 (Mask)"]
```

### 2. `theme_mapping.py` → 主题树 + 注释

```python
# theme_mapping.py
THEME_MAPPING = {
    "1. 半导体设备": {
        "光刻机": {
            "tags": ["EUV (极紫外光刻)", "ArF", ...],
            "description": "光刻机是半导体制造中最核心的设备..."
        }
    }
}
```

**作用**：
- 定义三级主题层级（一级→二级→三级）
- 为二级分类提供 `description`（注释）
- `update_data.py` 用它来匹配每个标签的 `theme_path`

**数据流**：
```
display_tags 中的 "EUV (极紫外光刻)"
        ↓
在 theme_mapping 中查找
        ↓
找到: ["1. 半导体设备", "光刻机", "EUV (极紫外光刻)"]
        ↓
生成 tag_themes: {tag: "EUV (极紫外光刻)", theme_path: [...]}
```

### 3. `sector_mapping.json` → 板块显示名 + 注释

```json
// data/sector_mapping.json
{
  "sector_mapping": [
    {
      "sector_id": "1.2",
      "sector_name": "半导体设备",
      "sector_comment": "半导体制造核心设备...",
      "industries": [
        {
          "industry_id": "1.2.1",
          "industry_name": "光刻机",
          "industry_comment": "光刻机是...核心设备"
        }
      ]
    }
  ]
}
```

**作用**：
- 为 `config.py` 中的 `sector` 和 `industry` 代码提供显示名称
- 在 `index.html` 中显示为中文名称和注释

**数据流**：
```
config.py 中: sector="1.2", industry="1.2.1"
        ↓
sector_mapping.json 查找
        ↓
index.html 显示: "半导体设备" > "光刻机"
```

---

## 📝 如何添加新的 WATCHLIST

### ✅ 完整操作步骤

当你要添加一只新股票时，需要按以下顺序操作：

#### Step 1: 在 `config.py` 的 `WATCHLIST` 中添加股票

```python
# config.py
WATCHLIST = [
    # ... 现有股票 ...
    
    # ⭐ 新增股票
    {
        "symbol": "股票代码",           # 美股: AAPL, 日股: 6758.T, A股: 600519.SS
        "name": "显示名称",
        "sector": "1.2",               # 从 sector_mapping.json 中找对应的 sector_id
        "industry": "1.2.1",           # 从 sector_mapping.json 中找对应的 industry_id
        "feature": "**行业地位**：描述\n**主营业务**：描述\n**竞争优势**：描述\n**未来方向**：描述",
        "tags": ["原始tag1", "原始tag2", "原始tag3"],  # 尽量使用统一的标签
        "market": "美股"                # 美股/日股/A股/韩股/德股
    },
]
```

#### Step 2: 确保 `tags` 中的标签能被映射

检查 `tag_display_map.py` 是否包含所有原始 tag：

```python
# tag_display_map.py - 添加缺失的映射
TAG_DISPLAY_MAP = {
    # ... 现有映射 ...
    "新原始tag": "新显示名",  # 如果需要添加
}
```

#### Step 3: 确保 `theme_mapping.py` 包含这些标签

```python
# theme_mapping.py - 确保标签存在于正确的主题树下
THEME_MAPPING = {
    "1. 半导体设备": {
        "光刻机": {
            "tags": [
                # ... 现有标签 ...
                "新显示名",  # 必须与 tag_display_map 中的显示名一致
            ],
            "description": "..."
        }
    }
}
```

#### Step 4: 确保 `sector_mapping.json` 包含对应的 sector/industry

如果使用了新的 `sector_id` 或 `industry_id`，需要添加：

```json
// data/sector_mapping.json
{
  "sector_mapping": [
    {
      "sector_id": "1.2",
      "sector_name": "新板块名",
      "sector_comment": "新板块注释",
      "industries": [
        {
          "industry_id": "1.2.1",
          "industry_name": "新子板块名",
          "industry_comment": "新子板块注释"
        }
      ]
    }
  ]
}
```

#### Step 5: 运行数据更新脚本

```bash
python scripts/update_data.py
```

#### Step 6: 部署到 Vercel

```bash
git add .
git commit -m "add new stock: xxx"
git push
```

---

## 📋 快速添加新股票的指令模板

当你需要添加新股票时，可以直接给我以下信息，我会帮你生成完整的配置代码：

```
【新增股票】
- 代码: 6758.T
- 名称: 索尼
- 板块ID: 3.2
- 子板块ID: 3.2.1
- 描述: **行业地位**：全球消费电子巨头\n**主营业务**：游戏、音乐、电影、传感器\n**竞争优势**：PS生态、CMOS传感器市占率第一\n**未来方向**：AI游戏、车载传感器
- 标签: [消费电子, 游戏, CMOS传感器, AI]
```

我会自动：
1. 检查 `tag_display_map.py` 是否需要添加新映射
2. 检查 `theme_mapping.py` 是否需要添加新标签
3. 生成完整的 `config.py` 新增条目
4. 检查 `sector_mapping.json` 是否需要补充

---

## 🎯 总结

| 配置文件 | 作用 | 何时修改 |
|---------|------|---------|
| **config.py** | 定义股票池 + 原始标签 | **每次添加新股票时修改** |
| **tag_display_map.py** | 统一标签名称 | 当新标签需要映射时修改 |
| **theme_mapping.py** | 定义主题树 + 注释 | 当新标签需要归属主题时修改 |
| **sector_mapping.json** | 板块显示名 + 注释 | 当新板块需要显示时修改 |

**最小操作流程**：大多数情况下，你只需要：
1. 在 `config.py` 的 `WATCHLIST` 中添加股票
2. 确保 `tags` 使用的标签在 `theme_mapping.py` 中已存在
3. 运行 `python scripts/update_data.py`
4. 部署
