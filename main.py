import Postgresql.postgresql_db as postgresql_db
import Interface.terminal_interface as gui
from Interface.terminal_interface import message
import datetime

#IN YEAR
def quarter_mark(year):
    gui.clear_terminal()
    subj_name, quarter_num = gui.quarter_mark()

    if not (len(quarter_num) == 1 and quarter_num[0] > '0' and quarter_num[0] < '5'):
        message('Нет такой четверти')
        return
    
    subj_id = postgresql_db.exist_subject_name(subj_name)
    if subj_id < 1:
        message('Не удалось найти предмет')
        return
    
    mark_list = year.quarter_marks(subj_id, int(quarter_num) - 1)
    if mark_list[0] == -1:
        message('Не удалось получить оценки')
        return
    
    gui.print_quarter_mark(mark_list, subj_name)
    
    
def add_mark(year):
    gui.clear_terminal()
    mark, subj_name, date = gui.add_mark()

    if not((len(mark) == 1 and mark > '0' and mark <= '9') or (len(mark) == 2 and mark[0] == '1' and mark[1] == '0')):
        message('Неправильно введеа оценка')
        return

    subj_id = postgresql_db.exist_subject_name(subj_name)
    if subj_id < 1:
        message('Не удалось найти предмет')
        return 
    
    rt = year.add_mark(mark, date, subj_id)
    if rt == 2:
        message('В эту дату нету четверти')
    elif rt == 1:
        message('Не удалось добавить оценку')
    else:
        message('Оценка была добавлена')

def year_menu(year_name):
    year = postgresql_db.Education_year(postgresql_db.exist_year_name(year_name))
    while 1:
        ch = gui.year_menu()
        match ch:
            case '1':
                add_mark(year)
            case '2':
                quarter_mark(year)
            case '3':
                break
            case _:
                message('Нет такого выбора')

#YEAR
def login_year():
    gui.clear_terminal()
    year_list = postgresql_db.get_list_year()
    gui.print_list(_list=year_list)
    year_name = gui.get_inp('Введите название года: ')

    if year_name in year_list:
        year_menu(year_name)
    else:
        message('Не удалось найти год')

def create_year():
    gui.clear_terminal()
    year = gui.get_inp('Введите название года: ')
    if postgresql_db.exist_year_name(year_name=year) > 0:
        message('Не удалось найти год')
        return
    
    try:
        quarter_list =[[datetime.datetime.strptime(e, '%Y-%m-%d') for e in i] for i in gui.creat_year_qulist()]
    except Exception as e:
        message('Некоректный ввод даты')
        return 
    
    for x in range(4):
        for y in range(x + 1,4):
            if quarter_list[y][0] > quarter_list[y][1]:
                message('Некоректный ввод даты')
            if (quarter_list[x][0] >= quarter_list[y][0] and quarter_list[x][0] <= quarter_list[y][0]) or (quarter_list[x][1] >= quarter_list[y][0] and quarter_list[x][1] <= quarter_list[y][1]):
                message('Некоректный ввод даты')
    
    if postgresql_db.create_year(year_name=year,quarterlist=quarter_list) != 0:
        message('Не удалось создать')
    else:
        message('Год был создан')

def delete_year():
    gui.clear_terminal()
    year_ls = postgresql_db.get_list_year()
    gui.print_list(year_ls)
    year = gui.get_inp('Введите название года: ')

    if not year in year_ls:
        message('Не удалось найти год')
        return

    if postgresql_db.delete_year(year_name=year) != 0:
        message('Не удалось удалить год')
    else:
        message('Год был удален')


#SUBJECT
def create_subject():
    gui.clear_terminal()
    sub_name = gui.get_inp('Введите название предмета: ')
    
    if postgresql_db.exist_subject_name(subject_name=sub_name) > 0:
        message('Предмет с таким именем уже существует')
    elif postgresql_db.create_subject(subj_name=sub_name) == 0:
        message('Предмет был создан')
    else:
        message('Не удалось создать предмет')

def delete_subject():
    gui.clear_terminal()
    sub_ls = postgresql_db.get_list_subject()
    gui.print_list(sub_ls)
    sub_name = gui.get_inp('Введите название предмета: ')
    
    if not sub_name in sub_ls:
        message('Не удалось найти предмет')
        return

    if postgresql_db.delete_subject(subj_name=sub_name) == 0:
        message('Предмет был удален')
    else:
        message('Не удалось удалить предмет')


#MAIN
def main():
    postgresql_db.connect()
    while 1:
        match gui.start_menu():
            case '1':
                login_year()
            case '2':
                create_year()
            case '3':
                delete_year()
            case '4':
                create_subject()
            case '5':
                delete_subject()
            case '6':
                break
            case _:
                message('Такого выбора не существует')

if __name__ == '__main__':
    main()