"""Pascal VOC XML -> YOLO TXT 标注转换。

运行：python train/voc_label.py
输入：data/Annotations/*.xml + data/ImageSets/{train,val,test}.txt
输出：data/labels/*.txt + data/{train,val,test}.txt（图片绝对路径列表）

说明：相比参考博客做了两处工程修正：
  1) 中心点坐标不再减 1（博客中的 `- 1` 会引入半个像素的系统偏移）；
  2) difficult 字段缺失时按 0 处理，并跳过标注越界的无效框。
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETS = ("train", "val", "test")
CLASSES = ("smoking",)


def convert(size, box):
    """(xmin, xmax, ymin, ymax) -> 归一化 (cx, cy, w, h)"""
    dw, dh = 1.0 / size[0], 1.0 / size[1]
    cx = (box[0] + box[1]) / 2.0
    cy = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return cx * dw, cy * dh, w * dw, h * dh


def convert_annotation(image_id, label_dir):
    in_file = ROOT / "data" / "Annotations" / f"{image_id}.xml"
    out_file = label_dir / f"{image_id}.txt"
    tree = ET.parse(in_file)
    root = tree.getroot()

    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)
    if w <= 0 or h <= 0:
        return 0

    lines = []
    for obj in root.iter("object"):
        name_el = obj.find("name")
        if name_el is None or name_el.text not in CLASSES:
            continue
        diff_el = obj.find("difficult")
        if diff_el is not None and diff_el.text and int(float(diff_el.text)) == 1:
            continue

        xmlbox = obj.find("bndbox")
        xmin = float(xmlbox.find("xmin").text)
        xmax = float(xmlbox.find("xmax").text)
        ymin = float(xmlbox.find("ymin").text)
        ymax = float(xmlbox.find("ymax").text)
        # 越界修正并过滤无效框
        xmin, xmax = max(0.0, xmin), min(float(w), xmax)
        ymin, ymax = max(0.0, ymin), min(float(h), ymax)
        if xmax <= xmin or ymax <= ymin:
            continue

        cx, cy, bw, bh = convert((w, h), (xmin, xmax, ymin, ymax))
        cls_id = CLASSES.index(name_el.text)
        lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")

    out_file.write_text("".join(lines), encoding="utf-8")
    return len(lines)


def main():
    label_dir = ROOT / "data" / "labels"
    label_dir.mkdir(parents=True, exist_ok=True)
    total_boxes = 0
    for image_set in SETS:
        list_file = ROOT / "data" / "ImageSets" / f"{image_set}.txt"
        if not list_file.exists():
            print(f"跳过 {image_set}：缺少 {list_file}")
            continue
        ids = list_file.read_text(encoding="utf-8").strip().split()
        out_list = ROOT / "data" / f"{image_set}.txt"
        with out_list.open("w", encoding="utf-8") as f:
            for image_id in ids:
                f.write(str(ROOT / "data" / "images" / f"{image_id}.jpg") + "\n")
                total_boxes += convert_annotation(image_id, label_dir)
        print(f"{image_set:5s}: {len(ids):5d} 张 -> {out_list.relative_to(ROOT)}")
    print(f"\n转换完成，共 {total_boxes} 个 smoking 标注框。")


if __name__ == "__main__":
    main()
