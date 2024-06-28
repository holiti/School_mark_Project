import postgresql_db
import Interface.terminal_interface as gui
from Interface.terminal_interface import message
import datetime

#IN YEAR
def add_mark(obj):
    gui.clear_terminal()
    mark, subj_name, date = gui.add_mark()

    if not((len(mark) == 1 and mark > '0' and mark <= '9') or (len(mark) == 2 and mark[0] == '1' and mark[1] == '0')):
        message('Неправильно введеа отметка')
        return

    subj_id = postgresql_db.exist_subject_name(subj_name)
    if subj_id < 1:
        message('Нет такого предмета')
        return 
    
    rt = obj.add_mark(mark, date, subj_id)
    if rt == 2:
        message('В эту дату нету четверти')
    elif rt == 1:
        message('Не удалось добавить отметку')
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
                pass
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
        pass
    else:
        message('Нет такого года')

def create_year():
    gui.clear_terminal()
    year = gui.get_inp('Введите название года: ')
    if postgresql_db.exist_year_name(year_name=year) > 0:
        message('Год с таким именем уже существует')
        return
    
    quarter_list = gui.creat_year_qulist()
    
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
        message('Такого года не существует')
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
        message('Нет такого предмета')
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