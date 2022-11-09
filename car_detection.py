from yolov5 import YOLOv5 # Подключаем пакет для работы с сеткой https://pypi.org/project/yolov5/
import numpy
import cv2

def result_model(images):
    """

    :param images: Путь к анализируемому изображению
    :return: список кооринат, вероятностей, классов
    """
    # Получаем рузультат детекции
    results = yolov5.predict(images, size=640)

    # разделяем результаты
    predictions = results.pred[0]

    boxes = numpy.array(predictions[:, :4])  # x1, y1, x2, y2 Координаты
    boxes = [[int(list_el) for list_el in list_box] for list_box in boxes]

    scores = numpy.array(predictions[:, 4])  # Вероятности
    scores = [int(list_el*100) for  list_el in scores]

    categories = numpy.array(predictions[:, 5])  # Классы
    categories = [int(list_el) for list_el in categories]

    return boxes, scores, categories


def separate_class(boxes, scores, categories):
    """
    Фунцкия раздлеят классы машин и номеров, для последующей установки соответсвий между ними
    :param boxes:
    :param scores:
    :param categories:
    :return:
    """
    if 3 in categories:
        boxes_plate = []
        scores_plate = []
        for _ in range(categories.count(3)):
            position = categories.index(3)
            boxes_plate.append(boxes.pop(position))
            scores_plate.append(scores.pop(position))
            categories.pop(position)
    return boxes_plate, scores_plate


def conformity_class(boxes, boxes_plate):
    conformity_list = []
    for _ in range(len(boxes_plate)):
        for __ in range(len(boxes)):
            if boxes_plate[_][0]> boxes[__][0] and boxes_plate[_][1]> boxes[__][1] and \
               boxes_plate[_][2] < boxes[__][2] and boxes_plate[_][3] < boxes[__][3]:
                conformity_list.append(__)
    return conformity_list

def result_detection(images_path, boxes, scores, categories, boxes_plate, scores_plate, conformity_list):
    img = cv2.imread(images_path)
    for ind in range(len(boxes)):
        print(f"Обнаружено транспортное средство: {class_name[categories[ind]]}")
        x1,y1,x2,y2 = boxes[ind]
        img1 = img[y1:y2, x1:x2]
        cv2.imshow("1", img1)
        if ind in conformity_list:
            ind_plate = conformity_list.index(ind)
            x1, y1, x2, y2 = boxes_plate[ind_plate]
            print(f"Обнаружен номер")
            img2 = img[y1:y2, x1:x2]
            cv2.imshow("2", img2)
        cv2.waitKey(0)


# Указываем путь к обученной модели
model_path = "model/yolov5m_car.pt"
device = "cpu"  # "cuda:0"  or "cpu"
class_name = ["Фура", "Бус", "Легковая", "Номер", "Спецтехника", "Грузовик"]

# Инициализируем модель
yolov5 = YOLOv5(model_path, device)

# Подгружаем изображение
images = "img_cl/15.09.20[M][0@0][0][0].jpg"

boxes, scores, categories = result_model(images)
print(boxes, scores, categories)
boxes_plate,scores_plate = separate_class(boxes, scores, categories)
print(boxes, scores, categories)
print(boxes_plate,scores_plate)
conformity_list = conformity_class(boxes, boxes_plate)
print(conformity_list)
result_detection(images, boxes, scores, categories, boxes_plate, scores_plate, conformity_list)
# img = cv2.imread(images)
# # img = cv2.resize(img, (640,640))
# x = int(boxes[0])
# xh = int(boxes[2])
# y = int(boxes[1])
# yh = int(boxes[3])
# print(x,xh,y,yh)
# img1 = img[y:yh, x:xh]
# cv2.imshow("1", img1)
# cv2.waitKey(0)
#
# results.show()