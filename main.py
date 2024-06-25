import postgresql_db
import Interface.terminal_interface as gui
from Interface.terminal_interface import message

#YEAR
def login_year():
    gui.clear_terminal()
    year_list = postgresql_db.get_list_year()
    gui.print_list(_list=year_list)
    year_name = gui.get_inp('Введите название года: ')

    if year_name in year_list:
        #create obj
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