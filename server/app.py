"""SmokeGuard 本地推理后端（FastAPI + Ultralytics YOLO）。

启动：python server/app.py
接口：
  GET  /health   查看模型加载状态
  POST /detect   上传图片做吸烟检测（multipart/form-data，字段名 file）

前端网页默认处于演示模式，启动本服务后可在网页顶栏切换为真实模型。
"""
import io
import os
import time
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = Path(os.environ.get("SMOKE_MODEL", str(ROOT / "runs" / "detect" / "train" / "weights" / "best.pt")))
DEVICE = os.environ.get("SMOKE_DEVICE", "cpu")

app = FastAPI(title="SmokeGuard Detection API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许本地 file:// 页面（Origin: null）访问
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
model_error = None


@app.on_event("startup")
def load_model():
    global model, model_error
    if not MODEL_PATH.exists():
        model_error = f"权重文件不存在：{MODEL_PATH}。请先完成训练，或设置环境变量 SMOKE_MODEL 指向 best.pt。"
        print("[SmokeGuard]", model_error)
        return
    try:
        from ultralytics import YOLO
        model = YOLO(str(MODEL_PATH))
        print("[SmokeGuard] 模型已加载：", MODEL_PATH)
    except Exception as exc:  # pragma: no cover
        model_error = f"模型加载失败：{exc}"
        print("[SmokeGuard]", model_error)


@app.get("/health")
def health():
    return {
        "status": "ok" if model is not None else "degraded",
        "model": str(MODEL_PATH) if model is not None else None,
        "device": DEVICE,
        "message": "running" if model is not None else model_error,
    }


@app.post("/detect")
async def detect(
    file: UploadFile | None = File(default=None),
    conf: float = Form(default=0.35),
    iou: float = Form(default=0.45),
    scene: str | None = Form(default=None),
):
    t0 = time.perf_counter()
    if model is None:
        return JSONResponse(status_code=503, content={"error": model_error or "模型未加载"})

    if file is None:
        return {
            "count": 0,
            "detections": [],
            "elapsed_ms": 0,
            "message": f"未收到图片（scene={scene}）。真实模式请上传图片或打开摄像头。",
        }

    try:
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    except Exception as exc:
        return JSONResponse(status_code=400, content={"error": f"图片解析失败：{exc}"})

    results = model.predict(
        source=image, imgsz=640, conf=conf, iou=iou,
        device=DEVICE, verbose=False,
    )

    detections = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = [round(v, 1) for v in box.xyxy[0].tolist()]
        detections.append({
            "class": "smoking",
            "confidence": round(float(box.conf[0]), 4),
            "box": [x1, y1, x2, y2],
            "normalized": False,
        })

    return {
        "count": len(detections),
        "detections": detections,
        "image_size": list(image.size),
        "elapsed_ms": round((time.perf_counter() - t0) * 1000, 1),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
