import json
import glob
from detection_YOLO import detect_objects

def calibration():

    directory = glob.glob('img/*.jpg')

    result_list = []

    for pic in directory:

        box_list = detect_objects(pic)

        result_list.append({"filename": pic, "boxes": box_list})

    with open('boxes/boxes.json', 'w', encoding="utf-8") as f:
        json.dump(result_list, f, ensure_ascii=False, indent=1)