<!-- source-sha256: be0040976e3b405c6e800ec23f061a6c89c76c44ecd29957f712f00696daf9f6 -->
---
name: mockup-device-3d
zh_name: "iPhone × MacBook 立体展架"
en_name: "设备 3D 展示台"
emoji: "📱"
description: "iPhone + MacBook 仿 GLTF 静态展架，屏幕内嵌真实 HTML 内容，玻璃镜头折射，360° 转盘构图"
category: poster
scenario: product
aspect_hint: "1920×1080 (16:9)"
featured: 47
tags: ["device", "mockup", "iphone", "macbook", "html-in-canvas", "product"]
example_id: sample-mockup-device-3d
example_name: "iPhone × MacBook 立体展架"
example_format: markdown
example_tagline: "HTML-in-Canvas 设备展示"
example_desc: "iPhone 屏幕 + MacBook 屏幕均嵌入真实 UI 内容，呈现玻璃镜头折射效果"
example_source_url: "https://hyperframes.heygen.com/catalog"
example_source_label: "hyperframes · vfx-iphone-device"
---

【模板：设备 3D 展架（设备 3D 展示台 / HTML-in-Canvas）】
【意图】产品发布、App 演示、设计稿展示。将用户提供的 UI 内容真实渲染到 iPhone / MacBook “屏幕”中，周围使用 CSS 3D transform 模拟 GLTF 模型的玻璃 / 高光 / 折射效果。灵感来自 hyperframes vfx-iphone-device。

【硬性构图】
- **画布**：1920×1080，暖灰渐变背景 `radial-gradient(#1a1a1f → #0a0a0f)`，底部反射地面（镜面渐变）。
- **iPhone 15 Pro 模型**：位于左侧 / 中部，`transform: rotateY(-12deg) rotateX(4deg) translateZ(40px)`；边框使用钛金属银 `#a8a8ad`（实心 4px）+ 屏幕圆角 56px；屏幕内嵌类似 iframe 的 div，真实渲染用户的 HTML 内容（移动端视口 375×812）。
- **MacBook Pro 14"**（可选第二台）：位于右侧，略小，`rotateY(8deg)`；上盖屏幕嵌入桌面端视口内容（1440×900 缩放）；底座键盘 + 触控板使用 CSS 阴影线条绘制（不绘制键帽细节）。
- **玻璃 / 镜头光斑**：顶部添加 2-3 个使用 `radial-gradient(ellipse, rgba(255,255,255,0.4) 0%, transparent 60%)` 的椭圆高光，模拟形变玻璃镜头。
- **地面反射**：设备下方使用 `transform: scaleY(-1)` + `mask-image: linear-gradient(to bottom, rgba(0,0,0,0.4), transparent 70%)`。

【屏幕内容来源】
- 用户提供文本/数据 → 自动渲染为模拟 App 界面（顶部状态栏 + 标题 + 正文 + 底部标签栏或主屏幕指示条）。
- 用户提供 HTML → 原样嵌入屏幕 div 内（注意使用缩放 transform 使其适配屏幕宽高）。
- 屏幕内 UI 使用 Tailwind，字号应遵循移动端真实尺寸（text-sm / text-base，不要使用 text-9xl）。

【可选附加元素】
- 右下角“产品短标识”角标：大号 logo + 一行标语 + 细线副标题。
- 顶部一行说明文字（英文无衬线字体、小字号、透明度 0.6）：产品代号 / 日期 / 版本。
- 添加 8s 自动 CSS 转盘动画：`@keyframes turntable` rotateY -12 ↔ 12, ease-in-out infinite alternate；可通过 `prefers-reduced-motion` 关闭。

【设计细节】
- **绝不**：使用外部 mockup 图片 URL（任何 unsplash / dribbble 链接），所有设备均使用 CSS / SVG 绘制。
- 字体：设备外的说明文字 / logo 使用 `Inter Tight` / `SF Pro` 风格；设备内根据用户内容自适应。
- 背景可选 4 套配色：炭黑 / 珍珠白 / 午夜蓝 / 摩卡色；不要使用彩虹渐变。
- 单文件 HTML；iframe 不要使用 srcdoc 嵌套（容易出问题），使用 `<div class="screen">` + Tailwind 渲染内容。
- 必须使用用户的真实数据填充屏幕内容，严禁使用 lorem ipsum 或“在此输入文字”。
