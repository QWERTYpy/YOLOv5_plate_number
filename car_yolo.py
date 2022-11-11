from yolov5 import YOLOv5 # Подключаем пакет для работы с сеткой https://pypi.org/project/yolov5/
import numpy
import cv2

class CarYOLO:
    def __init__(self):
        # Указываем путь к обученной модели
        model_path = "model/yolov5m_car_best.pt"
        device = "cpu"  # "cuda:0"  or "cpu"
        self.class_name = ["Фура", "Бус", "Легковая", "Номер", "Спецтехника", "Грузовик"]
        # Инициализируем модель
        self.yolov5 = YOLOv5(model_path, device)

    def result_model(self, images):
        """

        :param images: Путь к анализируемому изображению
        :return: список кооринат, вероятностей, классов
        """
        # Получаем рузультат детекции
        results = self.yolov5.predict(images, size=640)
        # results.show()
        # разделяем результаты
        predictions = results.pred[0]

        boxes = numpy.array(predictions[:, :4])  # x1, y1, x2, y2 Координаты
        boxes = [[int(list_el) for list_el in list_box] for list_box in boxes]

        scores = numpy.array(predictions[:, 4])  # Вероятности
        scores = [int(list_el * 100) for list_el in scores]

        categories = numpy.array(predictions[:, 5])  # Классы
        categories = [int(list_el) for list_el in categories]
        return boxes, scores, categories

    def separate_class(self, boxes, scores, categories):
        """
        Фунцкия раздлеят классы машин и номеров, для последующей установки соответсвий между ними
        :param boxes:
        :param scores:
        :param categories:
        :return:
        """
        boxes_plate = []
        scores_plate = []
        if 3 in categories:
            for _ in range(categories.count(3)):
                position = categories.index(3)
                boxes_plate.append(boxes.pop(position))
                scores_plate.append(scores.pop(position))
                categories.pop(position)
        return boxes_plate, scores_plate

    def conformity_class(self, boxes, boxes_plate):
        """
        Функция для сопоставления номеров машинам
        :param boxes:
        :param boxes_plate:
        :return: Список из двух списков. Первый - индекс номеров, Второй - индекс машины
        """
        conformity_list = [[],
                           []]  # Первый индекс номера, Второй индекс машины. Бывает случай, когда один номер принадлежит
        # двум классам одной машины
        for _ in range(len(boxes_plate)):
            for __ in range(len(boxes)):
                if boxes_plate[_][0] > boxes[__][0] and boxes_plate[_][1] > boxes[__][1] and \
                        boxes_plate[_][2] < boxes[__][2] and boxes_plate[_][3] < boxes[__][3]:
                    conformity_list[0].append(_)
                    conformity_list[1].append(__)
        return conformity_list

    def result_detection(self, images_path, folder_path, boxes, scores, categories, boxes_plate, scores_plate, conformity_list):
        img = cv2.imread(images_path)
        detect_list = []
        for ind in range(len(boxes)):
            # print(f"Обнаружено транспортное средство: {self.class_name[categories[ind]]}")
            x1, y1, x2, y2 = boxes[ind]
            img1 = img[y1:y2, x1:x2]
            # cv2.imshow("1", img1)
            *_, img_name = images_path.split('/')
            img_name = img_name[:8]
            *_, fld_name = folder_path.split('/')
            cv2.imwrite(f"{folder_path}/{img_name}_car_{ind}.jpg", img1)
            """
            Для вычисления среднего цвета по изрбражению
            yh =img1.shape[0]
            xh = img1.shape[1]
            img_tmp = img1[20:yh-20,20:xh-20]
            cv2.imshow("2", img_tmp)
            colors = numpy.unique(img1.reshape(-1, img1.shape[2]), axis=0)
            color = numpy.flip(colors.mean(axis=0, dtype=numpy.float64).astype(int)).tolist()
            print(color)
            """
            if ind in conformity_list[1]:
                ind_plate = conformity_list[1].index(ind)
                x1, y1, x2, y2 = boxes_plate[conformity_list[0][ind_plate]]
                # print(f"Обнаружен номер")
                img2 = img[y1:y2, x1:x2]
                # cv2.imshow("2", img2)
                cv2.imwrite(f"{folder_path}/{img_name}_plate_{ind_plate}.jpg", img2)
                detect_list.append([fld_name, img_name, self.class_name[categories[ind]],"NULL",
                                  f"{folder_path}/{img_name}_plate_{ind_plate}.jpg",
                                   f"{folder_path}/{img_name}_car_{ind}.jpg" ])
            else:
                detect_list.append([fld_name, img_name, self.class_name[categories[ind]], "NULL",
                                    "NULL",
                                    f"{folder_path}/{img_name}_car_{ind}.jpg"])
            # cv2.waitKey(0)
        return detect_list

