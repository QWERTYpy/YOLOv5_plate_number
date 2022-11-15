import plate_yolo as py
import postgresql as pg
import os


# Указываем путь к папке с анализируемыми изображениями
path_plate = "img_res/2022-11-10"

# Создаем экземпляр класса для детекции
plate_det = py.PlateYOLO()
# Создаем подключение к БД
bd = pg.PostgessBase()

i=0
flag_plate = True
while flag_plate:
    if bd.select_row() == None:
        break
    *_, number_plate_img, car_img = bd.select_row()

    # if i == 500: break
    #  Получаем результат от модели
    boxes, scores, categories = plate_det.result_model(number_plate_img)
    # print(boxes, scores, categories)
    plt = plate_det.result_detection(boxes, scores, categories)
    if plt:
        bd.update_row(plt, car_img)
        print(plt)
        i+=1
        print(i)
    else:
        bd.update_row("False", car_img)
