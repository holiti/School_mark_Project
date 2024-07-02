from os import system
from time import sleep

def message(error_message):
    print(error_message)
    sleep(2)

def clear_terminal():
    system('clear')

def print_list(_list):
    for i in _list:
        print(i)

def get_inp(message) -> str:
    res = input(message)
    return res

#MENU
def start_menu() -> str:
    clear_terminal()
    print("""1 - Войти в год
2 - Создать год
3 - Удалить год
4 - Создать предмет
5 - Удалить предмет
6 - Выйти из программы""")
    
    ch = input('Ваш выбор: ')
    return ch



#YEAR
def creat_year_qulist() -> list:
    qulist = []
    print("""Введите даты начала каждой четверти(из 4) в формате
начало_четверти(yyyy-mm-dd) конец_четвери(yyyy-mm-dd)""")
    for i in range(1,5):
        qulist.append(list(input(f'{i}: ').split()))
    return qulist

#IN YEAR
def year_menu() -> int:
    clear_terminal()
    print("""1 - Добавить отметку
2 - Получить отметки за четверть
3 - Выйти из года""")
    
    ch = input('Ваш выбор: ')
    return ch

def add_mark():
    mark = input('Введите оценку(10 бальная система): ')
    subj_name = input('Введеите название предммета: ')
    date = input('Введите дату получения оценки: ')
    return [mark, subj_name, date]

def quarter_mark() -> list:
    subj_name = input('Введите название предмета: ')
    quarter_num = input('Введите номер четверти(1, 2, 3 или 4): ')
    return [subj_name, quarter_num]

def print_quarter_mark(mark_list,subj_name):
    print(str('средний бал').rjust(len(subj_name) + 12),end='')
    for i in range(1,len(mark_list)):
        print(f' {mark_list[i][1]}',end = '')
    print()
    print(subj_name,end = '')
    print(str(mark_list[0]).rjust(12),end='')
    for i in range(1,len(mark_list)):
        print(' ' + str(mark_list[i][0]).rjust(10),end='')
    input('\nНажмите ENTER для выхода: ')
