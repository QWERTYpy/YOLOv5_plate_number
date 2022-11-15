import os
import car_yolo as cy
import postgresql as pg
import datetime
import re

# Указываем путь к папке с анализируемыми изображениями
# folder_path = "img_cl"
folder_path = "\\\\10.64.130.249\\Distr2\\CAM\\7K0215CPAJC2774"
# Указываем путь к папке с результатом детекции
folder_result_path = "img_res"
# Создаем экземпляр класса для детекции
car_det = cy.CarYOLO()
# Создаем подключение к БД
bd = pg.PostgessBase()
# Подгружаем изображение
# Получаем текущую дату
now_date = datetime.datetime.today().strftime("%Y-%m-%d")
# print(now_date) # 2022-11-14
# for ddir in os.listdir("\\\\10.64.130.249\\Distr2\\CAM\\7K0215CPAJC2774"):
#     if re.match(r'....-..-..', ddir):
#         print(ddir)

for folder_time in os.listdir(folder_path):
    if re.match(r'....-..-..', folder_time):
        if folder_time == now_date:
            continue

        if bd.date_exists(folder_time):
            # print(f"Папка {folder_time} - уже обрабатывалась.")
            # continue
            cur_time = bd.time_exists(folder_time)
        else:
            cur_time = datetime.datetime.strptime("00:00:00", '%H:%M:%S').time()
        full_path = f"{folder_path}/{folder_time}/pic_001/"
        print("\n", full_path)
        all_files = len(os.listdir(full_path))
        print(f"Всего файлов: {all_files}")
        count = 0

        for filename in os.listdir(full_path):
            count += 1
            print(f"\rОбработано процентов: {int(count*100/all_files)}", end="")
            img_time = filename[:8]
            img_time = f"{img_time.replace('.', ':')}"
            img_time = datetime.datetime.strptime(img_time, '%H:%M:%S').time()
            # print(img_time)
            if img_time < cur_time:
                continue
            # print("rrr")
            # Подготавливаем папку для результата
            if not os.path.exists(f"{folder_result_path}/{folder_time}"):
                os.mkdir(f"{folder_result_path}/{folder_time}")
                # print(f"Создана папка: {folder_time}")
            # составляем путь до изображения
            img_str = full_path + f"{filename}"
            #  Получаем результат от модели
            boxes, scores, categories = car_det.result_model(img_str)
            # Если ничего не найдено, то пропускаем
            if not boxes:
                # print("Транспортные средства не обнаружены.")
                continue
            # Разделяем результаты
            boxes_plate, scores_plate = car_det.separate_class(boxes, scores, categories)
            # Сопоставляем номера с машинами
            conformity_list = car_det.conformity_class(boxes, boxes_plate)
            # Получаем результат обработки
            detect_list = car_det.result_detection(img_str, f"{folder_result_path}/{folder_time}",
                                                   boxes, scores, categories, boxes_plate, scores_plate,
                                                   conformity_list)
            # Добавляем полученные данные в БД
            for _ in detect_list:
                bd.insert_data(_)
        print("\n")
            # print(img_str)




