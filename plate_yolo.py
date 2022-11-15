from yolov5 import YOLOv5 # Подключаем пакет для работы с сеткой https://pypi.org/project/yolov5/
import numpy
import cv2
from operator import itemgetter


class PlateYOLO:
    def __init__(self):
        # Указываем путь к обученной модели
        model_path = "model/yolov5m_best.pt"
        device = "cpu"  # "cuda:0"  or "cpu"
        self.class_name = list("0123456789ABCEHKMOPTXY")
        # Инициализируем модель
        self.yolov5 = YOLOv5(model_path, device)

    def result_model(self, images):
        """

        :param images: Путь к анализируемому изображению
        :return: список кооринат, вероятностей, классов
        """
        # Получаем рузультат детекции
        results = self.yolov5.predict(images, size=160)
        # results.show()
        # разделяем результаты
        predictions = results.pred[0]

        boxes = numpy.array(predictions[:, :4])  # x1, y1, x2, y2 Координаты
        boxes = [[int(list_el) for list_el in list_box] for list_box in boxes]

        scores = numpy.array(predictions[:, 4])  # Вероятности
        scores = [int(list_el * 100) for list_el in scores]

        categories = numpy.array(predictions[:, 5])  # Классы
        categories = [self.class_name[int(list_el)] for list_el in categories]
        return boxes, scores, categories

    def result_detection(self, boxes, scores, categories):
        plate_num = ""
        # Создаем список [x координата, вероятность, принадлежность классу
        symbol_result = list(zip(boxes, scores, categories))
        if len(symbol_result) < 5:
            return plate_num
        # print(symbol_result)
        # Сортируем по Х по возрастанию
        symbol_result = sorted(symbol_result, key=itemgetter(0))
        # print(symbol_result)
        symbol_result_tmp = []
        flag_dubl = False

        # Последовательно проверяем все найденные символы
        for _ in range(len(symbol_result) - 1):
            if flag_dubl:
                # Если были определены два символа по одним координатам
                flag_dubl = False
                continue
            if symbol_result[_ + 1][0][0] - symbol_result[_][0][0] > 5:  # Если растояние между символами >5: добавляем
                symbol_result_tmp.append(symbol_result[_])
                if _ == len(symbol_result) - 2:  # Если символ предпоследний
                    symbol_result_tmp.append(symbol_result[_ + 1])
            else:
                if symbol_result[_][1] < symbol_result[_ + 1][1]:
                    # symbol_result_tmp.append(symbol_result[_])
                    if _ == len(symbol_result) - 2:  # Если символ предпоследний
                        symbol_result_tmp.append(symbol_result[_ + 1])
                    continue
                else:
                    symbol_result_tmp.append(symbol_result[_])
                    flag_dubl = True

        # Сохраняем отсортированные символы
        symbol_result = symbol_result_tmp
        # print(symbol_result)

        # Составляем определенный номер из символов
        ver = ""
        for _ in symbol_result:
            plate_num += _[2]
            ver += str(_[1])+"-"
        print(ver)
        return plate_num


