import FinanceDataReader as fdr
import pandas as pd
import plotly.graph_objects as go


def get_chart(stock_code, period, moving_average):
    today = pd.Timestamp.today()
    start_point = today - pd.Timedelta(days=int(period))
    df = fdr.DataReader(stock_code, start_point, today)

    for ma in moving_average:
        df[f"ma_{ma}"] = df["Close"].rolling(window=int(ma)).mean()

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
        title=f"검색 기간: 최근 {period}일",
        plot_bgcolor="#fafafa",
        xaxis=dict(title="기 간", showgrid=True),
        yaxis=dict(title="주 가", showgrid=True),
    )

    fig = go.Figure(data=candle, layout=layout)
    for ma in moving_average:
        fig.add_trace(
            go.Scatter(x=df.index, y=df[f"ma_{ma}"], mode="lines", name=f"{ma}일선")
        )
    fig.update_yaxes(fixedrange=False)
    fig.write_html("chart/templates/chart/detail.html")
