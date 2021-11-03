from datetime import time
from typing import List, Dict
import pandas as pd

from .models import CorpDataQuarter, CorpDataYear


def update_point(time_point, yearly) -> pd.Timestamp:
    year = time_point.year
    month = time_point.month
    if yearly:
        if 1 <= month <= 3:
            return pd.Timestamp(year, 4, 1)
        else:
            return pd.Timestamp(year + 1, 4, 1)

    if 4 <= month <= 5:
        month = 6
    elif 6 <= month <= 8:
        month = 9
    elif 9 <= month <= 11:
        month = 12
    elif 1 <= month <= 3:
        month = 4
    else:
        year += 1
        month = 4

    return pd.Timestamp(year, month, 1)


def point_to_apply(time_point: pd.Timestamp, yearly) -> str:
    year = time_point.year
    month = time_point.month

    if 4 <= month <= 5:
        if not yearly:
            year -= 1
            month = "12"
    elif 6 <= month <= 8:
        month = "03"
    elif 9 <= month <= 11:
        month = "06"
    elif 1 <= month <= 3:
        year -= 1
        month = "09"
    else:
        month = "09"

    if yearly:
        time_point = str(year - 1)
    else:
        time_point = str(year) + month

    return time_point


def get_stocks(time_point, model, filter, data_to_use) -> List:
    if data_to_use == "quarter":
        time_point = point_to_apply(time_point, yearly=False)
    else:
        time_point = point_to_apply(time_point, yearly=True)
    result = model.objects.filter(time_point=time_point)
    for key in filter:
        if key == "pbr":
            result = result.filter(pbr__lt=filter[key])
        elif key == "per":
            result = result.filter(per__lt=filter[key])
        elif key == "roe":
            result = result.filter(roe__gt=filter[key])
        elif key == "debt_ratio":
            result = result.filter(debt_ratio__lt=filter[key])
        elif key == "operating_margin":
            result = result.filter(operating_margin__gt=filter[key])
        elif key == "borrowing_dependence":
            result = result.filter(borrowing_dependence__lt=filter[key])
        else:
            continue

    stocks = [x.corp_name for x in result]
    return stocks


def get_filter(parameters) -> Dict:
    filter = {}
    for key in parameters:
        if key != "csrfmiddlewaretoken":
            if key == "start_point":
                filter[key] = parameters[key]
            else:
                filter[key] = float(parameters[key])
    return filter


def get_history(model, parameters, data_to_use) -> Dict:
    history = {}
    filter = get_filter(parameters)
    time_point = pd.Timestamp(filter["start_point"])
    end_point = pd.Timestamp.today()

    while time_point < end_point:
        stocks = get_stocks(time_point, model, filter, data_to_use)
        time_point_str = time_point.strftime("%Y-%m-%d")
        history[time_point_str] = stocks
        if data_to_use == "quarter":
            time_point = update_point(time_point, yearly=False)
        else:
            time_point = update_point(time_point, yearly=True)

    end_point_str = end_point.strftime("%Y-%m-%d")
    history[end_point_str] = ["EOS"]
    return history


def backtest(data_to_use, parameters):
    if data_to_use == "quarter":
        model = CorpDataQuarter
    else:
        model = CorpDataYear
    history = get_history(model, parameters, data_to_use)
    return history
