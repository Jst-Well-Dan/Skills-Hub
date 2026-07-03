# Worked frame 范例（两 mold 各一张，真生过图验过）

照搬改 frame 即可。frame 只写「画什么」（继刚作主角的构图 + 隐喻物件 + 中文标注），**风格词不用写**——`gen_illustration.py` 的 `--mold` 已内置风格 DNA。

## 概念：《非对称风险》遍历性

意向画面（见 extraction.md 示例 A）：很多人各玩一次平均 +5%；但「你」沿一条时间线走，路上一道吸收壁（破产/归零，进去出不来），正期望也通向归零。继刚 = 那个走时间线的「你」。

### mold -a（动物森友会，默认）

```bash
python3 assets/gen_illustration.py --mold a \
  --frame "On the RIGHT, the villager-man walks alone along a single narrowing wooden plank tilting toward a dark whirlpool pit in teal water (an absorbing trap, fall in and cannot climb out). On the UPPER-LEFT, a row of cute Animal-Crossing villagers strolls on a flat safe grassy path. Labels: 你一个人玩很久 (near the man) / 很多人各玩一次 +5% (near villagers) / 一道吸收壁 (small wooden sign by the hole) / 进去出不来 (under the hole)." \
  --out /tmp/ljg_lib_ergodicity_a.png
```

出图：继刚作动森村民走木板奔向青水漩涡，村民群在安全草径，木牌「一道吸收壁」「进去出不来」。验过：~/Downloads/非对称风险-取景框卡-动森.png（整卡）、proto-ergodicity-animalcrossing.png。

### mold -c（pixel + cyber-hacker）

```bash
python3 assets/gen_illustration.py --mold c \
  --frame "On the RIGHT, the protagonist sprite walks alone along a single narrowing cyan neon-pixel bridge tilting down toward a glitching dark VOID portal (corrupted black hole, magenta glitch rim) at the right edge. On the UPPER-LEFT, a row of small green pixel-sprite figures walks along a flat safe neon lane. Labels: 你一个人玩很久 (near the man) / 很多人各玩一次 +5% (near the crowd) / 一道吸收壁 (near the void) / 进去出不来 (under the void)." \
  --out /tmp/ljg_lib_ergodicity_c.png
```

出图：继刚作霓虹像素精灵走青桥奔向洋红故障漩涡，绿像素人群在安全道。验过：proto-ergodicity-cyber-jigang-v2.png。

## 写 frame 的复用要点

- **主角先定位**：继刚（你）在哪、朝哪、在做什么核心动作。
- **隐喻物件落实**：把抽象命题换成可见物（木板/桥/漩涡/驾驶座/旧车…）。
- **对比/流向**：谁在安全侧、谁在危险侧、信息/箭头朝哪。
- **标注 3-5 个、每个 2-8 字**，标清挂在哪个元素旁。
- **风格交给 --mold**，frame 里别写"动森/像素/霓虹"这类风格词（会和内置 DNA 打架）。
- 生图后**必 Read 验**：继刚认得出、画面读得懂、中文不糊；不行调 frame 重生。
