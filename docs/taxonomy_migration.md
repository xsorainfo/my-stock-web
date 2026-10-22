# Taxonomy migration

项目当前处于 dual-write 阶段。股票条目继续保留旧字段，同时由 `scripts/update_data.py`
写入规范化字段：

- `market`
- `sector_id`
- `industry_id`
- `theme_ids`
- `tag_ids`
- `taxonomy`

目录来源：

- `data/sector_catalog.json`
- `data/theme_catalog.json`
- `data/tag_catalog.json`
- `data/taxonomy_schema.json`

## 检查

本地运行：

```bash
python scripts/validate_taxonomy.py
python scripts/taxonomy_report.py
```

校验脚本会检查市场、行业、主题和标签 ID 是否存在于目录中。报告同时显示
`config.WATCHLIST` 与生成后的 `data/data.json` 覆盖率，避免把“配置尚未迁移”
误判成“生成流程没有写入”。

## 导出迁移快照

如需审阅完整的规范化结果：

```bash
python scripts/export_normalized_watchlist.py --output data/watchlist_normalized.json
```

该命令不会修改 `config.py`，只生成可审阅的 JSON 快照。确认目录和映射无误后，
再把需要的字段回写到配置，最后继续保留旧字段一段时间以兼容旧页面。

## 回滚

本次重构在独立分支 `refactor/taxonomy-normalization` 完成，基线分支为
`backup/pre-taxonomy-refactor-2026-10-22`。如需回滚，恢复基线即可；main
分支在合并前不会受到影响。
