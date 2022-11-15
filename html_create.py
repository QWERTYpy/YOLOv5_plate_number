import shutil


def head_file(path, file_name, date):
    html_file = open(f"{path}/{file_name}.html", 'w')
    html_text = f"<html><head><h1>Таблица за {date}</h1></head><table border=1>" \
                f"<tr><td>Распознанный номер</td><td>Определенный номер</td><td>Фото машины</td></tr>"
    html_file.write(html_text)
    return  html_file

def str_file_error(html_file, text_error, file_name_big):
    html_text = f"<tr><td>{text_error}</td><td>...</td><td><img src='..\{file_name_big}' width = 200></td></tr>"
    html_file.write(html_text)

def str_file(html_file, plate_num_detect, path_img, path_result, file_name_small, file_name_big):
    shutil.copyfile(f"{path_img}/{file_name_small}", f"{path_result}/{file_name_small}")
    html_text = f"<tr><td>{plate_num_detect}</td>" \
                f"<td><img src='{file_name_small}' width = 200></td>" \
                f"<td><img src='{file_name_big}' width = 200></td></tr>"
    html_file.write(html_text)

def bd_str_file(html_file, list_str):
    place, date_photo, time_photo, type_car, number_plate, number_plate_img, car_img = list_str
    # shutil.copyfile(f"{path_img}/{file_name_small}", f"{path_result}/{file_name_small}")
    html_text = f"<tr><td>{place}</td>" \
                f"<td>{date_photo}</td>" \
                f"<td>{time_photo}</td>" \
                f"<td>{type_car}</td>" \
                f"<td>{number_plate}</td>" \
                f"<td><img src='{number_plate_img}' width = 200></td>" \
                f"<td><img src='{car_img}' width = 200></td></tr>"
    html_file.write(html_text)

def end_file(html_file):
    html_text = "</table></html>"
    html_file.write(html_text)
    html_file.close()
