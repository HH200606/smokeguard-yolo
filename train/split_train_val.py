"""划分抽烟识别数据集：trainval/test = 9:1，train/val = 9:1。

运行：python train/split_train_val.py
输入：data/Annotations/*.xml
输出：data/ImageSets/{trainval,train,val,test}.txt（每行一个图片编号，不含扩展名）
"""
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANN_DIR = ROOT / "data" / "Annotations"
OUT_DIR = ROOT / "data" / "ImageSets"

TRAINVAL_PERCENT = 0.9   # trainval 占总量比例
TRAIN_PERCENT = 0.9      # train 占 trainval 比例
SEED = 42                # 固定种子，保证划分可复现


def main():
    if not ANN_DIR.is_dir():
        raise SystemExit(f"找不到标注目录：{ANN_DIR}\n请先放置 VOC XML 文件。")

    names = sorted(p.stem for p in ANN_DIR.glob("*.xml"))
    if not names:
        raise SystemExit(f"{ANN_DIR} 中没有 XML 标注文件。")

    random.seed(SEED)
    total = len(names)
    indices = list(range(total))
    tv = int(total * TRAINVAL_PERCENT)
    tr = int(tv * TRAIN_PERCENT)

    trainval_idx = set(random.sample(indices, tv))
    train_idx = set(random.sample(sorted(trainval_idx), tr))

    splits = {
        "trainval": [names[i] for i in sorted(trainval_idx)],
        "test": [names[i] for i in indices if i not in trainval_idx],
        "train": [names[i] for i in sorted(train_idx)],
        "val": [names[i] for i in sorted(trainval_idx - train_idx)],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, items in splits.items():
        path = OUT_DIR / f"{name}.txt"
        path.write_text("\n".join(items) + "\n", encoding="utf-8")
        print(f"{name:9s}: {len(items):5d} -> {path.relative_to(ROOT)}")

    print(f"\n总计 {total} 张，比例：train {len(splits['train'])/total:.1%} / "
          f"val {len(splits['val'])/total:.1%} / test {len(splits['test'])/total:.1%}")


if __name__ == "__main__":
    main()
