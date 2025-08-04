# from transformers import DetrForObjectDetection
# model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import cv2
from PIL import Image
import requests

# url = "http://images.cocodataset.org/val2017/000000039769.jpg"

# image = Image.open(requests.get(url, stream=True).raw)
image = cv2.imread("../img/snap_4001.jpg")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# you can specify the revision tag if you don't want the timm dependency
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm") # "facebook/detr-resnet-101"
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm") # "facebook/detr-resnet-101"

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)

# convert outputs (bounding boxes and class logits) to COCO API
# let's only keep detections with score > 0.9

# target_sizes = torch.tensor([image.size[::-1]])
target_sizes = torch.tensor([image.shape[:-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
            f"Detected {model.config.id2label[label.item()]} with confidence "
            f"{round(score.item(), 3)} at location {box}"
    )

for _, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    bbox_coord = [int(i) for i in box.tolist()]
    cls_name = model.config.id2label[label.item()]

    # conf_proba = box.conf[0].item()
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