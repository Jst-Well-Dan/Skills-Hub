<!-- source-sha256: c9efdcbb88eb6d16ac3b79aef52d89b0054a170ea94481b8b5522335990084f7 -->
---
name: sync-accelevents
description: 用于将 Accelevents 的演讲者头像、社交资料、个人简介和日程元数据同步到 AI Engineer Europe 的源数据和照片资源中。
---

# 同步 Accelevents 演讲者数据（欧洲）

从 Accelevents API 获取演讲者头像和社交资料，并同步到欧洲会议日程中。

## 前置条件

- 必须设置 `ACCELEVENTS_API_KEY` 环境变量（存储为 Devin 密钥）
- 需要安装了 Pillow 的 Python 3（`pip install Pillow`），用于图像优化

## 步骤

1. **检出一个新分支**
   ```bash
   cd /home/ubuntu/repos/aiecode2025
   git checkout main && git pull origin main
   git checkout -b devin/$(date +%s)-sync-accelevents
   ```

2. **运行同步脚本**
   ```bash
   cd /home/ubuntu/repos/aiecode2025/src/pages/europe/source/_scripts
   python3 sync_accelevents.py --save-snapshot
   ```
   该操作将：
   - 从 Accelevents API 获取所有演讲者
   - 下载或替换演讲者上传到门户的头像
   - 为网格视图优化过大的图像（>200KB），并将原图保留在 `large/` 中
   - 使用社交资料和个人简介数据更新 `schedule.json`（仅填充空白字段，不覆盖现有内容）
   - 将 API 快照保存到 `_accelevents/accelevents_speakers_latest.json`

   **参数：**
   - `--dry-run` — 显示将发生的更改，但不写入任何内容
   - `--headshots-only` — 跳过社交资料和个人简介更新
   - `--data-only` — 跳过头像下载
   - `--save-snapshot` — 保存原始 API 响应
   - `--optimize-existing --data-only` — 优化现有的过大照片

3. **重新导出 CSV**
   ```bash
   cd /home/ubuntu/repos/aiecode2025/src/pages/europe/source
   python3 _scripts/export_csv.py
   ```

4. **运行类型检查**
   ```bash
   cd /home/ubuntu/repos/aiecode2025
   SKIP_ENV_VALIDATION=1 npx tsc --noEmit
   ```

5. **提交所有更改**
   ```bash
   cd /home/ubuntu/repos/aiecode2025
   git add public/speakers/europe/ src/pages/europe/source/schedule.json src/pages/europe/source/_accelevents/ src/pages/europe/source/schedule_export.csv
   git commit -m "sync: pull speaker headshots + social data from Accelevents API"
   git push origin HEAD
   ```

6. **创建 PR 并验证**
   - 创建一个合并到 `main` 的 PR
   - 启动开发服务器：`SKIP_ENV_VALIDATION=1 pnpm dev`
   - 访问 `http://localhost:3000/europe#speakers`
   - 验证演讲者球形展示使用更新后的头像正常渲染，且没有损坏的图像
   - 截取屏幕截图并与用户分享

## 关键路径

- 脚本：`src/pages/europe/source/_scripts/sync_accelevents.py`
- 日程的事实来源：`src/pages/europe/source/schedule.json`
- 照片（针对网格视图优化）：`public/speakers/europe/`
- 照片（用于灯箱的完整尺寸版本）：`public/speakers/europe/large/`
- API 快照：`src/pages/europe/source/_accelevents/accelevents_speakers_latest.json`
- CSV 导出文件：`src/pages/europe/source/schedule_export.csv`

## 注意事项

- 该脚本按以下优先级将 API 演讲者与日程演讲者进行匹配：`acceleventsSpeakerId` > email > name
- 首次运行时，109 位演讲者中仅有 8 位上传了头像——该数字会随时间增长
- `pnpm lint` 无法在 Next.js 16 上运行；请改用 `npx tsc --noEmit` 进行类型检查
- 某些文档中提到的 `europe:source:sync-public` 脚本并不存在；同步脚本会直接写入 `public/speakers/europe/`
