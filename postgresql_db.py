import psycopg2
import conf
from sys import exit

db = None

def connect() :
    global db
    try:
        db = psycopg2.connect(dbname=conf.db_name,host=conf.db_host,port=conf.db_port,user=conf.db_user,password=conf.db_password)
    except Exception as e:
        #need print
        exit()

def exist_in_db(id_column_name, table_name, column_name, name) -> int:
    """Проверяет наличие value в таблице table_name в столбце  column_name\n
    Возращает:\n-1 - ошибка обращения к бд\n0 - не удалось найти\n int(id_colum_name) > 0 - id найденого объекта"""
    res = None
    try:
        with db.cursor() as curr:
            curr.execute(f'SELECT {id_column_name} FROM {table_name} WHERE {column_name} = %s;',
                (name,))
        
            res = curr.fetchone()[0]
            if res == None:
                return 0
    except Exception as e:
        #need print
        return -1
    return res

def exist_year_name(year_name) -> int:
    return exist_in_db('year_id', 'education_year', 'year_name', year_name)

def exist_subject_name(subject_name) -> int:
    return exist_in_db('subject_id', 'subjects', 'subject_name', subject_name)



def create_year(year_name,quarterlist) -> int:
    """Создание учебново года в БД\n
    Передается:\nyear_name - проверенное име учебного года\n
    quarterlist - список четвертей в виде кортеджей(с информацией о четверти{yyyy-mm-dd})\n"""
    try:
        with db.cursor() as curr:
            qu_id_list = []
            for i in range(4):
                curr.execute(f'INSERT INTO quarters(start_date,finish_date) VALUES (%s,%s) RETURNING quarter_id;',
                    quarterlist[i])
                qu_id_list.append(curr.fetchone()[0])

            educ_year = [year_name] + qu_id_list
            
            curr.execute(f'INSERT INTO education_years(year_name,quarter0_id,quarter1_id,quarter2_id,quarter3_id) VALUES (%s,%s,%s,%s,%s);',
                tuple(educ_year))

    except Exception as e:
        #need print
        db.rollback()
        return 1
    db.commit()
    return 0

def create_subject(subject_name) -> int:
    'Создает учебный предемет в БД'
    try:
        with db.cursor() as curr:
            curr.execute('INSERT INTO subjects(subject_name) VAlUES (%s);',
                (subject_name,))
    except Exception as e:
        db.rollback()
        #need print
        return 1
    db.commit()
    return 0


class Education_year:
    def __init__(self,year_id) -> None:
        self.year_id = year_id
        self.quarterlist_id = []
        try:
            with db.cursor() as curr:
                curr.execute(f'SELECT quarter0_id,quarter1_id,quarter2_id,quarter3_id FROM education_years WHERE year_id = %s;',
                    (year_id,))
                
                self.quarterlist_id = list(curr.fetchone())
        except Exception as e:
            #need print
            pass
            
