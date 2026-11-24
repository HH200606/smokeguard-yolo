"""YOLOv8 吸烟行为检测训练入口。

运行：python train/smoking_train.py
依赖：pip install ultralytics
输出：runs/detect/train/weights/best.pt
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "train" / "smoking.yaml"
LOCAL_PRETRAINED = ROOT / "yolov8s.pt"


def main():
    try:
        from ultralytics import YOLO
    except ImportError:
        raise SystemExit("缺少 ultralytics，请先执行：pip install ultralytics")

    txts = [ROOT / "data" / f"{s}.txt" for s in ("train", "val")]
    missing = [p for p in txts if not p.exists()]
    if missing:
        raise SystemExit("缺少数据列表，请先运行：\n  python train/split_train_val.py\n  python train/voc_label.py\n缺失文件：" + str(missing))

    try:
        import torch
        device = 0 if torch.cuda.is_available() else "cpu"
    except ImportError:
        device = "cpu"

    weights = str(LOCAL_PRETRAINED) if LOCAL_PRETRAINED.exists() else "yolov8s.pt"
    model = YOLO(weights)

    results = model.train(
        data=str(DATA),
        epochs=200,
        imgsz=640,
        batch=16,
        workers=0,          # Windows 下建议保持 0
        device=device,      # 有 GPU 自动用 0，否则 cpu
        project=str(ROOT / "runs" / "detect"),
        name="train",
        exist_ok=True,
    )

    metrics = model.val(data=str(DATA), split="test", imgsz=640, device=device)
    print("\n==== 训练完成 ====")
    print("最佳权重：", ROOT / "runs" / "detect" / "train" / "weights" / "best.pt")
    print("mAP@0.5  :", getattr(metrics, "box", None) and metrics.box.map50)
    print("mAP@.5:.95:", getattr(metrics, "box", None) and metrics.box.map)
    print("提示：运行 python tools/plot_results.py 可导出真实曲线数据供网页使用。")


if __name__ == "__main__":
    main()
