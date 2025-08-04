import cv2
import json
import glob

directory = glob.glob('img/*.jpg')

with open('boxes/boxes.json', 'r', encoding="utf-8") as file:
    dump = json.load(file)

for pic in dump:
    image = cv2.imread(pic["filename"])
    boxes = pic["boxes"]

    for box in boxes:
        cls_name = box['cls_name']
        start_point = box['start_point']
        end_point = box['end_point']
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
        if cv2.waitKey(1) & 0xFF == 27:  # ord('q')
            break
