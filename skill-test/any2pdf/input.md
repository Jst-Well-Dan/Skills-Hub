# SkillHub 入库测试报告

这是一份用于测试 `huashu-md-html` skill 的短文档。目标是验证 Markdown 到 HTML 的兜底流水线是否可运行，并确认产物具备基本排版结构。

## 测试范围

| 项目 | 预期 |
| --- | --- |
| 标题层级 | 保留 h1 / h2 / h3 |
| 表格 | 渲染为可读表格 |
| 引用 | 转换为明确的引用块 |
| 代码 | 保留等宽代码块 |

> 好的文档流水线应该把 Markdown 当作源代码，把 HTML 当作可发布产物。

## 示例代码

```js
const workflow = ["import", "extract", "document", "validate"];
console.log(workflow.join(" -> "));
```

## 结论

如果这个文件能稳定转换为 HTML，说明基础模板、Pandoc 调用和输出路径都工作正常。
