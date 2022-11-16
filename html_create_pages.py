import shutil


def head_file(path, file_name, all_page):
    html_file = open(f"{path}/{file_name}.html", 'w')
    html_text = """
<html lang="ru"><head>

<title>CodGen</title>

<style>
body {
    margin: 0;
    padding: 0;
}

main,
nav {
    width: 100%;
    position: absolute;
    top: 0;
}

main > section {
    width: 100%;
    height: 100vh;
    display: none;
    position: relative;
}

main > section > span {
    #position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #000000;
    font: 800 32px Sans-serif;
    
}

ul {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    list-style-type: none;
}

ul > li {
    margin: 16px;
}

ul > li > label {
    font: 400 18px Sans-serif;
    color: #000000;
    cursor: pointer;
}

ul > li > label:hover {
    text-decoration: underline;
}
"""
    for _ in range(all_page):
        html_text += f'#r-{_}:checked ~ main > #p-{_}'
        if _ < all_page-1:
            html_text +=',\n'
    html_text+="""{
        display: block;
        }
</style>




<script>
    if (document.location.search.match(/type=embed/gi)) {
        window.parent.postMessage("resize", "*");
    }
</script>


</head>
"""
    html_file.write(html_text)
    return  html_file


def list_parser(list_result, count_row, count_page):
    html_text = ""
    left = -count_row
    right = 0
    for page in range(count_page):
        left += count_row
        right += count_row
        yield list_result[left:right]
        # place, date_photo, time_photo, type_car, number_plate, number_plate_img, car_img = list_row
        # html_text += f"<tr><td>{place}</td>" \
        #             f"<td>{date_photo}</td>" \
        #             f"<td>{time_photo}</td>" \
        #             f"<td>{type_car}</td>" \
        #             f"<td>{number_plate}</td>" \
        #             f"<td><img src='{number_plate_img}' width = 200></td>" \
        #             f"<td><img src='{car_img}' width = 200></td></tr>"
        # count_row -= 1
        # if count_row == 0:
        #     yield html_text



def str_file(html_file, list_result, all_page, all_row):
    html_text = '<body translate="no">\n'
    count_row = all_row
    for _ in range(all_page):
        if _ == 0:
            html_text += f'<input type="radio" name="page" id="r-{_}" hidden="" checked="">\n'
        else:
            html_text += f'<input type="radio" name="page" id="r-{_}" hidden="">\n'
    html_text += '<main>\n'
    for index, row_block in enumerate(list_parser(list_result, count_row, all_page)):
        html_text += f'<section id="p-{index}"><span><center>Страница - {index}</center>'
        html_text += f"<table border=1><tr><td>Местоположение</td><td>Дата</td><td>Время</td><td>Тип</td><td>Номер</td><td>Фото номера</td><td>Фото машины</td></tr>"
        for row in row_block:
            place, date_photo, time_photo, type_car, number_plate, number_plate_img, car_img = row
            html_text += f"<tr><td>{place}</td>" \
                        f"<td>{date_photo}</td>" \
                        f"<td>{time_photo}</td>" \
                        f"<td>{type_car}</td>" \
                        f"<td>{number_plate}</td>" \
                        f"<td><img src='{number_plate_img}' width = 200></td>" \
                        f"<td><img src='{car_img}' width = 200></td></tr>"

            # html_text += list_parser(list_result, count_row)
        html_text +=f'</table></span></section>\n'
    html_text += '</main>\n<nav><ul>\n'
    html_file.write(html_text)

def navigation(html_file, all_page):
    html_text=""
    for _ in range(all_page):

         html_text += f'<li><label for="r-{_}">{_}</label></li>\n'
    html_file.write(html_text)



def end_file(html_file):
    html_text = " </ul></nav></body></html>"
    html_file.write(html_text)
    html_file.close()


if __name__ == '__main__':
    html_file = head_file("./", f"1121","222", 5)

    str_file(html_file,"text",5)
    navigation(html_file, 5)
    end_file(html_file)