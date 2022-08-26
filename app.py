import datetime
from typing import Union
from fastapi import FastAPI
from database import interface_pg as dbi
from data_model import ForcastInfo, Parameter, ResponseGetDatetime, ResponseGetForcase, ResponseListString
from fastapi.middleware.cors import CORSMiddleware

from scripts import database as dbscript
from scripts import sync_forcast as sync_script

ORIGINS = [
    "http://localhost",
    "http://localhost:5500",
    "http://localhost:5501",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
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


# create/update
@app.get("/database")
async def checker(): 
    db = dbi.Database()
    query = "Select * from forcast;"
    db.exe(query)
    print(db.fa())
    print(db)


@app.post("/forcast/put/{Datetime}/")
async def forcast_put(Datetime: datetime.datetime, parameter: Parameter):
    """
    IMPOTAINT: You need to clear the body's parameter which not need, 
    otherwise they will be insert into the database.

    Put a new value into database.

    Insert a new one if the data not exist , otherwise update it.

    Datetime format: YYYY-MM-DD HH:MM:SS
    """

    dbscript.put(parameter, datetimelst=Datetime)


# read
@app.get("/forcast/get/{Days}", response_model=ResponseGetForcase)
async def forcast_get(Days: int):
    """
    start from current time
    Datetime format: YYYY-MM-DD HH:MM:SS
    """
    res = dbscript.get_forcast_nday(Days)
    res = dict(results=res)
    res = ResponseGetForcase.parse_obj(res)
    return res

# delete
@app.get("/forcast/delete/{Datetime}")
async def forcast_delete(Datetime: datetime.datetime):
    """
    Delete data by datetime
    Datetime format: YYYY-MM-DD HH:MM:SS
    """
    dbscript.delete_forcast(Datetime)

# sync
@app.get("/forcast/sync")
async def forcast_sync():
    """
    Sync forcast data
    """
    sync_script.sync_forcast()

# get datetimelist
@app.get("/forcast/get_all/datetime", response_model=ResponseGetDatetime)
async def forcast_get_all_datetime():
    """
    Get all forcast data's datetime
    """
    return dbscript.get_all_datetime()

# select single data by datetime
@app.get("/forcast/select/{Datetime}", response_model=ResponseGetForcase)
async def forcast_select_datetime(Datetime: datetime.datetime):
    """
    Select data by datetime
    Datetime format: YYYY-MM-DD HH:MM:SS
    """
    return dbscript.get_forcast_datetime(Datetime)

# get header
@app.get("/forcast/get_header", response_model=ResponseListString)
async def forcast_get_header():
    """
    Get all forcast data's datetime
    """
    return dbscript.get_header()

# if __name__=="__main__":
#     app.