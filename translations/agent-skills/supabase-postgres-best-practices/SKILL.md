<!-- source-sha256: ccd6e4596bd51cf344fe76c464867c541ccc16b6d90ae7a9db449fb17588613b -->
---
name: supabase-postgres-best-practices
description: 来自 Supabase 的 Postgres 性能优化与最佳实践。在编写、审查或优化 Postgres 查询、模式设计或数据库配置时使用此技能。
license: MIT
metadata:
  author: supabase
  version: "1.1.1"
  organization: Supabase
  date: 2026年1月
  abstract: 面向使用 Supabase 和 Postgres 的开发者的综合 Postgres 性能优化指南。包含横跨 8 个类别的性能规则，并按照影响程度从关键（查询性能、连接管理）到渐进改进（高级功能）进行优先级排序。每条规则都包含详细说明、错误与正确 SQL 示例对比、查询计划分析，以及用于指导自动优化和代码生成的具体性能指标。
---

# Supabase Postgres 最佳实践

由 Supabase 维护的 Postgres 综合性能优化指南。包含横跨 8 个类别的规则，并按照影响程度确定优先级，以指导自动查询优化和模式设计。

## 何时应用

在以下情况下参考这些准则：
- 编写 SQL 查询或设计模式
- 实现索引或查询优化
- 审查数据库性能问题
- 配置连接池或扩展
- 针对 Postgres 特有功能进行优化
- 使用行级安全性（RLS）

## 按优先级划分的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 查询性能 | 关键 | `query-` |
| 2 | 连接管理 | 关键 | `conn-` |
| 3 | 安全性与 RLS | 关键 | `security-` |
| 4 | 模式设计 | 高 | `schema-` |
| 5 | 并发与锁定 | 中高 | `lock-` |
| 6 | 数据访问模式 | 中 | `data-` |
| 7 | 监控与诊断 | 中低 | `monitor-` |
| 8 | 高级功能 | 低 | `advanced-` |

## 使用方法

阅读各个规则文件以获取详细说明和 SQL 示例：

```
references/query-missing-indexes.md
references/query-partial-indexes.md
references/_sections.md
```

每个规则文件包含：
- 对其重要性的简要说明
- 附带解释的错误 SQL 示例
- 附带解释的正确 SQL 示例
- 可选的 EXPLAIN 输出或指标
- 补充背景和参考资料
- Supabase 特定说明（如适用）

## 参考资料

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security
