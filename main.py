# Итак. Это третья версия проекта. Надеюсь доведу его до ума. Начало 28.10.2022
# Для начала была скачена модель YOLOv5
# $ git clone https://github.com/ultralytics/yolov5
# $ cd yolov5
# $ pip install -r requirements.txt
#Скачена предобученная модель s
# import torch
#
# # Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
# С помошью https://app.roboflow.com/ были размечены изображения
# Последняя версия находится в папке dataset
# В https://colab.research.google.com/ было проведено обучение
# !git clone https://github.com/ultralytics/yolov5
# !pip install -r ./yolov5/requirements.txt
# import torch
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# !python ./yolov5/train.py --img 160 --batch 32 --epochs 500 --data ./yolov5/data.yaml --weights ./yolov5/yolov5s.pt
# Обученная модель находится в папке model
# Это пока не получилось
# Преобразуем веса в TensorFlow
# python export.py --weights best.pt --include saved_model
# Используя скрипт из папки с моделью
# Работаем с обученной сеткой через torch


import torch
# Выполняем установку пакетов для выполения всех зависимостей
# import pillow
# import numpy
# import opencv-python
# import pandas
# import requests
# import IPython
# import torchvision
# import yaml
# from tqdm import tqdm
# import matplotlib.pyplot as plt
# import seaborn as sn
# import scipy
# import psutil

from PIL import Image
import numpy
from operator import itemgetter
import html_create as hc
import os

def get_plate_number(result_detection):
    symbol_result_all = result_detection.xyxy[0]  # im predictions (tensor)
    symbol_result_all = numpy.array(symbol_result_all)
    symbol_str = "0123456789ABCEHKMOPTXY"
    symbol_result = []

    for _ in symbol_result_all:
        symbol_result.append([_[0], _[4], _[5]])
    symbol_result = sorted(symbol_result, key=itemgetter(0))
    symbol_result_tmp = []
    flag_dubl = False
    for _ in range(len(symbol_result)-1):
        if flag_dubl:
            flag_dubl = False
            continue
        if symbol_result[_+1][0] - symbol_result[_][0] > 5:
            symbol_result_tmp.append(symbol_result[_])
            if _ == len(symbol_result)-2:
                symbol_result_tmp.append(symbol_result[_+1])
        else:
            if symbol_result[_][1] < symbol_result[_+1][1]:
                # symbol_result_tmp.append(symbol_result[_])
                continue
            else:
                symbol_result_tmp.append(symbol_result[_])
                flag_dubl = True
    # print(symbol_result)
    # print(symbol_result_tmp)

    symbol_result = symbol_result_tmp
    plate_num = ""
    for _ in symbol_result:
        plate_num += symbol_str[int(_[2])]
    return plate_num


# Загружаем модель
model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/yolov5s_best.pt', force_reload=True)  # yolov5n - yolov5x6 official model
#                                            'custom', 'path/to/best.pt')  # custom model

model.conf = 0.35 # Устанавливаем порог достоверности
path_result = "result"
path_img = "test_img"
html_file = hc.head_file(path_result, "test1", "31.10")

for filename in os.listdir(path_img):
    # Загружаем изображение
    img = Image.open(f"{path_img}/{filename}")
    # Inference
    results = model(img, size=160)
    # print(results.pandas().xyxy[0])
    plate_num_detect = get_plate_number(results)
    # print(plate_num_detect)

    # results.show()
    # input(">>>")
    hc.str_file(html_file,plate_num_detect, path_img, path_result, filename, "xxx")

hc.end_file(html_file)