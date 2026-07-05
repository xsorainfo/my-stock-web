# my-stock-web

📊 全球 AI 硬科技决策终端 — 面向多市场（美股/日股/A股/港股/韩股/德股）的核心标的监控与决策平台。

一个以原生静态页面为前端、Python 数据采集脚本为后端数据生产线、通过 GitHub Actions 定时更新并部署到 Vercel 的轻量化决策终端。

---

## 技术栈（Stack）
- Language(s): HTML (前端)、Python (数据采集与打包)、JavaScript (页面交互)
- Runtime / Hosting: Vercel（静态站点 + Serverless API）
- Notable libraries / tools:
  - yfinance（主要的数据抓取，历史价格/行情）
  - requests（抓取第三方财经 API，如新浪/腾讯）
  - GitHub Actions（自动抓取与更新 data.json）

---

## What this is
本仓库实现了一个以 WATCHLIST 列表为中心的「股票/主题监控面板」，把多源行情数据抓取成统一的 data.json，前端页面（pages/ 下的静态 HTML）读取并展示：
- index.html：按 sector → industry 分组展示核心标的卡片
- sub_ai.html：按 THEME_MAPPING（主题映射）展示基于 tag 的主题视图

目标用户：对全球 AI / 硬科技产业链感兴趣的研究员、投研人、个人投资者。

---

## 项目结构（重要目录说明）

```text
my-stock-web/
├── .github/workflows/    # CI：定时/事件触发的自动更新（auto_update.yml）
├── api/                  # Vercel Serverless 后端（/api/refresh.js）
├── components/           # 公共前端组件：样式与脚本（navbar, common, footer）
├── config.py             # 核心配置：WATCHLIST、MACRO_LIST、DEFAULT_STRATEGY、SOURCE_MAP
├── data/                 # 由脚本生成的运行时数据（data.json, stock_cache.json）
├── docs/                 # 项目文档与说明（md 渲染器、文档索引、行业/主题文档）
├── pages/                # 静态页面（index.html、sub_ai.html、settings.html(开发中)）
├── scripts/              # 数据抓取与打包脚本（scripts/update_data.py）
├── vercel.json           # Vercel 路由/部署配置
└── README.md             # (你正在阅读的文件)
```

How it fits together:
- scripts/update_data.py 负责读取 config.WATCHLIST 与 MACRO_LIST、调用 yfinance / 新浪 / 腾讯 等数据源，生成统一的 data/data.json（包含 macro、stocks、theme_mapping、tag_display_map 等字段）。
- GitHub Actions 定时触发 update 脚本并将 data.json 提交到仓库或触发静态站点的重建。
- Vercel 承载 pages/ 下的静态 HTML，并通过 api/refresh.js 提供「页面触发刷新」的后端中转（需要配置 MY_REPO_TOKEN）。
- 前端组件（components/common.js / navbar.js / footer.js）负责渲染通用交互；各页面只聚焦页面特有的布局与渲染逻辑。

---

## 核心配置说明
- config.py
  - WATCHLIST：主要的标的池，每个标的应包含字段：symbol、name、market、sector、industry、feature、tags。
  - MACRO_LIST：宏观与 ETF 指标列表（用于首页顶部/折叠展示）。
  - DEFAULT_STRATEGY / SOURCE_MAP：定义抓取顺序与特殊标的的数据源策略。
- THEME_MAPPING
  - 主题映射（在仓库中以 theme_mapping.py 管理），用于 sub_ai.html 中把 tags 对应到主题树（一级/二级/三级）。
- TAG_DISPLAY_MAP
  - 可选的 tag 显示映射（tag_display_map.py），用于把内部 tags 映射为面向用户的显示名称。

注意：新增标的时建议同时补齐 sector、industry 与 tags，以保证 index.html 与 sub_ai.html 两套视图都能正确展示。

---

## 环境变量（Environment variables）
本项目在部署到 Vercel 时使用了少量环境变量以保障页面触发数据刷新等功能：

