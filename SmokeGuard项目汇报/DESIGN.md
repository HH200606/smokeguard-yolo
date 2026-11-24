# DESIGN.md — SmokeGuard 技术项目汇报

## 全局视觉约定

### ① 画布与安全区
- 画布 1280×720（16:9），页面 padding 上下左右各 60px，内容区 1160×600（x 60–1220 / y 60–660）
- 页眉 y 60–110；标题 y 110–160；内容 y 176–650；页脚顶边 y=670，字号 14px
- 封面 / 检测效果高潮页 / 结尾可全出血；其余内容页严格在安全区内

### ② 配色方案（科技未来 · 深色冲击）
| 槽位 | 取值 |
|---|---|
| 主色 accent | `#63A7D4` |
| 辅色 surface / line | `#232C37` / `#60676F` |
| 强调色 | accent 主色，关键数字与结论专用，一页 ≤2–3 处 |
| 底色 bg | `#0B1521` |
| 正文色 | ink `#FFFFFF` / secondary `#A9CFE7` / body `#E7E8E9` / muted `#C9CCCE` |
| 深色块 deep_bg / on_deep | `#0B1521` / `#FFFFFF` |
| 主色深档 / 浅档 | `#0F1920` / `#B9D7EC` |
| 点缀色 | 冷蓝紫 `#4DA3FF` |
| 图表系列色 1→6 | `#24428F` `#3A5CBC` `#63A7D4` `#8FBCE4` `#E3F1F8` `#13263B` |
| 呼吸页浅底（P4 / P8） | `#E3F1F8`，深字 `#253649` |

- 色彩面积：深底主色点缀 ≤10%，辅色 ≤30%；Hero 页强调色可达 15–20%

### ③ 字体系统
- 中文标题 / 正文：Noto Sans SC（思源黑体），标题 Bold
- 西文 / 数字：Arial Narrow（仅标题与大数字，窄体），正文西文随 Noto Sans SC
- 说明：模板推荐字体 Barlow Condensed / Source Han Sans SC 在渲染环境缺失，改用系统真实存在的 Arial Narrow / Noto Sans SC，避免测量回退
- 字号阶梯：封面主标 88px / 章节大字 64px / 巨型数据 88px / 页面主标 36px / 卡片小标 24px / 正文 18px / 标签 16px / 脚注 14px
- 中西文间加半角空格；正文行距 1.5

### ④ 视觉母题
- 内容页主标题下 1px 贯通细线（底色→主色混 35%），仅标题一处
- 页脚左下 `SG / 编号`，右下页码；封面 / 目录 / 章节 / 高潮 / 结尾不显示页脚

### ⑤ 配图清单（统一摄影级科技风）
| 文件 | 用途 | 生成方式 | 真实内容 | 使用页 |
|---|---|---|---|---|
| `assets/cover_hero.png` | 主角 | ImageGen | 监控视角吸烟场景 + 红色检测框 | P1 封面 |
| `assets/tech_vision.png` | 主角 | ImageGen | AI 神经网络检测烟雾的抽象可视化 | P3 项目概述 |
| `assets/detect_office.png` | 证据 | ImageGen | 手部香烟与烟雾特写 + 红色检测框 | P7 检测效果 |

统一风格词：cinematic photorealistic, dark navy blue surveillance/AI atmosphere, cool cyan-blue rim lighting, glowing red detection bounding boxes, no text, no watermark, high detail.

---

## 逐页设计

### P1 封面
- title: SmokeGuard · YOLO 吸烟行为检测可视化平台
- type: cover / role: hero / rhythm: peak
- layout: 满版图 + 渐变蒙层
- visual: L1 `cover_hero.png` 满版出血，底部深→透明蒙层，标题压在下部
- density: 字数约 60 / 图 1 张 / 留白约 45%
- anti_pattern: 禁止文字投影；禁止四卡片预览；禁止页脚页码
- description: 项目名、一句话定位、技术标签「YOLOv8 · ONNX Runtime Web · 零依赖单文件」

### P2 目录
- title: 目录 / CONTENTS
- type: catalog / role: transition / rhythm: transition
- layout: 经典纵排
- visual: 六章编号 + 名称 + 页码三列对齐，1px 行分隔线
- density: 字数约 90 / 图 0 / 留白约 55%
- anti_pattern: 禁止卡片容器 / 行底色填充；禁止每章简述
- description: 项目概述、数据集与标注、技术路线、核心方案、实测效果、部署与使用

### P3 项目概述
- title: 一个可在浏览器直接运行的吸烟检测平台
- type: content / role: supporting / rhythm: valley
- layout: 左图右文（6:4）
- visual: L1 `tech_vision.png` 占左 60%，右侧三段文字 + 底部结论条
- density: 字数约 200 / 图 1 张 / 留白约 22%
- anti_pattern: 禁止 50:50 等分双栏；禁止对称卡片组
- description: 平台定位、浏览器端真实 YOLO 推理、零依赖单文件（31MB 内嵌模型+wasm）、禁烟监管/监控场景

