import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Глобальные переменные для хранения координат
rectangles = []  # Список для хранения координат выделенных областей
is_drawing = False  # Флаг, указывающий, рисуем ли мы
start_point = None  # Начальная точка выделения

# Функция для обработки кликов мыши
def onclick(event):
    try:
        global start_point, is_drawing, rectangles
        if event.button == 1:  # Левый клик
            if not is_drawing:
                start_point = (event.xdata, event.ydata)
                is_drawing = True
            else:
                end_point = (event.xdata, event.ydata)
                rectangles.append((start_point, end_point))  # Сохраняем координаты
                plt.gca().add_patch(plt.Rectangle(start_point,
                                                   end_point[0] - start_point[0],
                                                   end_point[1] - start_point[1],
                                                   edgecolor='green', facecolor='none', linewidth=2))
                is_drawing = False
                plt.draw()
    except:
        pass
# Загрузите изображение
image_path = "img/snap_101.jpg"
img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Преобразуем BGR в RGB

# Отображаем изображение
plt.imshow(img)
plt.axis('off')
plt.title('Нажмите и перетащите для выделения объектов.')
plt.connect('button_press_event', onclick)

plt.show()

# Создаем DataFrame для координат
xmin = []
ymin = []
xmax = []
ymax = []

for rect in rectangles:
    xmin.append(rect[0][0])
    ymin.append(rect[0][1])
    xmax.append(rect[1][0])
    ymax.append(rect[1][1])

df_coordinates = pd.DataFrame({
    'xmin': xmin,
    'ymin': ymin,
    'xmax': xmax,
    'ymax': ymax
})

# Выводим DataFrame
print(df_coordinates)
df_coordinates.to_csv('img/snap_101.csv', sep=';', index=False)