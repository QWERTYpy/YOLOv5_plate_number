import os
import car_yolo as cy
import postgresql as pg


# Указываем путь к папке с анализируемыми изображениями
folder_path = "img_cl"
# Указываем путь к папке с результатом детекции
folder_result_path = "img_res"
# Создаем экземпляр класса для детекции
car_det = cy.CarYOLO()
# Создаем подключение к БД
bd = pg.PostgessBase()
# Подгружаем изображение

for folder_time in os.listdir(folder_path):
    full_path = f"{folder_path}/{folder_time}/pic_001/"
    for filename in os.listdir(full_path):
        # Подготавливаем папку для результата
        if not os.path.exists(f"{folder_result_path}/{folder_time}"):
            os.mkdir(f"{folder_result_path}/{folder_time}")
            print(f"Создана папка: {folder_time}")
        # составляем путь до изображения
        img_str = full_path + f"{filename}"
        #  Получаем результат от модели
        boxes, scores, categories = car_det.result_model(img_str)
        # Если ничего не найдено, то пропускам
        if not boxes:
            print("Транспортные средства не обнаружены.")
            continue
        # print(boxes, scores, categories)
        # Разделяем результаты
        boxes_plate, scores_plate = car_det.separate_class(boxes, scores, categories)
        # print(boxes, scores, categories)
        # print(boxes_plate,scores_plate)
        # Сопоставляем номера с машинами
        conformity_list = car_det.conformity_class(boxes, boxes_plate)
        # print(conformity_list)
        # Получаем результат обработки
        detect_list = car_det.result_detection(img_str, f"{folder_result_path}/{folder_time}",
                                               boxes, scores, categories, boxes_plate, scores_plate, conformity_list)

        for _ in detect_list:
            bd.insert_data(_)

