import postgresql_db
import Interface.terminal_interface as gui
from Interface.terminal_interface import message

#YEAR
def login_year():
    year_list = postgresql_db.get_list_year()
    gui.get_year_list(year_list=year_list)
    year_name = gui.login_year()

    if year_name in year_list:
        #create obj
        pass
    else:
        message('Нет такого года')

def create_year():
    year = gui.create_year_getname()
    if postgresql_db.exist_year_name(year_name=year) > 0:
        message('Год с таким именем уже существует')
        return
    
    quarter_list = gui.creat_year_qulist()
    
    if postgresql_db.create_year(year_name=year,quarterlist=quarter_list) != 0:
        message('Не удалось создать')
    else:
        message('Год был создан')

def delete_year():
    gui.get_year_list(postgresql_db.get_list_year())
    year = gui.delete_year()

    if postgresql_db.exist_year_name(year_name=year) < 1:
        message('Такого года не существует')
        return

    if postgresql_db.delete_year(year_name=year) != 0:
        message('Не удалось удалить год')
    else:
        message('Год был удален')


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
                pass
            case '5':
                pass
            case '6':
                break
            case _:
                message('Такого выбора не существует')

if __name__ == '__main__':
    main()