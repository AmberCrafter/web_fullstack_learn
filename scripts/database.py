import os
import sys
# add backend folder to path
sys.path.append(os.path.join("/workspaces/web_fullstack_learn/"))
import datetime
from dateutil.parser import parse

from data_model import ForcastInfo, Parameter, ResponseGetDatetime, ResponseGetForcase, ResponseListString
from database import interface_pg as dbi

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
    # print(datas)

    headers = [val[0] for val in db.get_header()]
    
    paras = list(ForcastInfo.__fields__.keys())
    
    res = []
    for values in datas:
        tmp = {}
        for idx,header in enumerate(headers):

            if header in paras:
                if (not values[idx] in [' ', '', 'None']) and (not isinstance(values[idx], type(None))):
                    tmp[header] = values[idx]
                else:
                    tmp[header] = None
        print(tmp)
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

def get_forcast_datetime(datetimelst: datetime.datetime) -> ResponseGetForcase:
    db = dbi.Database()
    datas = db.get_datetime(datetimelst)

    headers = [val[0] for val in db.get_header()]
    paras = list(ForcastInfo.__fields__.keys())
    res = []
    for values in datas:
        tmp = {}
        for idx,header in enumerate(headers):
            if header in paras:
                if (not values[idx] in [' ', '', 'None']) and (not isinstance(values[idx], type(None))):
                    tmp[header] = values[idx]
                else:
                    tmp[header] = None
        res.append(ForcastInfo.parse_obj(tmp))

    res = dict(results=res)
    res = ResponseGetForcase.parse_obj(res)
    return res

def get_header() -> ResponseListString:
    db = dbi.Database()
    headers = [val[0] for val in db.get_header()]
    res = ResponseListString.parse_obj(
        dict(results=headers)
    )
    return res