from django.shortcuts import render

import FinanceDataReader as fdr
import pandas as pd
import plotly.graph_objects as go

from .models import ChartModel
from .forms import ChartForm


def chart_page(request):
    chart_form = ChartForm()
    return render(request, "chart/index.html", {"form": chart_form})


def chart_detail(request, stock_code):
    corp = ChartModel.objects.get(stock_code=stock_code)

    today = pd.Timestamp.today()
    start_point = today - pd.Timedelta(days=365)
    df = fdr.DataReader(stock_code, start_point, today)
    df["ma_60"] = df["Close"].rolling(window=60).mean()
    df["ma_20"] = df["Close"].rolling(window=20).mean()
    df["ma_10"] = df["Close"].rolling(window=10).mean()

    candle = go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="일봉 차트",
        increasing_line_color="red",
        decreasing_line_color="blue",
    )
    layout = go.Layout(
        width=1000,
        height=625,
        autosize=True,
        title="",
        plot_bgcolor="#fafafa",
        xaxis=dict(title="기 간", showgrid=True),
        yaxis=dict(title="주 가", showgrid=True),
    )
    ema_trace1 = go.Scatter(
        x=df.index, y=df["ma_10"], mode="lines", name="10일선", line=dict(color="black")
    )
    ema_trace2 = go.Scatter(
        x=df.index, y=df["ma_20"], mode="lines", name="20일선", line=dict(color="green")
    )
    ema_trace3 = go.Scatter(
        x=df.index, y=df["ma_60"], mode="lines", name="60일선", line=dict(color="orange")
    )

    fig = go.Figure(data=candle, layout=layout)
    fig.add_trace(ema_trace1)
    fig.add_trace(ema_trace2)
    fig.add_trace(ema_trace3)
    fig.update_yaxes(fixedrange=False)
    fig.write_html("chart/templates/chart/detail.html")
    return render(request, "chart/chart_detail.html", {"corp": corp})


def chart_load(request):
    return render(request, "chart/detail.html")
