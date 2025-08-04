# pip install ultralytics

import cv2
from ultralytics import YOLO

model = YOLO('yolov8l.pt')
results = model.predict("img/snap_101.jpg")
result = results[0]

image = cv2.imread("img/snap_101.jpg")

boxes = result.boxes

for box in boxes:
    cls_name = result.names[box.cls[0].item()]
    bbox_coord = box.xyxy[0].tolist()
    conf_proba = box.conf[0].item()
    # print("Object type:", cls_name)
    # print("Coordinates:", bbox_coord)
    # print("Probability:", conf_proba)

    x1, y1, x2, y2 = bbox_coord
    start_point = tuple(map(int, (x1, y1)))
    end_point = tuple(map(int, (x2, y2)))
    color = (0, 255, 0)
    thickness = 2

    image = cv2.rectangle(image, start_point, end_point, color, thickness)

    org = start_point
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.4
    color = (0, 255, 0)
    thickness = 1
    lineType = cv2.LINE_AA
    image = cv2.putText(image, cls_name, org, font, fontScale, color, thickness, cv2.LINE_AA)


# Нажмите 'Esc', чтобы выйти.
while True:
    cv2.imshow('parking', image)
    if cv2.waitKey(1) & 0xFF == 27: # ord('q')
        break

