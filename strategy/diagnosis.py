import pandas as pd
import quantstats as qs

qs.extend_pandas()
today = pd.Timestamp.today().strftime("%Y-%m-%d")


def summary_stats(portfolio_rtn, benchmark_rtn):
    """Return dictionary containing evaluation stats
    Args:
        portfolio_rtn (series): daily returns of portfolio
        benchmark_rtn (series): daily returns of benchmark
    Retruns:
        dict: dictionary containing evaluation stats
    """

    stats = {}
    start_point = portfolio_rtn.index[0].strftime("%Y-%m-%d")
    end_point = portfolio_rtn.index[-1].strftime("%Y-%m-%d")
    stats["points"] = [start_point, end_point]

    strategy_cumulative = round(qs.stats.compsum(portfolio_rtn)[-1] * 100, 2)
    benchmark_cumulative = round(qs.stats.compsum(benchmark_rtn)[-1] * 100, 2)
    stats["cumulative"] = [strategy_cumulative, benchmark_cumulative]

    strategy_cagr = round(qs.stats.cagr(portfolio_rtn) * 100, 2)
    benchmark_cagr = round(qs.stats.cagr(benchmark_rtn) * 100, 2)
    stats["cagr"] = [strategy_cagr, benchmark_cagr]

    strategy_sortino = qs.stats.sortino(portfolio_rtn)
    benchmark_sortino = qs.stats.sortino(benchmark_rtn)
    stats["sortino"] = [strategy_sortino, benchmark_sortino]

    strategy_md = round(qs.stats.max_drawdown(portfolio_rtn) * 100, 2)
    stats["md"] = [strategy_md]

    strategy_recover = qs.stats.recovery_factor(portfolio_rtn)
    benchmark_recover = qs.stats.recovery_factor(benchmark_rtn)
    stats["recover"] = [strategy_recover, benchmark_recover]

    alpha = qs.stats.greeks(portfolio_rtn, benchmark_rtn)["alpha"]
    beta = qs.stats.greeks(portfolio_rtn, benchmark_rtn)["beta"]
    stats["greeks"] = [alpha, beta]

    drawdown = qs.stats.to_drawdown_series(portfolio_rtn)
    df = qs.stats.drawdown_details(drawdown)
    longest_drawdown = df.loc[df["days"] == max(df["days"])].values[0]
    ldd_days = longest_drawdown[3]
    ldd_end = longest_drawdown[2]
    stats["dd"] = [ldd_days, ldd_end]

    return stats


