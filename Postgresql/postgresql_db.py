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

#EXISTS
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
    return exist_in_db('year_id', 'education_years', 'year_name', year_name)

def exist_subject_name(subject_name) -> int:
    return exist_in_db('subject_id', 'subjects', 'subject_name', subject_name)


#YEAR
def create_year(year_name,quarterlist) -> int:
    """Создание учебново года в БД\n
    Передается:\nyear_name - проверенное име учебного года\n
    quarterlist - список четвертей из списка(с началом и концом четверти{yyyy-mm-dd})\n"""
    try:
        with db.cursor() as curr:
            curr.execute('INSERT INTO education_years(year_name) VALUES (%s) RETURNING year_id;',
                (year_name,))
            year_id = curr.fetchone()[0]
            for i in quarterlist:
                curr.execute('INSERT INTO quarters(start_date,finish_date,year_id) VALUES (%s,%s,%s);',
                    (i[0],i[1],year_id))
    except Exception as e:
        db.rollback()
        #need print
        return 1
    db.commit()
    return 0

def get_list_year() -> list:
    try:
        year_list = []
        with db.cursor() as curr:
            curr.execute('SELECT year_name FROM education_years;')
            year_list = [i[0] for i in curr.fetchall()]
    except Exception as e:
        #need print
        return []
    return year_list

def delete_year(year_name) -> int:
    try:
        with db.cursor() as curr:
            curr.execute('DELETE FROM education_years WHERE year_name = %s;',
                (year_name,))
    except Exception as e:
        db.rollback()
        #need print
        return 1
    db.commit()
    return 0


#SUBJECT
def create_subject(subj_name) -> int:
    try:
        with db.cursor() as curr:
            curr.execute('INSERT INTO subjects(subject_name) VAlUES (%s);',
                (subj_name,))
    except Exception as e:
        db.rollback()
        #need print
        return 1
    db.commit()
    return 0

def get_list_subject() -> list:
    try:
        subj_list = []
        with db.cursor() as curr:
            curr.execute('SELECT subject_name FROM subjects;')
            subj_list = [i[0] for i in curr.fetchall()]
    except Exception as e:
        #need print
        return []
    return subj_list
    

def delete_subject(subj_name) -> int:
    try:
        with db.cursor() as curr:
            curr.execute('DELETE FROM subjects WHERE subject_name = %s;',
                (subj_name,))
    except Exception as e:
        db.rollback()
        #need print
        return 1
    db.commit()
    return 0


#CLASS
class Education_year:
    def __init__(self,year_id) -> None:
        self.year_id = year_id
        self.quarterlist_id = []
        with db.cursor() as curr:
            curr.execute('SELECT quarter_id FROM quarters WHERE year_id = %s ORDER BY start_date;',
                (year_id,))
            self.quarterlist_id = [i[0] for i in curr.fetchall()]

    def add_mark(self, mark, date, subj_id) -> int:
        quarter_id = None
        try:
            with db.cursor() as curr:
                curr.execute('SELECT quarter_id FROM quarters WHERE year_id = %s AND start_date <= %s AND %s <= finish_date;',
                    (self.year_id, date, date))
                
                quarter_id = curr.fetchone()
                if quarter_id == None:
                    return 2
                else:
                    quarter_id = quarter_id[0]

                curr.execute('INSERT INTO marks(mark, mark_date, subject_id, quarter_id) VALUES (%s,%s,%s,%s);',
                    (mark, date, subj_id, quarter_id))
        except Exception as e:
            db.rollback()
            #need print
            return 1
        db.commit()
        return 0


    def quarter_marks(self, subj_id, quarter_num) -> list:
        try:
            with db.cursor() as curr:
                curr.execute('SELECT AVG(mark) FROM marks WHERE subject_id = %s AND quarter_id = %s;',
                    (subj_id,self.quarterlist_id[quarter_num]))
                mark_list = [curr.fetchone()[0]]

                i = (1 if mark_list[0] % 2 == 0 else 0) 
                mark_list[0] = round(mark_list[0]) - i

                curr.execute('SELECT mark, mark_date FROM marks WHERE subject_id = %s AND quarter_id = %s ORDER BY mark_date;',
                    (subj_id,self.quarterlist_id[quarter_num]))
                mark_list += curr.fetchall()
        except Exception as e:
            #need print
            return [-1]
        return mark_list
