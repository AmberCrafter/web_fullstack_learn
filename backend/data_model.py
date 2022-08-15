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