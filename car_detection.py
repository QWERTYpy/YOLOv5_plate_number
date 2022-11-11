import os
import car_yolo as cy
# Указываем путь к папке с анализируемыми изображениями
images_path = "img_cl"

# Создаем экземпляр класса для детекции
car_det = cy.CarYOLO()
# Подгружаем изображение
for filename in os.listdir(images_path):
    # составляем путь до изображения
    img_str = f"{images_path}/{filename}"
    #  Получаем результат от модели
    boxes, scores, categories = car_det.result_model(img_str)
    # Если ничего не найдено, то пропускам
    if not boxes:
        print("Транспортные средства не обнаружены.")
        continue
    print(boxes, scores, categories)
    # Разделяем результаты
    boxes_plate, scores_plate = car_det.separate_class(boxes, scores, categories)
    print(boxes, scores, categories)
    print(boxes_plate,scores_plate)
    # Сопоставляем номера с машинами
    conformity_list = car_det.conformity_class(boxes, boxes_plate)
    print(conformity_list)
    # Получаем результат обработки
    car_det.result_detection(img_str, boxes, scores, categories, boxes_plate, scores_plate, conformity_list)