- MY_REPO_TOKEN (required for /api/refresh)
  - 说明：Vercel 后端函数 api/refresh.js 使用此 token 调用 GitHub repository dispatch API，为页面提供“召唤云端强刷”的能力。
  - 在 Vercel 中设置：Project Settings → Environment Variables → 添加 `MY_REPO_TOKEN`，在 Production/Preview/Development 根据需要选择。
  - 最佳实践：使用短期有效的 Personal Access Token（PAT），并限制其权限与有效期；不要在代码或公共配置中暴露该值。

最小权限建议（建议的最小范围）：
- 公共仓库 (public repo)：为 repository_dispatch 调用，建议使用带有 `public_repo` 范围的 PAT 可满足触发公开仓库的 dispatch。若不确定，使用 `repo` 权限。
- 私有仓库 (private repo)：需要 `repo` 全权限（包含 repository dispatch）。

更安全的替代方案：
- 使用 GitHub App（推荐）来替代 PAT：为 GitHub App 授予仅 repository_dispatch 权限（或触发 workflow 权限），并在 Vercel 后端使用 App 的 installation token，这能提供更细粒度与可撤销的权限控制。

安全建议：
- 为 PAT 设置短期过期、仅在需要时重新生成。
- 在 Vercel 中把变量设为 Environment Variable（而非公開设置），并定期轮换。
- 如果团队协作，优先使用 GitHub App + least-privilege 模型。

---

## 如何在本地运行（最短路径）
1. 克隆仓库并进入目录：

```bash
git clone https://github.com/xsorainfo/my-stock-web.git
cd my-stock-web
```

2. 建议使用虚拟环境并安装依赖（示例）：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install yfinance requests
```

说明：yfinance 会依赖 pandas，若不存在会自动安装。若你需要完整依赖锁文件，请创建 requirements.txt 并列出所需包。

3. 生成 data/data.json（单次抓取）

```bash
python3 scripts/update_data.py
```

脚本会读取 config.py 与 theme_mapping.py、tag_display_map.py（若存在），抓取 macro 与 WATCHLIST 中的行情并把结果写入 data/data.json。

4. 本地预览静态页面（任意静态服务器）：

```bash
# Python 内建静态服务器（在仓库根目录下运行）
python3 -m http.server 8000
# 然后在浏览器打开 http://localhost:8000/pages/index.html
```

或使用 Vercel CLI 部署：

```bash
# 需已登录 vercel
vercel --prod
```

---

## 部署与自动更新
- Vercel：仓库中包含 vercel.json，可直接部署。pages/ 目录为主要静态页面，api/ 包含后端中转函数。
- 自动更新：.github/workflows/auto_update.yml 定时触发脚本生成/更新 data.json（仓库中已有工作流，按工作日每 15 分钟/指定时间段运行）。
- 页面手动刷新：前端页面可调用 /api/refresh（api/refresh.js），需要在 Vercel 后台配置环境变量 MY_REPO_TOKEN（用于触发 GitHub repository_dispatch）。

---

## 常见操作与提示
- 新增标的：编辑 config.py 的 WATCHLIST，补齐 symbol、market、sector、industry、tags 与 feature，随后手动运行 scripts/update_data.py 或等待 Actions 自动更新。
- 调试抓取失败：scripts/update_data.py 有丰富的日志输出（抓取源切换、异常堆栈），建议在本地运行并观察控制台输出；同时检查 data/stock_cache.json 缓存文件是否损坏。
- 支持市场：脚本已支持美股/日股/A股/港股/韩股/德股（通过 symbol 后缀判断），并在抓取策略中做分流处理。

---

## 开发者想问
- 我如何把新的第三方数据源（例如 AlphaVantage）加入到抓取策略并在 SOURCE_MAP 中优雅地降级？
- 想把前端改为单页应用（React / Svelte），哪些模块（文件）是迁移的关键切入点？
- data.json 的 schema（fields）在哪些地方被前端强依赖？有哪些字段不能随意删除或重命名？

---

## License
MIT