def summary(portfolio_rtn, benchmark_rtn):
    """Return portfolio diagnosis summary
    Args:
        portfolio_rtn (series): daily returns of portfolio
        benchmark_rtn (series): daily returns of benchmark
    Retruns:
        str: sentences of summary
    """

    stats = summary_stats(portfolio_rtn, benchmark_rtn)
    start_point = stats["points"][0]
    end_point = stats["points"][1]
    sentence = (
        "본 진단서는 기간 <{}>~<{}> 내 사용자 설정 포트폴리오의 수익률과 벤치마크(코스피)의 수익률을 비교한 결과 입니다.\n".format(
            start_point, end_point
        )
    )
    sentence += (
        "아래 진단 내용들은 과거에 발생한 수익을 기반으로 한 포트폴리오 지표 분석이므로, 향후 시장 흐름에 따라 평가가 바뀔 수 있습니다.\n\n"
    )

    alpha = stats["greeks"][0]
    beta = stats["greeks"][1]
    sentence += "전반적으로 시장의 변화에 "
    if beta > 1:
        sentence += (
            "민감해 상승장일 때는 더 높은 수익률을, 하락장일 때는 더 낮은 수익률을 보일 수 있는 포트폴리오 입니다.\n추가적으로, "
        )
    elif 0 < beta <= 1:
        sentence += "민감하지 않아 상승장일 때 그다지 높은 수익률을 보여주지 않지만 하락장일 때는 손실을 비교적 작게 할 수 있는 포트폴리오 입니다.\n추가적으로, "
    else:
        sentence += "역행하는 성질을 지닌 포트폴리오 입니다.\n"
        sentence += "경우에 따라 이 포트폴리오는 오히려 시장의 흐름보다 더 안좋은 수익을 낼 수도 있습니다.\n\n"

    if beta > 0:
        if alpha >= 0.25:
            sentence += (
                "이 포트폴리오만이 가지고 있는 수익성은 매우 뛰어난 편이고, 시장 대비 훨씬 높은 수익률을 기록할 수 있습니다.\n"
            )
            sentence += "이는 종목 발굴을 상당히 잘한 편이라 할 수 있습니다.\n\n"
        elif alpha >= 0.15:
            sentence += "이 포트폴리오 자체의 수익성이 뛰어나 시장 대비 훨씬 더 많은 수익을 가져다 줄 수 있습니다.\n"
            sentence += "이는 종목 발굴을 꽤 잘한 편이라 할 수 있습니다.\n\n"
        elif alpha > 0:
            sentence += "이 포트폴리오만의 수익성이 어느정도 있어 추가적인 수익을 가져다 줄 수 있습니다.\n"
            sentence += "이는 종목 발굴을 괜찮게 한 편이라 할 수 있습니다.\n\n"
        else:
            sentence += "경우에 따라 이 포트폴리오는 오히려 시장 보다 못한 수익을 낼 수도 있습니다.\n"
            sentence += "이는 적절한 종목 발굴을 하지 못했을 가능성이 큽니다.\n\n"

    port_cumul = stats["cumulative"][0]
    bench_cumul = stats["cumulative"][1]
    port_cagr = stats["cagr"][0]
    bench_cagr = stats["cagr"][1]
    port_sortino = stats["sortino"][0]
    bench_sortino = stats["sortino"][1]
    sentence += "전체 기간에 대한 포트폴리오의 수익률은 {}%, 벤치마크의 수익률은 {}% 이고,\n".format(
        port_cumul, bench_cumul
    )
    sentence += "연 단위로 보면 각각 연 평균 {}%, {}%의 수익을 낸 것을 확인할 수 있습니다.\n".format(
        port_cagr, bench_cagr
    )

    if port_cumul > bench_cumul:
        if port_sortino < bench_sortino:
            sentence += "포트폴리오의 전체 수익률은 벤치마크 보다 좋으나, 안타깝게도 해당 포트폴리오는 벤치마크 보다 위험에 대한 보상이 더 작다고 할 수 있습니다.\n\n"
        else:
            sentence += (
                "포트폴리오의 전체 수익률도 벤치마크 보다 좋고, 또한 벤치마크 보다 위험에 대한 보상이 더 크다고 할 수 있습니다.\n\n"
            )
    else:
        if port_sortino < bench_sortino:
            sentence += "포트폴리오의 전체 수익률도 벤치마크 보다 좋지 않은데, 위험에 대한 보상 마저도 더 적습니다.\n\n"
        else:
            sentence += "전체 수익률은 벤치마크 수치 보다 낮지만, 해당 포트폴리오는 벤치마크 보다 위험에 대한 보상이 더 크다고 할 수 있습니다.\n\n"

    ldd_days = stats["dd"][0]
    ldd_end = stats["dd"][1]
    strategy_recover = stats["recover"][0]
    benchmark_recover = stats["recover"][1]
    sentence += "만약 이 포트폴리오를 이용하여 과거에 투자를 하셨다면 최대 {}%의 수익률 손실을 감내해야 했을 것입니다.\n".format(
        stats["md"][0]
    )
    if ldd_end == today:
        sentence += "게다가 한번 찍은 고점을 다시 회복하는데 최대 {}일이 걸렸고, 이는 현재진행형 입니다.\n".format(
            ldd_days
        )
    else:
        sentence += "게다가 한번 찍은 고점을 다시 회복하는데 최대 {}일이 걸렸던 적이 있습니다.\n".format(ldd_days)

    sentence += "평균적으로는 수익률에 손실이 났을 때, 다시 회복하는데 포트폴리오가 벤치마크 보다 "
    if strategy_recover > benchmark_recover:
        sentence += "빠르게 회복합니다.\n\n"
    else:
        sentence += "느리게 회복합니다.\n\n"

    return sentence
