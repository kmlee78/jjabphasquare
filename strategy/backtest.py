from typing import List, Dict, Tuple, Optional

import pandas as pd
import numpy as np
import FinanceDataReader as fdr
import quantstats as qs

from main.models import CorpModel

qs.extend_pandas()


def get_price_df(
    tickers: List[str], start_date: str, end_date: Optional[str] = None
) -> pd.DataFrame:
    """수정 주가 데이터를 리턴한다.

    Args:
        tickers: 종목코드
        start_date: 탐색 시작 시점
        end_date: 탐색 종료 시점
    """
    df = pd.DataFrame()

    if isinstance(tickers, str):
        tickers = [tickers]
    for ticker in tickers:
        df_temp = fdr.DataReader(ticker, start_date, end_date)
        df.loc[:, ticker] = df_temp["Close"]
    df.columns = tickers
    return df


def get_return_df(df_price: pd.DataFrame) -> pd.DataFrame:
    """일간 수익률을 리턴한다.

    Args:
        df_price: 수정 주가 데이터
    """
    df_return = df_price.pct_change().fillna(0)
    return df_return


def get_portfolio_return(df_price: pd.DataFrame) -> pd.Series:
    """포트폴리오 누적 수익률을 계산한다.

    Args:
        df_price: 수정 주가에 대한 데이터
    """
    df_cum_rtn = (df_price - df_price.iloc[0]) / df_price.iloc[0]
    portfolio_cum_rtn = df_cum_rtn.mean(axis=1)
    portfolio_rtn = (portfolio_cum_rtn + 1) / (portfolio_cum_rtn.shift(1) + 1) - 1

    return portfolio_rtn


def names_to_tickers(names: Optional[str]) -> List[str]:
    """종목명을 종목 코드로 변환한다.

    Args:
        names: 종목명
        market: 거래 시장 심볼
    """
    tickers = []
    for name in names:
        try:
            stock_code = CorpModel.objects.get(corp_name=name).stock_code
            tickers.append(stock_code)
        except Exception:
            continue
    return tickers


def prepare_inputs(
    start_date: str,
    end_date: Optional[str] = None,
    names: Optional[str] = None,
    tickers: Optional[str] = None,
    benchmark="KS11",
) -> Tuple[pd.Series, pd.Series]:
    """리밸런싱 전략을 적용하지 않았을 때(보유 종목이 변하지 않았을 때) 일간 수익률을 리턴한다.

    Args:
        start_date: 시작 시점
        end_date: 종료 시점
        names: 종목명
        tickers: 종목 코드
        benchmark: 벤치마크 심볼
    """
    if names is not None:
        tickers = names_to_tickers(names)
    elif tickers is None:
        raise Exception("Either names or tickers are needed")

    df_price = get_price_df(tickers, start_date, end_date)
    portfolio_rtn = get_portfolio_return(df_price).iloc[1:]

    benchmark_price = get_price_df(benchmark, start_date, end_date)
    benchmark_rtn = get_return_df(benchmark_price).iloc[1:].squeeze()

    return portfolio_rtn, benchmark_rtn


def holding_cash(
    start_date: str, end_date: Optional[str] = None, benchmark: str = "KS11"
) -> Tuple[pd.Series, pd.Series]:
    """리밸런싱 없이 현금만을 보유하고 있을 때 일간 수익률을 리턴한다.

    Args:
        start_date: 시작 시점
        end_date: 종료 시점
        benchmark: 벤치마크 심볼
    """
    benchmark_price = get_price_df(benchmark, start_date, end_date)
    benchmark_rtn = get_return_df(benchmark_price).iloc[1:].squeeze()

    portfolio_rtn = benchmark_rtn.copy()
    portfolio_rtn.iloc[:] = np.nan

    return portfolio_rtn, benchmark_rtn


def rebalanced_inputs(
    rebalancing_history: Dict[str, List[str]], benchmark: str = "KS11"
) -> Tuple[pd.Series, pd.Series]:
    """리밸런싱 전략에 따른 일간 수익률을 벤치마크(코스피)와 함께 리턴한다.

    Args:
        rebalancing_history: 시점에 따라 리스트로 정리된 종목들
        benchmark: 벤치마크 심볼
    """
    portfolio_rtn = pd.Series(dtype="float64")
    benchmark_rtn = pd.Series(dtype="float64")

    dates = list(rebalancing_history.keys())

    for idx, start_date in enumerate(dates):
        if idx != len(dates) - 1:
            end_date = dates[idx + 1]
        else:
            break
        if not rebalancing_history[start_date]:
            prtn_temp, brtn_temp = holding_cash(start_date, end_date)
        else:
            prtn_temp, brtn_temp = prepare_inputs(
                start_date=start_date,
                end_date=end_date,
                names=rebalancing_history[start_date],
                benchmark=benchmark,
            )
        portfolio_rtn = pd.concat([portfolio_rtn, prtn_temp])
        benchmark_rtn = pd.concat([benchmark_rtn, brtn_temp])

    return portfolio_rtn, benchmark_rtn


def get_backtest_page(portfolio_rtn: pd.Series, benchmark_rtn: pd.Series):
    """백테스팅 결과 페이지를 생성한다."""
    output_path = "strategy/templates/strategy/detail.html"
    qs.reports.html(portfolio_rtn, benchmark_rtn, output=output_path)
