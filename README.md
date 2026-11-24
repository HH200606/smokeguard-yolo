# SmokeGuard · YOLO 吸烟行为检测可视化平台

**在线体验（GitHub Pages）**：https://hh200606.github.io/smokeguard-yolo/

**源码仓库**：https://github.com/HH200606/smokeguard-yolo

一个**可直接用浏览器打开**的吸烟行为检测可视化项目。参考 [CSDN 文章《抽烟识别数据集 6953 张》](https://blog.csdn.net/kyriehan/article/details/143464989) 的数据规格与训练流程，提供数据集解析、训练监控、交互检测演示以及真实 YOLO 模型的接入链路。

> **重要说明**：原始数据集（6953 张图片）与训练权重需通过原文章渠道获取，本项目不包含这些数据。上传图片和摄像头走**浏览器端真实 YOLO 推理**；内置矢量插画场景没有真实目标，仍使用演示框展示交互。训练曲线为示意数据。按本文第 3 节启动本地后端后，可切换到自己训练的模型。

---

## 1. 打开网页

本项目提供两个版本，按需选择：

| 文件 | 用途 | 体积 | 打开方式 |
| --- | --- | --- | --- |
| `index.html` | **在线版 / GitHub Pages**（推荐） | 636 KB | 通过网页服务器访问；首次检测时自动加载 `models/` 与 `assets/` 下的模型文件，之后浏览器缓存 |
| `smokeguard-offline.html` | **离线单文件版** | 31 MB | 双击即可，模型和运行时全部内嵌，无需联网 |

**在线版（推荐，首屏秒开）**：把整个目录用网页服务器托管即可，例如 `python -m http.server 8080` 后访问 `http://localhost:8080/index.html`；或直接用上面的 GitHub Pages 链接。首次点击「开始检测」时会下载约 23 MB 的模型与运行时（按钮旁有加载提示），此后再检测无需重复下载。

**完全离线（双击打开）**：双击 `smokeguard-offline.html`。它是完整内嵌的单文件，不依赖外部资源。由于体积 31 MB，网络打开会很慢，仅建议本地使用。

> 早期的 `smokeguard-v5.html` 现与 `index.html` 内容相同，仅用于绕过某些预览面板的缓存。

> 摄像头在部分浏览器里要求安全上下文；若 `file://` 下摄像头被拒绝，用在线版或启动本地服务器访问即可。上传图片检测在两种方式下都可用。

页面包含 5 个模块：

| 模块 | 内容 |
| --- | --- |
| 项目总览 | 数据规模、类别、划分比例、训练配置、应用链路 |
| 数据集解析 | 类别分布、标注格式示例、四类场景样本预览 |
| 训练监控 | 损失曲线、mAP 曲线、超参数表、训练命令 |
| 检测演示 | 内置场景、上传图片、摄像头、置信度/IoU 调节、检测框与统计 |
| 接入指南 | 从数据到部署的四步教程、API 说明、FAQ |

顶部状态胶囊可切换「浏览器端 YOLO / 本地后端」；右上角按钮切换明暗主题。

---

## 2. 项目结构

```text
SmokeGuard/
├── index.html                 # 在线主页面（636 KB，模型外置按需加载）
├── smokeguard-offline.html    # 离线单文件版（31 MB，模型+wasm 全内嵌，双击即用）
├── assets/
│   ├── ort-wasm-simd.wasm     # ONNX Runtime Web 非线程 wasm（在线版按需加载）
│   └── results_data.json      # 可选：训练后导出的真实曲线数据
├── models/
│   └── smoking_v8n.onnx       # 吸烟/烟雾检测 ONNX 模型（在线版按需加载）
├── train/
│   ├── split_train_val.py     # 数据集划分
│   ├── voc_label.py           # VOC XML -> YOLO TXT
│   ├── smoking.yaml           # 数据集配置（nc=1, names=['smoking']）
│   └── smoking_train.py       # YOLOv8s 训练入口
├── server/
│   ├── app.py                 # FastAPI 推理接口
│   └── requirements.txt       # 后端依赖
├── tools/
│   └── plot_results.py        # results.csv -> 网页曲线数据
└── README.md
```

---

## 3. 使用自己训练的 YOLO 模型推理（可选）

> 页面默认已能真实检测，无需本节。本节仅用于换成你用自己的数据集训练出的 `best.pt`。

### 步骤 1：准备数据集

按原文章渠道获取数据集后，按如下结构放置：

```text
data/
├── images/         # 6953 张 jpg 图片
├── Annotations/    # 对应的 Pascal VOC XML 标注
└── ImageSets/      # 空目录，后续脚本会写入划分列表
```

### 步骤 2：划分与格式转换

```bash
python train/split_train_val.py   # train 5631 / val 626 / test 696（SEED=42 可复现）
python train/voc_label.py         # 生成 data/labels/*.txt 与 data/{train,val,test}.txt
```

### 步骤 3：训练模型

```bash
pip install ultralytics
python train/smoking_train.py
```

脚本要点与文章一致：`yolov8s.pt` 预训练、`epochs=200`、`imgsz=640`、`batch=16`、`workers=0`，并自动判断是否有 CUDA（无 GPU 时使用 `cpu`）。训练完成后权重在：

```text
runs/detect/train/weights/best.pt
```

### 步骤 4：启动本地后端并切换模式

```bash
pip install -r server/requirements.txt
python server/app.py
```

服务运行在 `http://127.0.0.1:8000`。回到网页「检测演示」页：

1. 点击顶栏状态胶囊，切换到**本地后端**；
2. 点击「检测后端状态」确认模型已加载；
3. 上传图片或打开摄像头，点击「开始检测」。

> 本地后端模式需要实际画面输入；内置矢量场景仅在默认浏览器推理模式下用于演示交互。

---

## 4. 后端接口

**GET `/health`** — 查看模型加载状态。

**POST `/detect`** — `multipart/form-data`，字段 `file`（图片）、可选 `conf`、`iou`。

```json
{
  "count": 2,
  "detections": [
    {"class": "smoking", "confidence": 0.9123, "box": [301, 173, 356, 256], "normalized": false}
  ],
  "image_size": [640, 480],
  "elapsed_ms": 42.6
}
```

`box` 为原图像素坐标 `[x1, y1, x2, y2]`，网页会自动映射到显示区域。

可用环境变量：`SMOKE_MODEL`（指定权重路径）、`SMOKE_DEVICE`（如 `0` 或 `cpu`）。

---

## 5. 替换为真实训练曲线

```bash
python tools/plot_results.py
```

生成 `assets/results_data.json`，其中含训练损失与 mAP 的真实数组。把 `index.html` 中 `drawChart(...)` 里的 `makeSeries(...)` 数据替换为对应数组即可（页面顶部「训练监控」的示意数据提示也可一并移除）。

---

## 6. 数据集规格（来自参考文章）

- 图像总量：**6953** 张 JPG，人工标注
- 类别：**1 类**，`names: ['smoking']`
- 标注格式：Pascal VOC XML + YOLO TXT
- 场景：园区、禁烟区、监控视角、无人机俯视；包含行人视角与俯视视角
- 划分逻辑：先 `trainval:test = 9:1`，再 `train:val = 9:1`
- 训练配置：`yolov8s.pt`、`epochs=200`、`imgsz=640`、`batch=16`、`workers=0`

脚本对参考博客做了两处工程修正：VOC→YOLO 转换中移除了中心点坐标错误的 `-1` 偏移；`difficult` 字段缺失时按 0 处理并过滤越界框。

---

## 7. 常见问题

**Q：网页里的检测结果是真的吗？**
是。上传图片和摄像头画面走**浏览器端真实 YOLO 推理**，模型与 wasm 运行时已内嵌在 `index.html` 中，双击即可用。只有内置矢量插画场景使用演示框（插画本身没有真实目标）。想用自己训练的模型，请按第 3 节操作并切换到本地后端模式。

**Q：上传真人照片为什么没有框？**
这个模型识别的是**香烟 / 烟雾等吸烟线索**，不是人脸或人体。普通人像、没有可见香烟或烟雾的照片不会触发。若人物确实在吸烟但烟雾很淡、香烟很小，请把置信度阈值降到 **0.10**（当前默认值），并使用清晰近景。已实测：一张近距离香烟照片在阈值 0.10 下可检出 1 个目标（置信度约 0.14），在 0.25 下会被过滤掉。

**Q：没有 GPU 能训练吗？**
可以，脚本会自动切换到 CPU，只是 200 轮训练耗时较长。也可把 `epochs` 调小做流程验证。

**Q：能换成自己的类别吗？**
修改 `train/smoking.yaml` 的 `nc`/`names`，同步修改 `train/voc_label.py` 中的 `CLASSES`，然后重新转换标签并训练。

**Q：摄像头打不开，提示 "Invalid security origin"？**
WorkBuddy 右侧预览是沙箱 iframe，浏览器禁止其中的页面调用摄像头。点击检测页的**「在新窗口打开」**按钮，在独立浏览器窗口中使用摄像头；或双击本地 `index.html` / 启动 `python -m http.server 8080` 后访问 `http://localhost:8080`。上传图片检测在预览面板里完全可用，不受影响。

---

## 8. 内置模型来源

- 模型：`MeetCool/yolov8n-smoking-detection`（Hugging Face，ONNX 导出版），输入 640×640，3 类别输出：`cls0=cigarette（香烟）`、`cls1=person（人物，已过滤）`、`cls2=smoke（烟雾）`。网页只保留香烟与烟雾两类，避免人物大框干扰。
- 运行时：ONNX Runtime Web **1.16.3**（MIT 许可，非线程 wasm 版本，不加载任何 `.mjs` 工作线程脚本），模型与 wasm 均已 base64 内嵌到 HTML 中，完全离线运行。
- 该模型为公开权重，精度有限；生产场景请使用第 3 节流程在参考数据集上训练自己的模型。

*本项目仅用于目标检测技术学习与可视化演示。请遵守当地法律法规与公共场所禁烟规定。*
