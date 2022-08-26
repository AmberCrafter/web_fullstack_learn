import psycopg2
from typing import Optional, Union
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
TABLENAME="forcast"
DATETIMEFORMAT="%Y-%m-%d %H:%M:%S"

class Singleton_meta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_meta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass = Singleton_meta):
    '''
    In release product, database need to change into other PaaS,
    which will advoid missing the data when rebuild the product.
    Recommand to use the firebase.
    '''

    def __init__(self):
        # database_path = os.getenv("QUEST_DATABASE")
        database_path = os.getenv("DATABASE_URL")
        self.db = psycopg2.connect(database_path, sslmode='require')
        self.cur = self.db.cursor()
        self.exe = self.cur.execute
        self.fa = self.cur.fetchall

        self.__table_create_forcasat()

    def __table_create_forcasat(self) -> bool:
        # at: 體感溫度
        table_information = """
            id serial primary key,
            datetimelst text,
            pop12h int,
            temperature_avg int,
            temperature_min int,
            temperature_max int,
            temperature_dew int,
            humidity_avg int,
            ci_min_index int,
            ci_min_description text,
            ci_max_index int,
            ci_max_description text,
            windspeed int,
            winddirection text,
            at_min int,
            at_max int,
            weather text,
            uvi int, 
            description text,
            updatetime text
        """

        try:
            query = f"create table if not exists {TABLENAME} ({table_information});"
            self.exe(query)
        except Exception as err:
            print(err)
            return False
        return True

    def get_header(self):
        query = f'Select * from information_schema.columns;'
        self.exe(query)
        info = self.fa()
        # return [(val[1], val[2]) for val in info]
        return info

    def insert(self, 
        datetimelst: Optional[datetime.datetime]=None, 
        pop12h: Optional[int]=None, 
        temperature_avg: Optional[int]=None,
        temperature_min: Optional[int]=None,
        temperature_max: Optional[int]=None,
        temperature_dew: Optional[int]=None,
        humidity_avg: Optional[int]=None,
        ci_min_index: Optional[int]=None,
        ci_min_description: Optional[str]=None,
        ci_max_index: Optional[int]=None,
        ci_max_description: Optional[str]=None,
        windspeed: Optional[int]=None,
        winddirection: Optional[str]=None,
        at_min: Optional[int]=None,
        at_max: Optional[int]=None,
        weather: Optional[str]=None,
        uvi: Optional[int]=None,
        description: Optional[str]=None,
        updatetime: datetime.datetime = datetime.datetime.now().strftime(DATETIMEFORMAT)
    ):
        keys = [
            "datetimelst",
            "pop12h",
            "temperature_avg",
            "temperature_min",
            "temperature_max",
            "temperature_dew",
            "humidity_avg",
            "ci_min_index",
            "ci_min_description",
            "ci_max_index",
            "ci_max_description",
            "windspeed",
            "winddirection",
            "at_min",
            "at_max",
            "weather",
            "uvi",
            "description",
            "updatetime"
        ]
        headers = []
        values = []
        for key in keys:
            tmp = locals()[key]
            if not isinstance(tmp, type(None)):
                headers.append(key)
                if type(tmp)==datetime.datetime:
                    values.append(f'"{tmp.strftime(DATETIMEFORMAT)}"')
                elif type(tmp)==str:
                    values.append(f'"{tmp}"')
                else: 
                    values.append(str(tmp))
        query = "Insert into {TABLENAME} ({headers}) values ({values});".format(
            TABLENAME = TABLENAME,
            headers = ','.join(headers),
            values = ','.join(values),
        )
        self.exe(query)
        self.db.commit()


    def get_all(self, limit: Optional[int]=None):
        if isinstance(limit, type(None)):
            query = f"select * from {TABLENAME} order by datetimelst asc;"
            self.exe(query)
            return self.fa()
        else: 
            query = f"select * from {TABLENAME} order by datetimelst asc limit {limit};"
            self.exe(query)
            return self.fa()
    
    def get_all_singal_para(self, parameter: str):
        query = f'select {parameter} from {TABLENAME} order by datetimelst asc;'
        self.exe(query)
        return self.fa()

    def get_id(self, index: int):
        query = f"select * from {TABLENAME} where id={index};"
        self.exe(query)
        return self.fa()

    def get_datetime(self, datetimelst: datetime.datetime):
        query = f'select * from {TABLENAME} where datetimelst="{datetimelst}";'
        self.exe(query)
        return self.fa()

    def get_datetime_range(self, starttime: datetime.datetime, endtime: datetime.datetime):
        query = f'select * from {TABLENAME} where datetimelst between "{starttime}" and "{endtime}" order by datetimelst asc;'
        self.exe(query)
        return self.fa()

    def get_last(self, index: Optional[int]=None):
        query = f"select * from {TABLENAME} order by id desc limit 1;"
        self.exe(query)
        return self.fa()

    def update_id(self, index: int, parameters: list[str], values: Union[list[str], list[int]]) -> bool:
        currtime = datetime.datetime.now().strftime(DATETIMEFORMAT)
        # check header and value nums
        if len(parameters)!=len(values): 
            raise f"{currtime} [ERROR]: Numbers of parameter and value element not match. (parameter: {len(parameters)}; value: {len(values)})"

        values = [str(val) if type(val)==int else f'"{val}"' for val in values]
        setter = ','.join([f"{key}={val}" for key, val in zip(parameters, values)])
        query = f'update {TABLENAME} set {setter}, updatetime="{currtime}" where id={index};'
        try:
            self.exe(query)
            self.db.commit()
            return True
        except Exception as err:
            print(f"{currtime} [Error]: Update data failed. {err}")
            return False

    def update_datetime(self, datetimelst: datetime.datetime, parameters: list[str], values: Union[list[str], list[int]]) -> bool:
        currtime = datetime.datetime.now().strftime(DATETIMEFORMAT)
        # check header and value nums
        if len(parameters)!=len(values): 
            raise f"{currtime} [ERROR]: Numbers of parameter and value element not match. (parameter: {len(parameters)}; value: {len(values)})"

        values = [str(val) if type(val)==int else f'"{val}"' for val in values]
        setter = ','.join([f"{key}={val}" for key, val in zip(parameters, values)])
        query = f'update {TABLENAME} set {setter}, updatetime="{currtime}" where datetimelst="{datetimelst.strftime(DATETIMEFORMAT)}";'
        try:
            self.exe(query)
            self.db.commit()
            return True
        except Exception as err:
            print(f"{currtime} [Error]: Update data failed. {err}")
            return False

    def delete_id(self, index: int) -> bool:
        currtime = datetime.datetime.now().strftime(DATETIMEFORMAT)
        query = f'delete from {TABLENAME} where id={index};'
        try:
            self.exe(query)
            self.db.commit()
            return True
        except Exception as err:
            print(f"{currtime} [Error]: Update data failed. {err}")
            return False

    def delete_datetime(self, datetimelst: datetime.datetime) -> bool:
        currtime = datetime.datetime.now().strftime(DATETIMEFORMAT)
        query = f'delete from {TABLENAME} where datetimelst="{datetimelst.strftime(DATETIMEFORMAT)}";'
        try:
            self.exe(query)
            self.db.commit()
            return True
        except Exception as err:
            print(f"{currtime} [Error]: Update data failed. {err}")
            return False

if __name__=="__main__":
    # db = Database()
    # db.insert(1,2,3,4,5)

    # test singleton
    db1 = Database()
    db2 = Database()
    print(db1, db2)