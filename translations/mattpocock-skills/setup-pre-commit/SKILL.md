<!-- source-sha256: 872f4037cb7e6e0e340d4175c086550072959925dffc87b160d1a30dc9f63bbd -->
---
name: setup-pre-commit
description: 在当前仓库中使用 lint-staged（Prettier）、类型检查和测试设置 Husky pre-commit hooks。当用户希望添加 pre-commit hooks、设置 Husky、配置 lint-staged，或添加提交时的格式化、类型检查和测试时使用。
---

# 设置 Pre-Commit Hooks

## 此配置包含的内容

- **Husky** pre-commit hook
- **lint-staged** 对所有已暂存文件运行 Prettier
- **Prettier** 配置（如果缺失）
- pre-commit hook 中的 **typecheck** 和 **test** scripts

## 步骤

### 1. 检测包管理器

检查是否存在 `package-lock.json`（npm）、`pnpm-lock.yaml`（pnpm）、`yarn.lock`（yarn）、`bun.lockb`（bun）。使用已存在的包管理器。如果无法确定，默认使用 npm。

### 2. 安装依赖

将以下依赖安装为 devDependencies：

```
husky lint-staged prettier
```

### 3. 初始化 Husky

```bash
npx husky init
```

这会创建 `.husky/` 目录，并将 `prepare: "husky"` 添加到 package.json。

### 4. 创建 `.husky/pre-commit`

写入以下内容（Husky v9+ 无需 shebang）：

```
npx lint-staged
npm run typecheck
npm run test
```

**按需调整**：将 `npm` 替换为检测到的包管理器。如果仓库的 package.json 中没有 `typecheck` 或 `test` script，则省略相应行并告知用户。

### 5. 创建 `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. 创建 `.prettierrc`（如果缺失）

仅当不存在 Prettier 配置时创建。使用以下默认值：

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. 验证

- [ ] `.husky/pre-commit` 存在且可执行
- [ ] `.lintstagedrc` 存在
- [ ] package.json 中的 `prepare` script 为 `"husky"`
- [ ] Prettier 配置存在
- [ ] 运行 `npx lint-staged` 验证其是否正常工作

### 8. 提交

暂存所有已更改或创建的文件，并使用以下消息提交：`Add pre-commit hooks (husky + lint-staged + prettier)`

这会运行新配置的 pre-commit hooks，是检验所有配置是否正常工作的有效冒烟测试。

## 注意事项

- Husky v9+ 的 hook 文件不需要 shebang
- `prettier --ignore-unknown` 会跳过 Prettier 无法解析的文件（图像等）
- pre-commit 会先运行 lint-staged（速度快，仅处理已暂存文件），然后运行完整的类型检查和测试
