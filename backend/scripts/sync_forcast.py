import os
import sys
# add backend folder to path
sys.path.append(os.path.join("/workspaces/web_fullstack_learn/backend/"))
from database import interface as dbi
import requests
from dotenv import load_dotenv
import datetime
from dateutil.parser import parse

load_dotenv()
DATETIMEFORMAT="%Y-%m-%d %H:%M:%S"

ParameterMap = dict(
    PoP12h = "pop12h",
    T = "temperature_avg",
    RH = "humidity_avg",
    MinCI_index = "ci_min_index",
    MinCI_description = "ci_min_description",
    WS = "windspeed",
    MaxAT = "at_max",
    Wx = "weather",
    MaxCI_index = "ci_max_index",
    MaxCI_description = "ci_max_description",
    MinT = "temperature_min",
    UVI = "uvi",
    WeatherDescription = "description",
    MinAT = "at_min",
    MaxT = "temperature_max",
    WD = "winddirection",
    Td = "temperature_dew",
)

def sync_forcast():
    # get last data
    db = dbi.Database()
    last_data = db.get_last()
    if len(last_data)>0:
        st = parse(last_data[0][1])  # string
        st+=datetime.timedelta(seconds=1)
        st = st.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        st=""

    query = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-007?Authorization={CWBAPI_TOKEN}&format=JSON&locationName={locationName}&timeFrom={st}'.format(
            CWBAPI_TOKEN=os.getenv("CWB_OPENAPI_TOKEN"),
            locationName="中壢區",
            st=st
        )

    res = requests.get(query).json()
    res = res['records']['locations'][0]['location'][0]['weatherElement']

    # package the data
    header = []
    for ele in res:
        header.append(ele["elementName"])
    data = {}
    for i in range(len(res[0]["time"])):
        for ele in res:
            if i>=len(ele["time"]): continue
            if not ele["time"][i]["startTime"] in data.keys():
                data[ele["time"][i]["startTime"]] = {}
            if ele["elementName"] in ["MinCI", "MaxCI"]:
                key = ParameterMap[f"{ele['elementName']}_index"]
                data[ele["time"][i]["startTime"]][key] = ele["time"][i]["elementValue"][0]["value"]
                key = ParameterMap[f"{ele['elementName']}_description"]
                data[ele["time"][i]["startTime"]][key] = ele["time"][i]["elementValue"][0]["value"]
            else:
                key = ParameterMap[ele["elementName"]]
                data[ele["time"][i]["startTime"]][key] = ele["time"][i]["elementValue"][0]["value"]
        
    timelist = list(data.keys())
    timelist.sort()

    for key in timelist:
        tmp = data[key]
        tmp['datetimelst'] = parse(key)
        db.insert(**tmp)

if __name__=="__main__":
    sync_forcast()