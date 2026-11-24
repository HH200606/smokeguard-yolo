"""把 YOLO 训练日志 runs/detect/train/results.csv 转成网页可用的曲线数据。

运行：python tools/plot_results.py
输出：assets/results_data.json（包含 loss / mAP 两组序列，以及可直接粘贴的 JS 片段）
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "runs" / "detect" / "train" / "results.csv"
OUT_PATH = ROOT / "assets" / "results_data.json"


def pick(row, *candidates):
    """兼容不同 ultralytics 版本的列名。"""
    for name in candidates:
        if name in row and row[name]:
            try:
                return float(row[name])
            except ValueError:
                continue
    return None


def main():
    if not CSV_PATH.exists():
        raise SystemExit(f"找不到训练日志：{CSV_PATH}\n请先完成模型训练。")

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    loss = {"box_loss": [], "cls_loss": [], "dfl_loss": []}
    map_ = {"map50": [], "map5095": []}
    epochs = []
    for row in rows:
        epochs.append(int(float(row.get("epoch", len(epochs) + 1))))
        loss["box_loss"].append(pick(row, "train/box_loss"))
        loss["cls_loss"].append(pick(row, "train/cls_loss"))
        loss["dfl_loss"].append(pick(row, "train/dfl_loss"))
        map_["map50"].append(pick(row, "metrics/mAP50(B)", "metrics/mAP_0.5"))
        map_["map5095"].append(pick(row, "metrics/mAP50-95(B)", "metrics/mAP_0.5:0.95"))

    def compact(seq):
        return [round(v, 5) if v is not None else None for v in seq]

    payload = {
        "epochs": epochs,
        "loss": {k: compact(v) for k, v in loss.items()},
        "map": {k: compact(v) for k, v in map_.items()},
        "note": "将 index.html 中 drawChart 的 makeSeries(...) 数据替换为这里的数组即可展示真实曲线。",
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已导出 {len(rows)} 个 epoch 的真实曲线数据 -> {OUT_PATH.relative_to(ROOT)}")
    print("替换方式：把 index.html 中 drawChart($('#lossChart'), [...]) 与 drawChart($('#mapChart'), [...]) ")
    print("里的 data: makeSeries(...) 分别改成 results_data.json 中 loss / map 对应数组。")


if __name__ == "__main__":
    main()