### P4 数据集与标注
- title: 6953 张标注图像，9:1 两级划分
- type: content / role: supporting / rhythm: valley
- layout: 数据展示（多图看板）+ 浅底呼吸
- visual: 巨型数字 6953 + doughnut 划分比例 + 类别/格式要点
- density: 字数约 180 / 图表 2 / 留白约 28%
- anti_pattern: 禁止三等分卡片；禁止图表等大均分
- description: 6953 张 JPG、单类 smoking、Pascal VOC XML + YOLO TXT、trainval:test=9:1 与 train:val=9:1、四类场景

### P5 技术路线
- title: 从数据到检测：六步闭环
- type: content / role: supporting / rhythm: valley
- layout: 流程链（g）
- visual: 六阶段 SVG 流程链 + 箭头 + 阶段输出条
- density: 字数约 160 / 图 1 / 留白约 25%
- anti_pattern: 禁止并列卡片；禁止阶段 >6
- description: 数据采集 → 标注转换 → YOLOv8s 训练 → ONNX 导出 → 浏览器推理 → 结果可视化，标注每步产物

### P6 核心技术方案
- title: 浏览器端真实推理：640×640 到检测框
- type: content / role: supporting / rhythm: valley
- layout: 左标题色块 + 右内容（m）
- visual: 左侧主色块大标题，右侧四段技术要点 + 类别过滤说明
- density: 字数约 240 / 图 0 / 留白约 20%
- anti_pattern: 禁止等宽多栏；禁止用卡片罗列递进步骤
- description: 图像直接 resize 到 640×640 RGB CHW、ONNX Runtime Web wasm、输出 [1,7,8400] 解析、NMS、只保留 cls0 香烟与 cls2 烟雾并过滤 person、object-fit:fill 坐标对齐

### P7 检测效果实测
- title: 真实照片：烟雾与香烟被准确定位
- type: content / role: hero / rhythm: peak
- layout: 左图右文（7:3）+ 满版图氛围
- visual: L1 `detect_office.png` 占左 70%，右侧两组结果数据
- density: 字数约 120 / 图 1 张 / 留白约 25%
- anti_pattern: 禁止对半分；禁止把核心数据塞进图角落
- description: smoke 0.58 框(336,243,53,211)、cigarette 0.32 框(393,548,20,20)，阈值 0.10，红框分别落在烟雾柱与手部香烟

### P8 训练监控
- title: 200 轮训练：损失收敛与 mAP 提升
- type: content / role: supporting / rhythm: valley
- layout: 数据展示（单图主图）+ 浅底呼吸
- visual: L1 lineChart 损失曲线占 62%，右侧 mAP 要点 + 脚注标注示意数据
- density: 字数约 130 / 图表 1 / 留白约 26%
- anti_pattern: 禁止所有图等大均分；禁止图旁无洞察
- description: yolov8s、epochs=200、imgsz=640、batch=16、workers=0；损失下降 / mAP 上升；曲线为示意数据，可用工具替换为真实 results.csv

### P9 部署与使用
- title: 双击即用：三种打开方式
- type: content / role: supporting / rhythm: valley
- layout: 三栏非均分（c）
- visual: 主栏「本地双击」+ 两副栏「本地服务器 / 在线 Pages」，各配小图标
- density: 字数约 180 / 图 0 / 留白约 24%
- anti_pattern: 禁止等宽三栏；禁止对称罗列
- description: index.html 双击离线运行；python -m http.server 8080 供摄像头安全上下文；GitHub Pages 在线链接；可选 FastAPI 后端切换本地模型

### P10 成果与亮点
- title: 四项能力，构成完整检测闭环
- type: content / role: supporting / rhythm: valley
- layout: 巨型数字 + 洞察（数据卡片组 + 底部结论条）
- visual: 四个不等大数字锚点（6953 / 0 / 31MB / 100%）+ 底部 accent 满底结论条
- density: 字数约 150 / 图 0 / 留白约 30%
- anti_pattern: 禁止等宽卡片横排；禁止把数字塞进卡片角落
- description: 6953 张数据规模、0 服务器依赖、31MB 单文件、100% 浏览器端推理；结论「从数据集到可交互检测，全流程可复现」

### P11 结尾
- title: 在线体验与源码
- type: ending / role: hero / rhythm: peak
- layout: 收束金句 + 落款
- visual: 居中大字金句 + 在线地址 / 仓库地址两行链接 + 落款
- density: 字数约 80 / 图 0 / 留白约 55%
- anti_pattern: 禁止只写「谢谢」占整页；禁止页脚页码
- description: 金句「让禁烟监管，从人工值守走向智能识别」+ GitHub Pages 在线链接 + 仓库链接 + 项目落款
