import requests
from datetime import datetime
import re
import os

from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv(".env")

BASEURL = "https://opendart.fss.or.kr/api"
DART_REPORT_URL = "http://dart.fss.or.kr"
URL_COMPONENT_KEYS = ["rcpNo", "dcmNo", "eleId", "offset", "length", "dtd"]
QUARTERS = {
    1: "분기보고서",
    2: "반기보고서",
    3: "분기보고서",
    4: "사업보고서",
}


def get_report_list(
    code: str, start: datetime.date, end: datetime.date
) -> pd.DataFrame:
    """주어진 기간에 공시된 기업보고서의 리스트를 리턴한다.

    Args:
        code: 기업 코드
        start: 기간 시작 날짜
        end: 기간 끝 날짜
    """
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
    api_key = os.getenv("DART_API_KEYS")
    payload = {"crtfc_key": api_key, **payload}
    res = requests.get(url, params=payload)
    data = res.json()
    if data["status"] != "000":
        raise Exception(data["message"], data["status"])

    df_data = pd.DataFrame(data["list"])
    return df_data


def get_report_menu(rcept_no: str) -> pd.DataFrame:
    """공시보고서의 상세 리스트를 리턴한다.

    Args:
        rcept_no: 보고서 번호
    """
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


def get_account_month(corp_code: str) -> int:
    """기업의 결산월을 리턴한다.

    Args:
        corp_code: 기업 코드
    """
    payload = {"corp_code": corp_code}
    url = f"{BASEURL}/company.json"
    api_key = os.getenv("DART_API_KEYS")
    payload = {"crtfc_key": api_key, **payload}

    res = requests.get(url, params=payload)
    data = res.json()
    acc_mt = int(data["acc_mt"])
    return acc_mt


def get_rcept_no(corp_code: str, bsns_year: int, quarter: int) -> str:
    """특정 분기에 공시된 기업의 보고서 번호를 리턴한다.

    Args:
        corp_code: 기업 코드
        bsns_year: 연도
        quarter: 분기
    """
    today = datetime.today()
    df = get_report_list(corp_code, datetime(bsns_year - 1, 1, 1), today)
    if quarter == 4:
        bsns_year += 1
    month = get_account_month(corp_code) + quarter * 3
    if month > 12:
        month -= 12
    quarter = QUARTERS[quarter]
    list_len = df.shape[0]

    for i in range(list_len):
        report_nm = df.loc[i, "report_nm"]
        report_year = re.sub(r"[^\d]", "", report_nm)[:4]
        report_month = re.sub(r"[^\d]", "", report_nm)[4:]
        if (
            bsns_year == int(report_year)
            and quarter in report_nm
            and int(report_month) == month
        ):
            return df.loc[i, "rcept_no"]
    return


def get_url(rcept_no: str, connected: bool) -> str:
    """보고서에서 재무제표가 기록된 페이지의 url을 리턴한다.

    Args:
        rcept_no: 보고서 번호
        connected: 재무제표의 연결 여부
    """
    report_menu = get_report_menu(rcept_no)
    report_menu["title"] = report_menu["title"].str.replace(r"\([^)]*\)|[^가-힣]", "")
    if connected:
        url = report_menu[report_menu["title"] == "연결재무제표"]["url"].values[0]
    else:
        url = report_menu[report_menu["title"] == "재무제표"]["url"].values[0]
    return url
