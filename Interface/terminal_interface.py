from os import system
from time import sleep

def message(error_message):
    print(error_message)
    sleep(1)

def clear_terminal():
    system('clear')

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
def get_year_list(year_list):
    clear_terminal()
    for i in year_list:
        print(i)
    
def login_year() -> str:
    year_name = input('Введите название года: ')
    return year_name

def create_year_getname() -> str:
    clear_terminal()
    year = input('Введите имя года: ')
    return year

def creat_year_qulist() -> list:
    qulist = []
    print("""Введите даты начала каждой четверти(из 4) в формате
начало_четверти(yyyy-mm-dd) конец_четвери(yyyy-mm-dd)""")
    for i in range(1,5):
        qulist.append(list(input(f'{i}: ').split()))
    return qulist

def delete_year() -> str:
    year = input('Введите название года: ')
    return year