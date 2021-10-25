import requests
from datetime import datetime
import re
import os

import pandas as pd
import numpy as np


BASEURL = "https://opendart.fss.or.kr/api"
DART_REPORT_URL = "http://dart.fss.or.kr"
URL_COMPONENT_KEYS = ["rcpNo", "dcmNo", "eleId", "offset", "length", "dtd"]
API_KEY = os.getenv("DART_API_KEYS")


def get_report_list(
    code: str, start: datetime.date, end: datetime.date
) -> pd.DataFrame:
    start = start.strftime("%Y%m%d")
    end = end.strftime("%Y%m%d")

    payload = {
        "corp_code": code,
        "bgn_de": start,
        "end_de": end,
        "last_reprt_at": "N",
        "page_no": 1,
        "page_count": 100,
        "pblntf_ty": "A",
    }

    path = "/list.json"
    url = f"{BASEURL}{path}"
    api_key = API_KEY
    payload = {"crtfc_key": api_key, **payload}
    res = requests.get(url, params=payload)
    data = res.json()
    if data["status"] != "000":
        raise Exception(data["message"], data["status"])

    df_data = pd.DataFrame(data["list"])
    return df_data


def get_report_menu(rcept_no: str) -> pd.DataFrame:
    url = f"{DART_REPORT_URL}/dsaf001/main.do?rcpNo={rcept_no}"
    data = requests.get(url)

    titles = re.findall("\\['text'\\] = \"(.*)\";", data.text)
    url_components = []
    for key in URL_COMPONENT_KEYS:
        url_components.append(re.findall(f"\\['{key}'\\] = \"(.*)\";", data.text))
    keys = np.transpose(url_components)

    report_url = f"{DART_REPORT_URL}/report/viewer.do?"
    urls = [
        f"{report_url}rcpNo={x[0]}&dcmNo={x[1]}"
        f"&eleId={x[2]}&offset={x[3]}&length={x[4]}&dtd={x[5]}"
        for x in keys
    ]

    df = pd.DataFrame(zip(titles, urls), columns=["title", "url"])
    return df
