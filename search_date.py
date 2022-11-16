import postgresql as pg
import re
import datetime
import html_create as hc
import html_create_pages as hcp

# Создаем подключение к БД
bd = pg.PostgessBase()
# Получаем минимальную и максимальную дату в архиве
list_mm_date = bd.mm_date()

print(f"БД с - {list_mm_date[0][0]} по {list_mm_date[0][1]}.")
input_date = ""

flag_date = True
while flag_date:
    while not re.match(r'....-..-..', input_date):
        input_date = input("\rВведите дату для поиска:")
    input_date = datetime.datetime.strptime(input_date, '20%y-%m-%d').date()
    if input_date >= list_mm_date[0][0] and input_date <= list_mm_date[0][1]:
        flag_date = False
    else:
        print("Дата вне интервала.")
        input_date = ""
input_low = input("Введите с какого часа искать:")
input_hight = input("Введите по какой час искать:")
car_type = ["Фура", "Бус", "Легковая", "Номер", "Спецтехника", "Грузовик", "Все"]
print(f"Выберите тип траспортного средства: ", end="")
for _ in range(len(car_type)):
    print(f"{car_type[_]} - {_} ", end="")
input_type = input("Введите номер:")

list_result = bd.select_date(input_date, f"{input_low}:00:00", f"{input_hight}:00:00", car_type[int(input_type)])
print(f"Найдено {len(list_result)} записей")
# Создаем файл с отчетом
html_file = hc.head_file("./", f"{input_date}_{input_low}_{input_hight}", str(input_date))
for res in list_result:
    hc.bd_str_file(html_file, res)
hc.end_file(html_file)


# row_count = 12
# str_count = int(len(list_result)/row_count)+1
# html_file = hcp.head_file("./", f"{input_date}_{input_low}_{input_hight}", str_count)
# hcp.str_file(html_file, list_result, str_count,row_count)
# hcp.navigation(html_file, str_count)
# hcp.end_file(html_file)

