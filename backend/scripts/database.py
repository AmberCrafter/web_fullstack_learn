import os
import sys
# add backend folder to path
sys.path.append(os.path.join("/workspaces/web_fullstack_learn/backend/"))
import datetime
from dateutil.parser import parse

from data_model import ForcastInfo, Parameter, ResponseGetDatetime
from database import interface as dbi

def put(parameter: Parameter, *args, **kwargs)->bool:
    parameter = parameter.dict()
    
    db = dbi.Database()
    # check data exist or not
    res = db.get_datetime(kwargs['datetimelst'])
    status = False
    if len(res)>0:
        headers = list(parameter.keys())
        values = [parameter[key] for key in headers]
        status = db.update_datetime(datetimelst=kwargs['datetimelst'], parameters = headers, values = values)
    else:
        parameter['datetimelst'] = kwargs['datetimelst']
        status = db.insert(**parameter)
    return status

def get_forcast_nday(days: int) -> list[ForcastInfo]:
    starttime = datetime.datetime.now()
    endtime = starttime + datetime.timedelta(days=days)
    db = dbi.Database()
    datas = db.get_datetime_range(starttime, endtime)

    headers = [val[0] for val in db.get_header()]
    
    paras = list(ForcastInfo.__fields__.keys())
    
    res = []
    for values in datas:
        tmp = {}
        for idx,header in enumerate(headers):

            if header in paras:
                tmp[header] = values[idx] if values[idx]!=' ' else None
        res.append(ForcastInfo.parse_obj(tmp))

    return res

def delete_forcast(datetimelst: datetime.datetime) -> bool:
    db = dbi.Database()
    return db.delete_datetime(datetimelst)

def get_all_datetime() -> ResponseGetDatetime:
    db = dbi.Database()
    res = dict(results=[parse(val[0]) for val in db.get_all_singal_para("datetimelst")])
    res = ResponseGetDatetime.parse_obj(res)
    return res