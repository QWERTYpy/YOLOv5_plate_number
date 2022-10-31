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
#  Преобразуем веса в TensorFlow
# python export.py --weights best.pt --include saved_model
# Используя скрипт из папки с моделью
