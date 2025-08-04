import cv2

path_photo = "../img/snap_1001.jpg"

image_cv = cv2.imread(path_photo)
print(type(image_cv))

image_file = open(path_photo, 'rb')
print(type(image_file))