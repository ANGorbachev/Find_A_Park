from ultralytics.utils.metrics import bbox_iou
from detection_YOLO import detect_objects
from get_picture import get_picture
import json
import cv2
from torch import Tensor

THRESHOLD = 0.2

def get_bboxes():
    try:
        with open('boxes/boxes.json', 'r', encoding="utf-8") as file:
            bbox_dump = json.load(file)
        return bbox_dump
    except FileNotFoundError:
        print("Файл калибровки не найден! Сначала запустите калибровку!")


def get_available_parkings(dump, threshold=THRESHOLD):
    get_picture()
    available_parkings = []
    for pic in dump:
        image = cv2.imread(pic["filename"])
        saved_boxed = pic["boxes"]
        current_boxes = [(*box["start_point"], *box["end_point"]) for box in detect_objects(pic["filename"])]
        is_parking_available = False

        for box in saved_boxed:
            cls_name = box['cls_name']
            start_point = box['start_point']
            end_point = box['end_point']

            box1 = Tensor([*start_point, *end_point])
            box2 = Tensor(current_boxes)

            iou = bbox_iou(box1, box2, xywh=False)
            # print(iou, iou.shape)
            iou_result = iou.max() if sum(iou.shape) > 0 else iou.sum()

            if iou_result < threshold:
                is_parking_available = True
                # color = (0, 0, 255) if iou_result < threshold else (0, 255, 0)
                color = (0, 0, 255)
                thickness = 2

                image = cv2.rectangle(image, start_point, end_point, color, thickness)

                org = start_point
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 0.4
                thickness = 1
                lineType = cv2.LINE_AA
                image = cv2.putText(image, cls_name, org, font, fontScale, color, thickness, cv2.LINE_AA)

        if is_parking_available:
            available_parkings.append(image)
    return available_parkings

if __name__ == "__main__":
    dump = get_bboxes()
    available_parkings = get_available_parkings(dump)
    for image in available_parkings:
        # Нажмите 'Esc', чтобы выйти.
        while True:
            cv2.imshow('parking', image)
            if cv2.waitKey(1) & 0xFF == 27:  # ord('q')
                break