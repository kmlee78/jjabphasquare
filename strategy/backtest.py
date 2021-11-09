import pandas as pd
import numpy as np
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import quantstats as qs

qs.extend_pandas()


def get_price_df(tickers, start_date, end_date=None, is_realtime=True):
    """Return the adjusted close prices
    Args:
        tickers (list or str): firms' stock codes
        start_date (str)
        end_date (str, optional)
    Returns:
        DataFrame: adjusted close price
    """

    if not is_realtime:
        if type(tickers) is str:
            tickers = [tickers]
        df = pd.read_pickle("Refined_Data/close_prices.pkl")
        return df.loc[start_date:end_date, tickers]

    df = pd.DataFrame()

    if type(tickers) is str:
        tickers = [tickers]

    for ticker in tickers:
        df_temp = fdr.DataReader(ticker, start_date, end_date)
        df.loc[:, ticker] = df_temp["Close"]

    df.columns = tickers

    return df


def get_return_df(df_price, log_rtn_flag=False):
    """Return the daily returns of stocks

    Args:
        df_price (DataFrame): Adjusted close prices of stocks
        log_rtn_flag (bool): if true, calculate log returns

    Returns:
        DataFrame: daily stocks returns
    """

    if log_rtn_flag:
        df_return = np.log(df_price) - np.log(df_price.shift())  # calculate log return
    else:
        df_return = df_price.pct_change().fillna(0)  # calculate return

    return df_return


def get_portfolio_return(df_price):
    """Return the daily returns of Buy-and-Hold portfolio
    Args:
        df_price (DataFrame): Adjusted close prices of stocks
    Returns:
        Series: daily returns of Buy-and-hold portfolio
    """

    df_cum_rtn = (df_price - df_price.iloc[0]) / df_price.iloc[0]  # 종목별 누적수익률 계산
    portfolio_cum_rtn = df_cum_rtn.mean(axis=1)  # 포트폴리오 누적수익률 계산
    # 포트폴리오 일간수익률 계산
    portfolio_rtn = (portfolio_cum_rtn + 1) / (portfolio_cum_rtn.shift(1) + 1) - 1

    return portfolio_rtn


def names_to_tickers(names, market="KRX"):
    """Convert names to tickers

    Args:
        names (list): firms' names
        market (str, optional): Stock Exchange

    Returns:
        list: firms' tickers
    """

    Stocklist = fdr.StockListing(market)  # dataframe containing ticker and names
    mask = Stocklist["Name"].isin(names)  # filtering

    return Stocklist[mask]["Symbol"].tolist()


def prepare_inputs(
    start_date,
    end_date=None,
    names=None,
    tickers=None,
    benchmark="KS11",
    is_realtime=True,
):
    """Prepare inputs for quantstats reports with buy-and-hold strategy,

    Args:
        start_date (str)
        end_date (str, optional)
        names (list, optional): firms' names. Either names or tickers are required
        tickers (list, optional): firms' tickers. Either names or tickers are required
        benchmark (str, optional): symbol of benchmark

    Returns:
        portfolio_rtn (Series): Daily returns of portfolio
        benchmark_rtn (Series): Daily returns of benchmark
    """

    if names is not None:
        tickers = names_to_tickers(names)
    elif tickers is None:
        raise Exception("Either names or tickers are needed")

    df_price = get_price_df(tickers, start_date, end_date)
    portfolio_rtn = get_portfolio_return(df_price).iloc[1:]  # drop first row

    benchmark_price = get_price_df(benchmark, start_date, end_date, is_realtime)
    benchmark_rtn = get_return_df(benchmark_price).iloc[1:].squeeze()  # drop first row

    return portfolio_rtn, benchmark_rtn


def holding_cash(start_date, end_date=None, benchmark="KS11", is_realtime=True):
    """Prepare inputs for quantstats reports with cash-holding strategy,
    Args:
        start_date (str)
        end_date (str, optional)
        benchmark (str, optional): symbol of benchmark
        is_realtime (bool, optional): until today or not
    Returns:
        portfolio_rtn (Series): Daily returns of portfolio
                                (in this case, return nan series)
        benchmark_rtn (Series): Daily returns of benchmark
    """

    benchmark_price = get_price_df(benchmark, start_date, end_date, is_realtime)
    benchmark_rtn = get_return_df(benchmark_price).iloc[1:].squeeze()  # drop first row

    portfolio_rtn = benchmark_rtn.copy()
    portfolio_rtn.iloc[:] = np.nan

    return portfolio_rtn, benchmark_rtn


def rebalanced_inputs(rebalancing_history, benchmark="KS11"):
    """Prepare inputs for quantstats reports with rebalancing strategy

    Args:
        rebalancing_history (dict): key = rebalancing dates,
                                    value = rebalanced stocks
        benchmark (str, optional): symbol of benchmark

    Returns:
        portfolio_rtn (Series): Daily returns of portfolio
        benchmark_rtn (Series): Daily returns of benchmark
    """

    portfolio_rtn = pd.Series(dtype="float64")
    benchmark_rtn = pd.Series(dtype="float64")

    dates = list(rebalancing_history.keys())

    is_realtime = False if rebalancing_history[dates[-1]] == ["EOS"] else True

    for idx, start_date in enumerate(dates):
        if not idx == len(dates) - 1:
            end_date = dates[idx + 1]
        else:
            if not is_realtime:
                break
            else:
                end_date = None
        if not rebalancing_history[start_date]:  # if filtered nothing(empty list)
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


def get_backtest_page(portfolio_rtn, benchmark_rtn):
    output_path = "strategy/templates/strategy/detail.html"
    qs.reports.html(portfolio_rtn, benchmark_rtn, output=output_path)
