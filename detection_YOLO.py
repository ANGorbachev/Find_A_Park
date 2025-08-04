# pip install ultralytics
from ultralytics import YOLO


def detect_objects(pic_file):
    model = YOLO('model/yolov8l.pt')
    results = model.predict(pic_file)
    result = results[0]
    boxes = result.boxes
    box_list = []
    for box in boxes:
        cls_name = result.names[box.cls[0].item()]
        bbox_coord = box.xyxy[0].tolist()
        conf_proba = box.conf[0].item()

        x1, y1, x2, y2 = bbox_coord
        start_point = tuple(map(int, (x1, y1)))
        end_point = tuple(map(int, (x2, y2)))
        box_list.append({"cls_item": int(box.cls[0].item()),
                         "cls_name": cls_name,
                         "proba": round(conf_proba, 4),
                         "start_point": start_point,
                         "end_point": end_point,
                         })
    return box_list


if __name__ == "__main__":
    print("It is a module py-file")