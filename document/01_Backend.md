# Backend Design

## TODO List
 - [x] route
 - [x] CRUD
   - [x] create
   - [x] read
   - [x] update
   - [x] delete
 - [x] SQL interface (ORM)
 - [x] stream scripts
 - [x] data model (FastAPI required)
 - [x] CORS
 - [x] Startup

---
## Install

Install fastapi
```bash
> pip install fastapi
or 
> pip3 install fastapi
```
> `pip` alias `pip3` after here

Install uvicorn (Async CGI)
```bash
> pip install "uvicorn[standard]"
```

Run server
```bash
> uvicorn main:app --host 0.0.0.0 --port 80
```
And we can launch the website at [localhost:80](http://127.0.0.1:80), more detail information can find in [offical website](https://fastapi.tiangolo.com/deployment/manually/?h=uvicorn#deployment-concepts).


---
## Basic

1. Get mehtod
```python
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

2. Post method
```python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

---
## Routing Design (RESTful like)

You can also find this informatino in OpenAPI, which auto-generate by FastAPI.
URL: {website.address:port}/docs

 * root: /forcast
   + /put/{Datetime}/: [Post] Update/Insert the forcast data at {Datetime}
   + /get/{Days}: [Get] Query {Days} forcast's data after current datetime
   + /delete/{Datetime}: [Get] Delete the forcast data at {Datetime}
   + /sync: [Get] Sync forcast data
   + /get_all/datetime: [Get] Get all forcast data's datetime in database
   + /select/{Datetime}: [Get] Get data at {Datetime}
   + /get_header: [Get] Get all forcast data header in database set

## SQL interface

In this project, I'll like to build the sql interface by myself. The reason is that SQL language is most powerful than the ORM under complex cases. 
> Another reason is that I'll combine database server and web server in one machine in this case. This mean there has no limitation on database calculation. More over, the SQL language is usually more faster on data search.

Here is the sqlite3 version, you can also find postqresql version on my [github](https://github.com/AmberCrafter/web_fullstack_learn/blob/heroku_backend/database/interface_pg.py).

> Due to different type defined and syntex of database, we need to build a custom database interface for each one. And this is done by ORM if you use it.

***Briefly show of the code***

1. Setup singleton to make sure there has only one sql connection by each worker
```python
// backend/database/interface.py
class Singleton_meta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_meta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass = Singleton_meta):
    ...
```

2. Setup database table
```python
class Database(metaclass = Singleton_meta):
    ...
    def __table_create_forcasat(self) -> bool:
        # at: 體感溫度
        table_information = """
            id integer primary key autoincrement,
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
    ...
```

3. Setup other function
 - get_header
 - insert
 - get_all
 - get_all_singal_para
 - get_id : get data by id
 - get_datetime : get data by datetime
 - get_datetime_range : get data by datetime range
 - get last
 - update_id : update data by id
 - update_datetime : update data by datetime
 - delete_id : delete data by id
 - delete_datetime : delete data by datetime

## Data model
Based on [offical documents](https://fastapi.tiangolo.com/tutorial/body/#create-your-data-model).

The data model is used to wrap the pyhton data into FastAPI arguments.

```python
# /backend/app.py
from data_model import ForcastInfo, Parameter, ResponseGetDatetime, ResponseGetForcase, ResponseListString


# /backend/data_model.py
import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel

class Parameter(BaseModel):
    pop12h: int | None = None
    temperature_avg: int | None = None
    temperature_min: int | None = None
    temperature_max: int | None = None
    temperature_dew: int | None = None
    humidity_avg: int | None = None
    ci_min_index: int | None = None
    ci_min_description: str | None = None
    ci_max_index: int | None = None
    ci_max_description: str | None = None
    windspeed: int | None = None
    winddirection  : str | None = None
    at_min: int | None = None
    at_max: int | None = None
    weather: str | None = None
    uvi: int | None = None
    description: str | None = None

class ForcastInfo(BaseModel):
    datetimelst: datetime.datetime
    pop12h: int | None = None
    temperature_avg: int | None = None
    temperature_min: int | None = None
    temperature_max: int | None = None
    temperature_dew: int | None = None
    humidity_avg: int | None = None
    ci_min_index: int | None = None
    ci_min_description: str | None = None
    ci_max_index: int | None = None
    ci_max_description: str | None = None
    windspeed: int | None = None
    winddirection  : str | None = None
    at_min: int | None = None
    at_max: int | None = None
    weather: str | None = None
    uvi: int | None = None
    description: str | None = None

class ResponseGetForcase(BaseModel):
    results: list[ForcastInfo]

class ResponseGetDatetime(BaseModel):
    results: list[datetime.datetime]

class ResponseListString(BaseModel):
    results: list[str | None]
```


## CORS
[MDN](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/CORS)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ORIGINS = [
    "http://localhost",
    "http://localhost:5500",  # used by LiveServer
    "http://127.0.0.1:5500",  # used by LiveServer
    "*"
]

app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

```

---
## Note.
### Different between Sqlite3 and PostgresQL
1. The query syntex
 - sqlite3: string wrap by double quotes (")
 - postgresql: string wrap by single quote (')
2. Datetime type
 - sqlite3: text -> return string in python
 - postgresql: date, time, timestamp... -> return datetime in python


## Future work
1. Re-design the database, which can record more than one site data
2. Build a interface layer of database to make the operation uniform.

---
Reference:

https://fastapi.tiangolo.com/

https://developer.mozilla.org/zh-TW/docs/Web/HTTP/CORS
