import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import random
import pandas as pd

from freqtrade.constants import Config
from freqtrade.configuration import TimeRange
from freqtrade.data.btanalysis import (analyze_trade_parallelism,# calculate_max_drawdown, combine_dataframes_with_mean,create_cum_profit,
                                        extract_trades_of_period, load_trades)
from freqtrade.data.converter import trim_dataframe
from freqtrade.data.dataprovider import DataProvider
from freqtrade.data.history import get_timerange, load_data
from freqtrade.data.metrics import (
    calculate_max_drawdown,
    calculate_underwater,
    combine_dataframes_with_mean,
    create_cum_profit,
)
from freqtrade.enums import CandleType
from freqtrade.exceptions import OperationalException
from freqtrade.exchange import timeframe_to_prev_date, timeframe_to_seconds
from freqtrade.misc import pair_to_filename
from freqtrade.plugins.pairlist.pairlist_helpers import expand_pairlist
from freqtrade.resolvers import ExchangeResolver, StrategyResolver
from freqtrade.strategy import IStrategy
from freqtrade.strategy.strategy_wrapper import strategy_safe_wrapper
from freqtrade.util import get_dry_run_wallet


## List of available main plot render commands

plot_indicators = ["volatility",
                   "volatility-above","uptrend","uptrend-above","uptrendsmall","uptrendsmall-above","BULL"]

default_indicators1 = ['main', 'volatility', 'sma50', 'sma200', 'sma400', 'sma10k']

default_indicators2 = ["ppo5"]

default_indicators3 = ["rsi"]

logger = logging.getLogger(__name__)


try:
    import plotly.graph_objects as go
    from plotly.offline import plot
    from plotly.subplots import make_subplots
    import plotly.express as px
except ImportError:
    logger.exception("Module plotly not found \n Please install using `pip3 install plotly`")
    exit(1)


def init_plotscript(config, markets: list, startup_candles: int = 0):
    """
    Initialize objects needed for plotting
    :return: Dict with candle (OHLCV) data, trades and pairs
    """

    if "pairs" in config:
        pairs = expand_pairlist(config["pairs"], markets)
    else:
        pairs = expand_pairlist(config["exchange"]["pair_whitelist"], markets)

    # Set timerange to use
    timerange = TimeRange.parse_timerange(config.get("timerange"))

    data = load_data(
        datadir=config.get("datadir"),
        pairs=pairs,
        timeframe=config["timeframe"],
        timerange=timerange,
        startup_candles=startup_candles,
        data_format=config["dataformat_ohlcv"],
        candle_type=config.get("candle_type_def", CandleType.SPOT),
    )

    if startup_candles and data:
        min_date, max_date = get_timerange(data)
        logger.info(f"Loading data from {min_date} to {max_date}")
        timerange.adjust_start_if_necessary(
            timeframe_to_seconds(config["timeframe"]), startup_candles, min_date
        )

    no_trades = False
    filename = config.get('exportfilename')
    if config.get('no_trades', False):
        no_trades = True
    elif config["trade_source"] == "file":
        if not filename.is_dir() and not filename.is_file():
            logger.warning("Backtest file is missing skipping trades.")
            no_trades = True
    try:
        trades = load_trades(
            config["trade_source"],
            db_url=config.get("db_url"),
            exportfilename=filename,
            no_trades=no_trades,
            strategy=config.get("strategy"),
        )
    except ValueError as e:
        raise OperationalException(e) from e
    if not trades.empty:
        trades = trim_dataframe(trades, timerange, df_date_col="open_date")

    return {
        "ohlcv": data,
        "trades": trades,
        "pairs": pairs,
        "timerange": timerange,
    }


def add_indicators(fig, row, indicators: dict[str, dict], data: pd.DataFrame, solo_fade_mask=None) -> make_subplots:
    """
    Generate all the indicators selected by the user for a specific row, based on the configuration
    :param fig: Plot figure to append to
    :param row: row number for this plot
    :param indicators: Dict of Indicators with configuration options.
                       Dict key must correspond to dataframe column.
    :param data: candlestick DataFrame
    :param solo_fade_mask: Optional boolean Series - True where solo trend is active
    """
    plot_kinds = {
        "scatter": go.Scatter,
        "bar": go.Bar,
    }
    for indicator, conf in indicators.items():
        logger.debug(f"indicator {indicator} with config {conf}")

        ##DRAWS THE NEW TREND INDICATORS
        if(indicator in plot_indicators):
            fig = plot_trend(fig, data, label=indicator, solo_fade_mask=solo_fade_mask)

        elif indicator in data:
            plot_type = conf.get("type", "scatter")
            color = conf.get("color")
            
            # If solo_fade_mask is provided, plot continuous faded line then overlay active portions
            if solo_fade_mask is not None and plot_type == "scatter":
                # Convert color to rgba with 0.25 opacity for faded line
                faded_color = 'rgba(128, 128, 128, 0.25)'
                if color:
                    if color.startswith('#') and len(color) == 7:
                        r = int(color[1:3], 16)
                        g = int(color[3:5], 16)
                        b = int(color[5:7], 16)
                        faded_color = f'rgba({r}, {g}, {b}, 0.25)'
                    elif color.startswith('rgba'):
                        faded_color = color.replace('1)', '0.25)').replace('0.8)', '0.25)').replace('0.5)', '0.25)')
                
                # First: Plot the FULL continuous line at faded opacity (so line stays connected)
                kwargs_faded = {'x': data['date'],
                          'y': data[indicator].values,
                          'name': indicator + ' (bg)',
                          'showlegend': False,
                          'mode': 'lines',
                          'line': {'color': faded_color},
                          'hoverinfo': 'skip'
                          }
                trace_faded = go.Scatter(**kwargs_faded)
                fig.add_trace(trace_faded, row, 1)
                
                # Second: Overlay the active portions at full opacity
                # Use None to create gaps in the line where inactive
                y_values = data[indicator].copy()
                y_values_masked = y_values.where(solo_fade_mask, other=None)
                
                kwargs_active = {'x': data['date'],
                          'y': y_values_masked,
                          'name': indicator,
                          'mode': 'lines',
                          'connectgaps': False
                          }
                if color:
                    kwargs_active.update({"line": {"color": color}})
                kwargs_active.update(conf.get("plotly", {}))
                trace_active = go.Scatter(**kwargs_active)
                fig.add_trace(trace_active, row, 1)
            else:
                # Original behavior - single trace
                kwargs = {'x': data['date'],
                          'y': data[indicator].values,
                          'name': indicator
                          }

                if plot_type == "bar":
                    kwargs.update(
                        {
                            "marker_color": color or "DarkSlateGrey",
                            "marker_line_color": color or "DarkSlateGrey",
                        }
                    )
                else:
                    if color:
                        kwargs.update({"line": {"color": color}})
                    kwargs["mode"] = "lines"
                    if plot_type != "scatter":
                        logger.warning(
                            f"Indicator {indicator} has unknown plot trace kind {plot_type}"
                            f', assuming "scatter".'
                        )

                kwargs.update(conf.get("plotly", {}))
                trace = plot_kinds[plot_type](**kwargs)
                fig.add_trace(trace, row, 1)
        else:
            if(not indicator.startswith('solo') and not indicator == 'main'):
                logger.info(
                    'Indicator "%s" ignored. Reason: This indicator is not found '
                    'in your strategy.',
                    indicator
                )

    return fig


def add_profit(fig, row, data: pd.DataFrame, column: str, name: str) -> make_subplots:
    """
    Add profit-plot
    :param fig: Plot figure to append to
    :param row: row number for this plot
    :param data: candlestick DataFrame
    :param column: Column to use for plot
    :param name: Name to use
    :return: fig with added profit plot
    """
    profit = go.Scatter(
        x=data.index,
        y=data[column],
        name=name,
    )
    fig.add_trace(profit, row, 1)

    return fig


def add_max_drawdown(
    fig, row, trades: pd.DataFrame, df_comb: pd.DataFrame, timeframe: str, starting_balance: float
) -> make_subplots:
    """
    Add scatter points indicating max drawdown
    """
    try:
        drawdown = calculate_max_drawdown(trades, starting_balance=starting_balance)

        drawdown = go.Scatter(
            x=[drawdown.high_date, drawdown.low_date],
            y=[
                df_comb.loc[timeframe_to_prev_date(timeframe, drawdown.high_date), "cum_profit"],
                df_comb.loc[timeframe_to_prev_date(timeframe, drawdown.low_date), "cum_profit"],
            ],
            mode="markers",
            name=f"Max drawdown {drawdown.relative_account_drawdown:.2%}",
            text=f"Max drawdown {drawdown.relative_account_drawdown:.2%}",
            marker=dict(symbol="square-open", size=9, line=dict(width=2), color="green"),
        )
        fig.add_trace(drawdown, row, 1)
    except ValueError:
        logger.warning("No trades found - not plotting max drawdown.")
    return fig


def add_underwater(fig, row, trades: pd.DataFrame, starting_balance: float) -> make_subplots:
    """
    Add underwater plots
    """
    try:
        underwater = calculate_underwater(
            trades, value_col="profit_abs", starting_balance=starting_balance
        )

        underwater_plot = go.Scatter(
            x=underwater["date"],
            y=underwater["drawdown"],
            name="Underwater Plot",
            fill="tozeroy",
            fillcolor="#cc362b",
            line={"color": "#cc362b"},
        )

        underwater_plot_relative = go.Scatter(
            x=underwater["date"],
            y=(-underwater["drawdown_relative"]),
            name="Underwater Plot (%)",
            fill="tozeroy",
            fillcolor="green",
            line={"color": "green"},
        )

        fig.add_trace(underwater_plot, row, 1)
        fig.add_trace(underwater_plot_relative, row + 1, 1)
    except ValueError:
        logger.warning("No trades found - not plotting underwater plot")
    return fig


def add_parallelism(fig, row, trades: pd.DataFrame, timeframe: str) -> make_subplots:
    """
    Add Chart showing trade parallelism
    """
    try:
        result = analyze_trade_parallelism(trades, timeframe)

        drawdown = go.Scatter(
            x=result.index,
            y=result["open_trades"],
            name="Parallel trades",
            fill="tozeroy",
            fillcolor="#242222",
            line={"color": "#242222"},
        )
        fig.add_trace(drawdown, row, 1)
    except ValueError:
        logger.warning("No trades found - not plotting Parallelism.")
    return fig


def plot_trades(fig, trades: pd.DataFrame) -> make_subplots:
    """
    Add trades to "fig"
    """
    # Trades can be empty
    if trades is not None and len(trades) > 0:
        # Create description for exit summarizing the trade
        trades["desc"] = trades.apply(
            lambda row: f"{row['profit_ratio']:.2%}, "
            + (f"{row['enter_tag']}, " if row["enter_tag"] is not None else "")
            + f"{row['exit_reason']}, "
            + f"{row['trade_duration']} min",
            axis=1,
        )
        trade_entries = go.Scatter(
            x=trades["open_date"],
            y=trades["open_rate"],
            mode="markers",
            name="Trade entry",
            text=trades["desc"],
            marker=dict(
                symbol='circle-open',
                size=13,
                line=dict(width=2),
                color='cyan'

            )
        )

        trade_exits = go.Scatter(
            x=trades.loc[trades['profit_ratio'] > 0, "close_date"],
            y=trades.loc[trades['profit_ratio'] > 0, "close_rate"],
            text=trades.loc[trades['profit_ratio'] > 0, "desc"],
            mode='markers',
            name='Exit - Profit',
            marker=dict(
                symbol='square-open',
                size=13,
                line=dict(width=2),
                color='green'
            )
        )
        trade_exits_loss = go.Scatter(
            x=trades.loc[trades['profit_ratio'] <= 0, "close_date"],
            y=trades.loc[trades['profit_ratio'] <= 0, "close_rate"],
            text=trades.loc[trades['profit_ratio'] <= 0, "desc"],
            mode='markers',
            name='Exit - Loss',
            marker=dict(
                symbol='square-open',
                size=13,
                line=dict(width=2),
                color='red'
            )
        )
        fig.add_trace(trade_entries, 1, 1)
        fig.add_trace(trade_exits, 1, 1)
        fig.add_trace(trade_exits_loss, 1, 1)
    else:
        logger.warning("No trades found.")
    return fig


def create_plotconfig(indicators1: List[str], indicators2: List[str], indicators3: List[str],
                      plot_config: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Combines indicators 1 and indicators 2 into plot_config if necessary
    :param indicators1: List containing Main plot indicators
    :param indicators2: List containing Sub plot indicators
    :param plot_config: Dict of Dicts containing advanced plot configuration
    :return: plot_config - eventually with indicators 1 and 2
    """

    if plot_config:
        if indicators1:
            plot_config["main_plot"] = {ind: {} for ind in indicators1}
        if indicators2:
            plot_config['subplots'] = {'Indicator 2': {ind: {} for ind in indicators2}}
        if indicators3:
            plot_config['subplots']["Indicator 3"] = {ind: {} for ind in indicators3}

    if not plot_config:
        # If no indicators and no plot-config given, use defaults.
        if not indicators1:
            indicators1 = default_indicators1
        if not indicators2:
            indicators2 = default_indicators2
        if not indicators3:
            indicators3 = default_indicators3

        # Create subplot configuration if plot_config is not available.
        plot_config = {
            'main_plot': {ind: {} for ind in indicators1},
            'subplots': {'Indicator 2': {ind: {} for ind in indicators2}}
        }
        if(indicators3):
            plot_config['subplots']["Indicator 3"] = {ind: {} for ind in indicators3}

    if 'main_plot' not in plot_config:
        plot_config['main_plot'] = {}

    if 'subplots' not in plot_config:
        plot_config['subplots'] = {}


    return plot_config


def plot_area(
    fig,
    row: int,
    data: pd.DataFrame,
    indicator_a: str,
    indicator_b: str,
    label: str = "",
    fill_color: str = "rgba(0,176,246,0.2)",
) -> make_subplots:
    """Creates a plot for the area between two traces and adds it to fig.
    :param fig: Plot figure to append to
    :param row: row number for this plot
    :param data: candlestick DataFrame
    :param indicator_a: indicator name as populated in strategy
    :param indicator_b: indicator name as populated in strategy
    :param label: label for the filled area
    :param fill_color: color to be used for the filled area
    :return: fig with added  filled_traces plot
    """

    data = data.copy()

    if( label=="main"):


        main_trend_color_hex = {  5:"rgba(24, 69, 13,0.5)",#"name":"UPPER_DANGER"}
                            3:"rgba(0,128,0, 0.3)",#"name":"LONG_UPTREND"},
                            # 2:"rgba(70, 130, 180,0.35)",#"name":"DOWNTREND_UPSWING"},
                            1:"rgba(255,255,159,0.35)",#"name":"DATA_NOT_LOADED"}, #"rgba(255,255,159,0.1)",
                            0:"rgba(255, 255, 255, 0)",#"name":"NOTREND"}, #"rgba(0,176,246,0.2)",
                            -1:"rgba(233, 150, 122,0.35)",#"name":"SLOW_DOWNTREND"},
                            -2:"rgba(255, 0, 0,0.3)",#"name":"LONG_DOWNTREND"},
                            -3:"rgba(106, 11, 16,0.5)",#"name":"BOTTOM_DANGER"},
                        }
        main_trend_labels = {  "5":"UPPER_DANGER",
                            "3":"LONG_UPTREND",
                            # "2":"DOWNTREND_UPSWING",
                            "1":"DATA_NOT_LOADED",
                            "0":"NOTREND",
                            "-1":"SLOW_DOWNTREND",
                            "-2":"LONG_DOWNTREND",
                            "-3":"BOTTOM_DANGER"

                        }

        main_volatility_hex = {
                    0:"rgba(0, 0, 0, 0)",#"name":"NONE"},
                    1:"rgba(175, 225, 233, 0.25)",#"name":"LOW"},
                    2:"rgba(73, 187, 204, 0.25)",#"name":"MID"},
                    3:"rgba(0, 139, 251, 0.22)",#"name":"HIGH"}
                        }
        main_volatility_labels = {
                    "0":"NONE",
                    "1":"LOW_VOL",
                    "2":"MID_VOL",
                    "3":"HIGH_VOL"
                        }
        line = {'color': 'rgba(255,255,255,0)'}

        for m_trend in data["main_trend"].copy().drop_duplicates():
            if(m_trend != 0):
                newframe = data.copy()

                newframe.loc[( newframe['main_trend'] != m_trend), 'bb_upperband'] = newframe['bb_middleband']
                newframe.loc[( newframe['main_trend'] != m_trend), 'bb_lowerband'] = newframe['bb_middleband']


                main_trend_area_style = main_trend_color_hex[m_trend]
                main_trend_label_style = main_trend_labels[str(m_trend)]


                trace_a = go.Scatter(x=newframe.date, y=newframe[indicator_a],
                                 showlegend=False,
                                 line=line)
                trace_b = go.Scatter(x=newframe.date, y=newframe[indicator_b], name=main_trend_label_style,
                                     fill="tonexty", fillcolor=main_trend_area_style,
                                     line=line)
                fig.add_trace(trace_a, row, 1)
                fig.add_trace(trace_b, row, 1)
            else:
                for vol in range(3):
                    vol+=1
                    newframe = data.copy()

                    newframe.loc[(( newframe['main_trend'] != m_trend | (newframe['volatility'] != vol)&(newframe['volatility'] != 0))), 'bb_upperband'] = newframe['bb_middleband']
                    newframe.loc[(( newframe['main_trend'] != m_trend | (newframe['volatility'] != vol)&(newframe['volatility'] != 0))), 'bb_lowerband'] = newframe['bb_middleband']


                    vol_area_style = main_volatility_hex[vol]
                    vol_area_labels = main_volatility_labels[str(vol)]


                    trace_a = go.Scatter(x=newframe.date, y=newframe[indicator_a],
                                     showlegend=False,
                                     line=line)
                    trace_b = go.Scatter(x=newframe.date, y=newframe[indicator_b], name=vol_area_labels,
                                         fill="tonexty", fillcolor=vol_area_style,
                                         line=line)
                    fig.add_trace(trace_a, row, 1)
                    fig.add_trace(trace_b, row, 1)


    if( label.startswith('solo')):

        solo_parts = label.split("=")[1]
        # Parse optional sub-filter (e.g. "solo=-2&uptrend" -> m_trend=-2, sub_filter="uptrend")
        if "&" in solo_parts:
            m_trend = int(solo_parts.split("&")[0])
            sub_filter = solo_parts.split("&")[1]
        else:
            m_trend = int(solo_parts)
            sub_filter = None


        main_trend_color_hex = {  5:"rgba(24, 69, 13,0.5)",#"name":"UPPER_DANGER"}
                            3:"rgba(0,128,0, 0.3)",#"name":"LONG_UPTREND"},
                            # 2:"rgba(70, 130, 180,0.35)",#"name":"DOWNTREND_UPSWING"},
                            1:"rgba(255,255,159,0.35)",#"name":"DATA_NOT_LOADED"}, #"rgba(255,255,159,0.1)",
                            0:"rgba(255, 255, 255, 0)",#"name":"NOTREND"}, #"rgba(0,176,246,0.2)",
                            -1:"rgba(233, 150, 122,0.35)",#"name":"SLOW_DOWNTREND"},
                            -2:"rgba(255, 0, 0,0.3)",#"name":"LONG_DOWNTREND"},
                            -3:"rgba(106, 11, 16,0.5)",#"name":"BOTTOM_DANGER"},
                        }
        main_trend_labels = {  "5":"UPPER_DANGER",
                            "3":"LONG_UPTREND",
                            # "2":"DOWNTREND_UPSWING",
                            "1":"DATA_NOT_LOADED",
                            "0":"NOTREND",
                            "-1":"SLOW_DOWNTREND",
                            "-2":"LONG_DOWNTREND",
                            "-3":"BOTTOM_DANGER"

                        }

        main_volatility_hex = {
                    0:"rgba(0, 0, 0, 0)",#"name":"NONE"},
                    1:"rgba(175, 225, 233, 0.25)",#"name":"LOW"},
                    2:"rgba(73, 187, 204, 0.25)",#"name":"MID"},
                    3:"rgba(0, 139, 251, 0.22)",#"name":"HIGH"}
                        }
        main_volatility_labels = {
                    "0":"NONE",
                    "1":"LOW_VOL",
                    "2":"MID_VOL",
                    "3":"HIGH_VOL"
                        }
        line = {'color': 'rgba(255,255,255,0)'}

        # Helper to build the sub-filter mask (True = keep, False = hide)
        def _sub_filter_mask(frame, sf):
            if sf == "uptrend":
                return frame['uptrend'] != 0
            elif sf == "downtrend":
                return frame['uptrend'] == 0
            elif sf == "BULL":
                return frame['BULL'] == 1
            elif sf == "BEAR":
                return frame['BULL'] == -1
            return True  # no filter


        if(m_trend != 0):


            newframe = data.copy()

            # Base condition: main_trend must match
            hide_mask = (newframe['main_trend'] != m_trend)
            # Apply sub-filter overlap condition
            if sub_filter:
                hide_mask = hide_mask | (~_sub_filter_mask(newframe, sub_filter))

            newframe.loc[hide_mask, 'bb_upperband'] = newframe['bb_middleband']
            newframe.loc[hide_mask, 'bb_lowerband'] = newframe['bb_middleband']

            if sub_filter:
                main_trend_area_style = main_trend_color_hex[m_trend]
                main_trend_label_style = main_trend_labels[str(m_trend)] + " + " + sub_filter
            else:
                main_trend_area_style = main_trend_color_hex[m_trend]
                main_trend_label_style = main_trend_labels[str(m_trend)]

            trace_a = go.Scatter(x=newframe.date, y=newframe[indicator_a],
                                 showlegend=False,
                                 line=line)
            trace_b = go.Scatter(x=newframe.date, y=newframe[indicator_b], name=main_trend_label_style,
                                 fill="tonexty", fillcolor=main_trend_area_style,
                                 line=line)
            fig.add_trace(trace_a, row, 1)
            fig.add_trace(trace_b, row, 1)

            # draws danger zone on -1 and -2 BOTH DOWNTRENDS (only when no sub-filter)
            if not sub_filter and ((m_trend == -1) or (m_trend == -2)):
                newframe = data.copy()

                newframe.loc[(newframe['main_trend'] != -3) , 'bb_upperband'] = newframe['bb_middleband']
                newframe.loc[(newframe['main_trend'] != -3) , 'bb_lowerband'] = newframe['bb_middleband']

                main_trend_area_style = main_trend_color_hex[-3]
                main_trend_label_style = main_trend_labels[str(-3)]

                trace_a = go.Scatter(x=newframe.date, y=newframe[indicator_a],
                                     showlegend=False,
                                     line=line)
                trace_b = go.Scatter(x=newframe.date, y=newframe[indicator_b], name=main_trend_label_style,
                                     fill="tonexty", fillcolor=main_trend_area_style,
                                     line=line)
                fig.add_trace(trace_a, row, 1)
                fig.add_trace(trace_b, row, 1)
            # draws upper danger zone on LONG UPTREND (only when no sub-filter)
            if not sub_filter and (m_trend == 3):
                newframe = data.copy()

                newframe.loc[(newframe['main_trend'] != 5) , 'bb_upperband'] = newframe['bb_middleband']
                newframe.loc[(newframe['main_trend'] != 5) , 'bb_lowerband'] = newframe['bb_middleband']

                main_trend_area_style = main_trend_color_hex[5]
                main_trend_label_style = main_trend_labels[str(5)]

                trace_a = go.Scatter(x=newframe.date, y=newframe[indicator_a],
                                     showlegend=False,
                                     line=line)
                trace_b = go.Scatter(x=newframe.date, y=newframe[indicator_b], name=main_trend_label_style,
                                     fill="tonexty", fillcolor=main_trend_area_style,
                                     line=line)
                fig.add_trace(trace_a, row, 1)
                fig.add_trace(trace_b, row, 1)
        else:
            if sub_filter:
                # m_trend == 0 with sub-filter: show Normal areas overlapping with sub-filter
                newframe = data.copy()

                hide_mask = (newframe['main_trend'] != m_trend) | (~_sub_filter_mask(newframe, sub_filter))
                newframe.loc[hide_mask, 'bb_upperband'] = newframe['bb_middleband']
                newframe.loc[hide_mask, 'bb_lowerband'] = newframe['bb_middleband']

                area_style = main_trend_color_hex[m_trend]
                label_style = main_trend_labels[str(m_trend)] + " + " + sub_filter

                trace_a = go.Scatter(x=newframe.date, y=newframe[indicator_a],
                                 showlegend=False,
                                 line=line)
                trace_b = go.Scatter(x=newframe.date, y=newframe[indicator_b], name=label_style,
                                     fill="tonexty", fillcolor=area_style,
                                     line=line)
                fig.add_trace(trace_a, row, 1)
                fig.add_trace(trace_b, row, 1)
            else:
                for vol in range(3):
                    vol+=1
                    newframe = data.copy()

                    newframe.loc[(( newframe['main_trend'] != m_trend | (newframe['volatility'] != vol)&(newframe['volatility'] != 0))), 'bb_upperband'] = newframe['bb_middleband']
                    newframe.loc[(( newframe['main_trend'] != m_trend | (newframe['volatility'] != vol)&(newframe['volatility'] != 0))), 'bb_lowerband'] = newframe['bb_middleband']


                    vol_area_style = main_volatility_hex[vol]
                    vol_area_labels = main_volatility_labels[str(vol)]


                    trace_a = go.Scatter(x=newframe.date, y=newframe[indicator_a],
                                     showlegend=False,
                                     line=line)
                    trace_b = go.Scatter(x=newframe.date, y=newframe[indicator_b], name=vol_area_labels,
                                         fill="tonexty", fillcolor=vol_area_style,
                                         line=line)
                    fig.add_trace(trace_a, row, 1)
                    fig.add_trace(trace_b, row, 1)




    if label=="Bolinger Bands" and indicator_a in data and indicator_b in data:
        # make lines invisible to get the area plotted, only.
        line = {'color': 'rgba(255,255,255,0)'}
        # TODO: Figure out why scattergl causes problems plotly/plotly.js#2284
        trace_a = go.Scatter(x=data.date, y=data[indicator_a],
                             showlegend=False,
                             line=line)
        trace_b = go.Scatter(x=data.date, y=data[indicator_b], name=label,
                             fill="tonexty", fillcolor=fill_color,
                             line=line)
        fig.add_trace(trace_a, row, 1)
        fig.add_trace(trace_b, row, 1)

    return fig


def plot_trend(fig, data: pd.DataFrame, label: str = "", solo_fade_mask=None) -> make_subplots:
    """ Creates a plot for the main/volatility trends provided.
    :param fig: Plot figure to append to
    :param data: candlestick DataFrame
    :param label: label for the trend area
    :param solo_fade_mask: Optional boolean Series - True where solo trend is active
    :return: fig with added  filled_traces plot
    """

    data = data.copy()

    labels = label.split('=')
    label = labels[0]

    display="below"
    if(len(labels)>1):
        display = labels[1]

    ##not used at the moment
    if( label=="main_trend"):
        distance = 18

        main_color_hex = {  "5":"#8FBC8F",#"name":"UPPER_DANGER"}
                            "3":"rgba(0,128,0, 0.8)",#"name":"LONG_UPTREND"},
                            "2":"#4682B4",#"name":"DOWNTREND_UPSWING"},
                              "0": "rgba(255, 255, 255, 0.01)",#"name":"NOTREND"}, #"rgba(0,176,246,0.2)",
                            "-1":"#E9967A",#"name":"SLOW_DOWNTREND"},
                                 "-2":"#FF0000",#"name":"LONG_DOWNTREND"},
                                "-3":"#006400",#"name":"BOTTOM_DANGER"},

            }
        main_volatility_hex = {
                    "1":"rgba(175, 225, 233, 0.5)",#"name":"LOW"},
                    "2":"rgba(73, 187, 204, 0.5)",#"name":"MID"},
                    "3":"rgba(0, 139, 251, 0.5)",#"name":"HIGH"}
                }

        main_volatility_symbols = {
                    "1":"circle-open",#"name":"LOW"},
                    "2":"circle-open-dot",#"name":"MID"},
                    "3":"circle",#"name":"HIGH"}
                }
        main_trend_symbols = {
                            "3":"star-triangle-up",#"name":"LONG_UPTREND"},
                            "-2":"star-triangle-down",#"name":"LONG_DOWNTREND"},
                             "-1":"triangle-down",#"name":"SLOW_DOWNTREND"},
                             "0": "circle",#"name":"NOTREND"}, #"rgba(0,176,246,0.2)",
                            "2":"cross",#"name":"DOWNTREND_UPSWING"},
                            "-3":"x",#"name":"BOTTOM_DANGER"},
                             "5":"x"#"name":"UPPER_DANGER"}
                }


        data['main_trend'] = data['main_trend'].astype(str)
        data['volatility'] = data['volatility'].astype(str)


        #volatility_df = data.copy()
        volatility_df = data[data['main_trend'] == "0"]
        main_trend_df = data[data['main_trend'] != "0"]


        if(display == "above"):
            main_trend_df['sma_main_trend_display'] =(main_trend_df['sma25']+(main_trend_df['sma25']/100*distance))
            volatility_df['sma_main_trend_display'] =(volatility_df['sma25']+(volatility_df['sma25']/100*distance))
        else:
            main_trend_df['sma_main_trend_display'] =(main_trend_df['sma25']-(main_trend_df['sma25']/100*distance))
            volatility_df['sma_main_trend_display'] =(volatility_df['sma25']-(volatility_df['sma25']/100*distance))


        trace_main1 = px.scatter(main_trend_df, x="date", y="sma_main_trend_display",#,
                            # hover_name="main_trend",
                             color_discrete_sequence=px.colors.qualitative.Alphabet,
                             color_discrete_map=main_color_hex,
                             color ="main_trend",
                             symbol ="main_trend",
                             symbol_map =main_trend_symbols
                             # symbol ="main_trend",
                             # height=30,
                             # opacity =0.5,

                          )

        main_trend_df['sma_main_trend_display'] =(main_trend_df['sma_main_trend_display']-(main_trend_df['sma_main_trend_display']/100*1))

        trace_main2 = px.scatter(main_trend_df, x="date", y="sma_main_trend_display",#,
                            # hover_name="main_trend",
                             color_discrete_sequence=px.colors.qualitative.Alphabet,
                             color_discrete_map=main_color_hex,
                             color ="main_trend",
                             symbol ="main_trend",
                             symbol_map =main_trend_symbols

                          )

        trace_mainVOL = px.scatter(volatility_df, x="date", y="sma_main_trend_display",#,
                             #hover_name="volatility",
                             color_discrete_sequence=px.colors.qualitative.Alphabet,
                             color_discrete_map=main_volatility_hex,
                             color ="volatility",
                             symbol ="volatility",
                             symbol_map =main_volatility_symbols
                             # symbol ="main_trend",
                             # height=30,
                             # opacity =0.5,
                          )

        fig.add_traces(
            list(trace_main1.select_traces())
        )
        fig.add_traces(
            list(trace_main2.select_traces())
        )
        fig.add_traces(
            list(trace_mainVOL.select_traces())
        )

    if( label=="volatility"):
        distance = 14

        main_volatility_hex = {
                    "0":"rgba(0, 0, 0, 0)",#"name":"NONE"},
                    "1":"rgba(175, 225, 233, 0.5)",#"name":"LOW"},
                    "2":"rgba(73, 187, 204, 0.5)",#"name":"MID"},
                    "3":"rgba(0, 139, 251, 0.5)",#"name":"HIGH"}
                }
        
        # Faded version for inactive areas
        main_volatility_hex_faded = {
                    "0":"rgba(0, 0, 0, 0)",
                    "1":"rgba(175, 225, 233, 0.06)",
                    "2":"rgba(73, 187, 204, 0.06)",
                    "3":"rgba(0, 139, 251, 0.06)"
                }

        main_volatility_symbols = {
                    "0":"square",#"name":"NONE"},
                    "1":"circle-open",#"name":"LOW"},
                    "2":"circle-open-dot",#"name":"MID"},
                    "3":"circle",#"name":"HIGH"}
                }


        data['volatility'] = data['volatility'].astype(str)

        display="above"  ##SET VOLATILITY TO BE ABOVE BY DEFAULT

        if(display == "above"):
            data['sma_volatility_display'] =(data['sma25']+(data['sma25']/100*distance))
        else:
            data['sma_volatility_display'] =(data['sma25']-(data['sma25']/100*distance))

        # If solo_fade_mask is provided, split into active/faded
        if solo_fade_mask is not None:
            data_active = data[solo_fade_mask]
            data_faded = data[~solo_fade_mask]
            
            # Faded traces first
            if len(data_faded) > 0:
                trace_faded = px.scatter(data_faded, x="date", y="sma_volatility_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=main_volatility_hex_faded,
                                 color="volatility",
                                 symbol="volatility",
                                 symbol_map=main_volatility_symbols
                              )
                for trace in trace_faded.select_traces():
                    trace.showlegend = False
                fig.add_traces(list(trace_faded.select_traces()))
            
            # Active traces on top
            if len(data_active) > 0:
                trace_active = px.scatter(data_active, x="date", y="sma_volatility_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=main_volatility_hex,
                                 color="volatility",
                                 symbol="volatility",
                                 symbol_map=main_volatility_symbols
                              )
                fig.add_traces(list(trace_active.select_traces()))
        else:
            trace_upper1 = px.scatter(data, x="date", y="sma_volatility_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=main_volatility_hex,
                                 color ="volatility",
                                 symbol ="volatility",
                                 symbol_map =main_volatility_symbols
                              )
            fig.add_traces(list(trace_upper1.select_traces()))

    if(label == "uptrend"):
        distance = 16

        uptrend_color_hex = {
                        "4.0":"rgba(0,128,0,0.20)",
                        "3.0":"rgba(50,205,50,0.29)",
                         "2.0":"rgba(124,252,0,0.29)",
                        "1.0":"rgba(152,251,152,0.35)",
                      "0.0": "rgba(0, 0, 0, 0.01)",
                        "-0.0": "rgba(0, 0, 0, 0.01)",
                         "-1.0":"rgba(255,160,122,0.35)",
                         "-2.0":"rgba(240,128,128,0.29)",
                         "-3.0":"rgba(220,20,60,0.29)",
                        "-4.0":"rgba(255,0,0,0.20)"
        }
        
        # Faded version for inactive areas
        uptrend_color_hex_faded = {
                        "4.0":"rgba(0,128,0,0.03)",
                        "3.0":"rgba(50,205,50,0.04)",
                         "2.0":"rgba(124,252,0,0.04)",
                        "1.0":"rgba(152,251,152,0.05)",
                      "0.0": "rgba(0, 0, 0, 0)",
                        "-0.0": "rgba(0, 0, 0, 0)",
                         "-1.0":"rgba(255,160,122,0.05)",
                         "-2.0":"rgba(240,128,128,0.04)",
                         "-3.0":"rgba(220,20,60,0.04)",
                        "-4.0":"rgba(255,0,0,0.03)"
        }

        uptrend_symbols = { "4.0":"x",
                            "3.0":"star-triangle-up",
                             "2.0":"triangle-up",
                            "1.0":"triangle-up",
                             "0.0": "triangle-down",
                            "-0.0": "triangle-down",
                             "-1.0":"triangle-down",
                            "-2.0":"triangle-down",
                            "-3.0":"star-triangle-down",
                            "-4.0":"x"
                }


        data['uptrend'] = data['uptrend'].astype(str)

        uptrend_df = data[(data['uptrend'] != "0")&(data['uptrend'] != "nan")]

        if(display == "above"):
            uptrend_df['sma_uptrend_display'] =(uptrend_df['sma25']+(uptrend_df['sma25']/100*distance))
        else:
            uptrend_df['sma_uptrend_display'] =(uptrend_df['sma25']-(uptrend_df['sma25']/100*distance))

        # If solo_fade_mask is provided, split into active/faded
        if solo_fade_mask is not None:
            # Need to align mask with uptrend_df indices
            uptrend_active_mask = solo_fade_mask.loc[uptrend_df.index]
            data_active = uptrend_df[uptrend_active_mask]
            data_faded = uptrend_df[~uptrend_active_mask]
            
            # Faded traces first
            if len(data_faded) > 0:
                trace_faded = px.scatter(data_faded, x="date", y="sma_uptrend_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=uptrend_color_hex_faded,
                                 color="uptrend",
                                 symbol="uptrend",
                                 symbol_map=uptrend_symbols
                              )
                for trace in trace_faded.select_traces():
                    trace.showlegend = False
                fig.add_traces(list(trace_faded.select_traces()))
            
            # Active traces on top
            if len(data_active) > 0:
                trace_active = px.scatter(data_active, x="date", y="sma_uptrend_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=uptrend_color_hex,
                                 color="uptrend",
                                 symbol="uptrend",
                                 symbol_map=uptrend_symbols
                              )
                fig.add_traces(list(trace_active.select_traces()))
            print("Drawing uptrend line on chart...")
        else:
            trace_uptrend1 = px.scatter(uptrend_df, x="date", y="sma_uptrend_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=uptrend_color_hex,
                                 color ="uptrend",
                                 symbol ="uptrend",
                                 symbol_map =uptrend_symbols
                              )
            print("Drawing uptrend line on chart...")
            fig.add_traces(list(trace_uptrend1.select_traces()))

    if(label == "BULL"):
        distance = 20

        bull_bear_color_hex = {
                        "1":"rgba(31,233,255,0.45)",
                      "0": "rgba(0, 0, 0, 0)",
                         "-1":"rgba(229,102,255,0.45)",
        }
        
        # Faded version for inactive areas
        bull_bear_color_hex_faded = {
                        "1":"rgba(31,233,255,0.05)",
                      "0": "rgba(0, 0, 0, 0)",
                         "-1":"rgba(229,102,255,0.05)",
        }

        bull_bear_symbols = {
                            "1":"triangle-up",
                             "0": "triangle-down",
                             "-1":"triangle-down",
                }


        data['BULL'] = data['BULL'].astype(str)

        bull_bear_df = data[(data['BULL'] != "0")&(data['BULL'] != "nan")]

        display="below"

        if(display == "above"):
            bull_bear_df['sma_bull_bear_display'] =(bull_bear_df['sma25']+(bull_bear_df['sma25']/100*distance))
        else:
            bull_bear_df['sma_bull_bear_display'] =(bull_bear_df['sma25']-(bull_bear_df['sma25']/100*distance))

        # If solo_fade_mask is provided, split into active/faded
        if solo_fade_mask is not None:
            # Need to align mask with bull_bear_df indices
            bull_active_mask = solo_fade_mask.loc[bull_bear_df.index]
            data_active = bull_bear_df[bull_active_mask]
            data_faded = bull_bear_df[~bull_active_mask]
            
            # Faded traces first
            if len(data_faded) > 0:
                trace_faded = px.scatter(data_faded, x="date", y="sma_bull_bear_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=bull_bear_color_hex_faded,
                                 color="BULL",
                                 symbol="BULL",
                                 symbol_map=bull_bear_symbols
                              )
                for trace in trace_faded.select_traces():
                    trace.showlegend = False
                fig.add_traces(list(trace_faded.select_traces()))
            
            # Active traces on top
            if len(data_active) > 0:
                trace_active = px.scatter(data_active, x="date", y="sma_bull_bear_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=bull_bear_color_hex,
                                 color="BULL",
                                 symbol="BULL",
                                 symbol_map=bull_bear_symbols
                              )
                fig.add_traces(list(trace_active.select_traces()))
            print("Drawing bull_bear line on chart...")
        else:
            trace_bull_bear1 = px.scatter(bull_bear_df, x="date", y="sma_bull_bear_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=bull_bear_color_hex,
                                 color ="BULL",
                                 symbol ="BULL",
                                 symbol_map =bull_bear_symbols
                              )
            print("Drawing bull_bear line on chart...")
            fig.add_traces(list(trace_bull_bear1.select_traces()))

                #Main trend

        # 3 - LONG/SHARP UPTREND
        # 2 - DOWNTREND UPSWING
        # 1 - SMALL UPSWING
        # 0 - NORMAL
        #-1 - SLOW DOWNTREND
        #-2 - LONG/SHARP DOWNTREND
        #-3 - DANGER ZONE


        # SEC
        # 5 - UPPER DANGER ZONE
        # 4 - HUGE FALL TURNAROUND
        # 3 - LONG/SHARP UPTREND
        # 2 - DOWNTREND UPSWING
        #-2 - LONG/SHARP DOWNTREND
        #-3 - DANGER ZONE

    if(label == "uptrendsmall"):
        distance = 13

        uptrendsmall_color_hex = {
                        "3.0":"rgba(50,205,50,0.29)",
                         "2.0":"rgba(124,252,0,0.29)",
                        "1.0":"rgba(152,251,152,0.35)",
                      "0.0": "rgba(0, 0, 0, 0.01)",
                        "-0.0": "rgba(0, 0, 0, 0.01)",
                         "-1.0":"rgba(255,160,122,0.35)",
                         "-2.0":"rgba(240,128,128,0.29)",
                         "-3.0":"rgba(220,20,60,0.29)"
        }
        
        # Faded version for inactive areas
        uptrendsmall_color_hex_faded = {
                        "3.0":"rgba(50,205,50,0.10)",
                         "2.0":"rgba(124,252,0,0.10)",
                        "1.0":"rgba(152,251,152,0.12)",
                      "0.0": "rgba(0, 0, 0, 0)",
                        "-0.0": "rgba(0, 0, 0, 0)",
                         "-1.0":"rgba(255,160,122,0.12)",
                         "-2.0":"rgba(240,128,128,0.10)",
                         "-3.0":"rgba(220,20,60,0.10)"
        }

        uptrendsmall_symbols = {
                            "3.0":"star-triangle-up",
                             "2.0":"triangle-up",
                            "1.0":"triangle-up",
                             "0.0": "triangle-down",
                            "-0.0": "triangle-down",
                             "-1.0":"triangle-down",
                            "-2.0":"triangle-down",
                            "-3.0":"star-triangle-down"
                }


        data['uptrendsmall'] = data['uptrendsmall'].astype(str)

        uptrendsmall_df = data[(data['uptrendsmall'] != "0")&(data['uptrendsmall'] != "nan")]

        if(display == "above"):
            uptrendsmall_df['sma_uptrendsmall_display'] =(uptrendsmall_df['sma25']+(uptrendsmall_df['sma25']/100*distance))
        else:
            uptrendsmall_df['sma_uptrendsmall_display'] =(uptrendsmall_df['sma25']-(uptrendsmall_df['sma25']/100*distance))

        # If solo_fade_mask is provided, split into active/faded
        if solo_fade_mask is not None:
            # Need to align mask with uptrendsmall_df indices
            uptrendsmall_active_mask = solo_fade_mask.loc[uptrendsmall_df.index]
            data_active = uptrendsmall_df[uptrendsmall_active_mask]
            data_faded = uptrendsmall_df[~uptrendsmall_active_mask]
            
            # Faded traces first
            if len(data_faded) > 0:
                trace_faded = px.scatter(data_faded, x="date", y="sma_uptrendsmall_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=uptrendsmall_color_hex_faded,
                                 color="uptrendsmall",
                                 symbol="uptrendsmall",
                                 symbol_map=uptrendsmall_symbols
                              )
                for trace in trace_faded.select_traces():
                    trace.showlegend = False
                fig.add_traces(list(trace_faded.select_traces()))
            
            # Active traces on top
            if len(data_active) > 0:
                trace_active = px.scatter(data_active, x="date", y="sma_uptrendsmall_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=uptrendsmall_color_hex,
                                 color="uptrendsmall",
                                 symbol="uptrendsmall",
                                 symbol_map=uptrendsmall_symbols
                              )
                fig.add_traces(list(trace_active.select_traces()))
            print("Drawing uptrendsmall line on chart "+str(display)+"...")
        else:
            trace_uptrendsmall1 = px.scatter(uptrendsmall_df, x="date", y="sma_uptrendsmall_display",
                                 color_discrete_sequence=px.colors.qualitative.Alphabet,
                                 color_discrete_map=uptrendsmall_color_hex,
                                 color ="uptrendsmall",
                                 symbol ="uptrendsmall",
                                 symbol_map =uptrendsmall_symbols
                              )
            print("Drawing uptrendsmall line on chart "+str(display)+"...")
            fig.add_traces(list(trace_uptrendsmall1.select_traces()))

                #Main trend

        # 3 - LONG/SHARP UPTREND
        # 2 - DOWNTREND UPSWING
        # 1 - SMALL UPSWING
        # 0 - NORMAL
        #-1 - SLOW DOWNTREND
        #-2 - LONG/SHARP DOWNTREND
        #-3 - DANGER ZONE


        # SEC
        # 5 - UPPER DANGER ZONE
        # 4 - HUGE FALL TURNAROUND
        # 3 - LONG/SHARP UPTREND
        # 2 - DOWNTREND UPSWING
        #-2 - LONG/SHARP DOWNTREND
        #-3 - DANGER ZONE


    return fig


def add_areas(fig, row: int, data: pd.DataFrame, indicators) -> make_subplots:
    """Adds all area plots (specified in plot_config) to fig.
    :param fig: Plot figure to append to
    :param row: row number for this plot
    :param data: candlestick DataFrame
    :param indicators: dict with indicators. ie.: plot_config['main_plot'] or
                            plot_config['subplots'][subplot_label]
    :return: fig with added  filled_traces plot
    """
    for indicator, ind_conf in indicators.items():
        if "fill_to" in ind_conf:
            indicator_b = ind_conf["fill_to"]
            if indicator in data and indicator_b in data:
                label = ind_conf.get("fill_label", f"{indicator}<>{indicator_b}")
                fill_color = ind_conf.get("fill_color", "rgba(0,176,246,0.2)")
                fig = plot_area(
                    fig, row, data, indicator, indicator_b, label=label, fill_color=fill_color
                )
            elif indicator not in data:
                logger.info(
                    'Indicator "%s" ignored. Reason: This indicator is not found in your strategy.',
                    indicator,
                )
            elif indicator_b not in data:
                logger.info(
                    'fill_to: "%s" ignored. Reason: This indicator is not in your strategy.',
                    indicator_b,
                )
    return fig


def create_scatter(data, column_name, color, direction) -> go.Scatter | None:
    if column_name in data.columns:
        df_short = data[data[column_name] == 1]
        if len(df_short) > 0:
            shorts = go.Scatter(
                x=df_short.date,
                y=df_short.close,
                mode="markers",
                name=column_name,
                marker=dict(
                    symbol=f"triangle-{direction}-dot",
                    size=9,
                    line=dict(width=1),
                    color=color,
                ),
            )
            return shorts
        else:
            logger.warning(f"No {column_name}-signals found.")

    return None


def generate_candlestick_graph(pair: str, data: pd.DataFrame, trades: pd.DataFrame = None, *,
                               indicators1: List[str] = [],
                               indicators2: List[str] = [],
                               indicators3: List[str] = [],
                               plot_config: Dict[str, Dict] = {},
                               ) -> go.Figure:
    """
    Generate the graph from the data generated by Backtesting or from DB
    Volume will always be plotted in row2, so Row 1 and 3 are to our disposal for custom indicators
    :param pair: Pair to Display on the graph
    :param data: OHLCV DataFrame containing indicators and entry/exit signals
    :param trades: All trades created
    :param indicators1: List containing Main plot indicators
    :param indicators2: List containing Sub plot indicators
    :param plot_config: Dict of Dicts containing advanced plot configuration
    :return: Plotly figure
    """
    plot_config = create_plotconfig(
        indicators1 or [],
        indicators2 or [],
        indicators3 or [],
        plot_config or {},
    )
    rows = 1 + len(plot_config["subplots"])
    row_widths = [1 for _ in plot_config["subplots"]]
    # Define the graph
    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        row_width=[1] + [1, 4],
        vertical_spacing=0.0001,
    )
    fig["layout"].update(title=pair)
    fig["layout"]["yaxis1"].update(title="Price")
    fig["layout"]["yaxis2"].update(title="Volume")
    for i, name in enumerate(plot_config["subplots"]):
        fig["layout"][f"yaxis{2 + i}"].update(title=name)
    fig["layout"]["xaxis"]["rangeslider"].update(visible=False)
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])

    # Check if a solo trend is selected and create fade mask
    solo_fade_mask = None
    for ind in indicators1:
        if ind.startswith('solo='):
            solo_parts = ind.split("=")[1]
            if "&" in solo_parts:
                m_trend = int(solo_parts.split("&")[0])
                sub_filter = solo_parts.split("&")[1]
            else:
                m_trend = int(solo_parts)
                sub_filter = None
            
            # Build the active mask (True = trend is active, False = inactive/faded)
            if 'main_trend' in data.columns:
                solo_fade_mask = (data['main_trend'] == m_trend)
                if sub_filter:
                    if sub_filter == "uptrend" and 'uptrend' in data.columns:
                        solo_fade_mask = solo_fade_mask & (data['uptrend'] != 0)
                    elif sub_filter == "downtrend" and 'uptrend' in data.columns:
                        solo_fade_mask = solo_fade_mask & (data['uptrend'] == 0)
                    elif sub_filter == "BULL" and 'BULL' in data.columns:
                        solo_fade_mask = solo_fade_mask & (data['BULL'] == 1)
                    elif sub_filter == "BEAR" and 'BULL' in data.columns:
                        solo_fade_mask = solo_fade_mask & (data['BULL'] == -1)
            break

    # Common information - Candlesticks
    if solo_fade_mask is not None:
        # Split data into active and inactive parts
        data_active = data[solo_fade_mask].copy()
        data_inactive = data[~solo_fade_mask].copy()
        
        # Active candles - full opacity
        if len(data_active) > 0:
            candles_active = go.Candlestick(
                x=data_active.date, open=data_active.open, high=data_active.high, 
                low=data_active.low, close=data_active.close, name="Price",
                increasing_line_color='#26a69a', decreasing_line_color='#ef5350',
                increasing_fillcolor='#26a69a', decreasing_fillcolor='#ef5350',
            )
            fig.add_trace(candles_active, 1, 1)
        
        # Inactive candles - faded (0.5 opacity)
        if len(data_inactive) > 0:
            candles_inactive = go.Candlestick(
                x=data_inactive.date, open=data_inactive.open, high=data_inactive.high,
                low=data_inactive.low, close=data_inactive.close, name="Price (faded)",
                showlegend=False,
                increasing_line_color='rgba(38, 166, 154, 0.3)', decreasing_line_color='rgba(239, 83, 80, 0.3)',
                increasing_fillcolor='rgba(38, 166, 154, 0.3)', decreasing_fillcolor='rgba(239, 83, 80, 0.3)',
            )
            fig.add_trace(candles_inactive, 1, 1)
    else:
        candles = go.Candlestick(
            x=data.date, open=data.open, high=data.high, low=data.low, close=data.close, name="Price"
        )
        fig.add_trace(candles, 1, 1)
    
    # Enable for shorter code or if futures don't work
    # longs = create_scatter(data, "enter_long", "green", "up")
    # exit_longs = create_scatter(data, "exit_long", "red", "down")
    # shorts = create_scatter(data, "enter_short", "blue", "down")
    # exit_shorts = create_scatter(data, "exit_short", "violet", "up")

    buy_colours_hex=["#7CFC00"  ,  "#32CD32"  , "#006400" , "#9ACD32" , "#00FA9A" , "#8FBC8F" ,     #green colours
                         "#20B2AA" , "#00FFFF" , "#00CED1" , "#008B8B",   ##electric color
                         "#556B2F" , "#808000",#brownish olive green
                         "#E6E6FA", "#B0E0E6" , "#00BFFF" , "#1E90FF" , "#0000FF" , "#000080" , "#7B68EE" , "#8A2BE2",  # blue to purple
                         "#FFC0CB", "#FF69B4" ,   #pink
                         "#C0C0C0", "#808080" , "#2F4F4F",   #grey
                         "#FFFAFA", "#F0FFF0" , "#F0FFFF" ,"#F0F8FF" , "#F5F5DC" ,"#FFFFF0" ,"#FAEBD7" ,"#FFE4E1" , "#FFDEAD", #white - little orange shades in end
                         "#FFFACD", "#F0E68C" , "#FFFF00", "#FFD700"  #yellow
                             ]

    if 'enter_long' in data.columns:
        df_buy = data[data['enter_long'] == 1]
        if len(df_buy) > 0:
            index = 0

            random.shuffle(buy_colours_hex)

            buy_symbols=["circle"  ,  "square"  , "diamond" , "cross" , "pentagon" , "star" ,
                         "hexagram" , "star-triangle-up" , "star-triangle-down" , "star-square",
                         "hexagon" , "star-diamond", "octagon", "diamond-tall"
                         ]

            for enter_tag in df_buy.enter_tag.copy().drop_duplicates():
                enter_tag_series = df_buy[df_buy['enter_tag'] == enter_tag]
                enter_tag_style = generate_enter_tag_style(enter_tag, buy_colours_hex[index%len(buy_colours_hex)], buy_symbols[index%len(buy_symbols)])
                
                # If solo_fade_mask exists, split buys into active/faded
                if solo_fade_mask is not None:
                    buy_indices = enter_tag_series.index
                    buy_active_mask = solo_fade_mask.loc[buy_indices]
                    
                    # Active buys - full opacity
                    buy_active = enter_tag_series[buy_active_mask]
                    if len(buy_active) > 0:
                        buys_active = go.Scatter(
                            x=buy_active.date,
                            y=buy_active.close,
                            mode='markers',
                            text=buy_active.enter_tag,
                            name='enter_long',
                            marker=dict(
                                symbol=enter_tag_style["symbol"],
                                size=enter_tag_style["size"],
                                line=dict(width=1),
                                color=enter_tag_style["color"]
                            )
                        )
                        fig.add_trace(buys_active, 1, 1)
                    
                    # Faded buys - reduced opacity
                    buy_faded = enter_tag_series[~buy_active_mask]
                    if len(buy_faded) > 0:
                        orig_color = enter_tag_style["color"]
                        if orig_color.startswith('#') and len(orig_color) == 7:
                            r = int(orig_color[1:3], 16)
                            g = int(orig_color[3:5], 16)
                            b = int(orig_color[5:7], 16)
                            faded_color = f'rgba({r}, {g}, {b}, 0.15)'
                            faded_line_color = f'rgba({r}, {g}, {b}, 0.15)'
                        elif orig_color.startswith('RGBA') or orig_color.startswith('rgba'):
                            # Handle RGBA colors
                            faded_color = orig_color.replace('1)', '0.15)').replace(',1)', ',0.15)').replace('0.8)', '0.15)')
                            faded_line_color = faded_color
                        else:
                            faded_color = 'rgba(0, 128, 0, 0.15)'
                            faded_line_color = 'rgba(0, 128, 0, 0.15)'
                        
                        buys_faded = go.Scatter(
                            x=buy_faded.date,
                            y=buy_faded.close,
                            mode='markers',
                            text=buy_faded.enter_tag,
                            name='enter_long (faded)',
                            showlegend=False,
                            marker=dict(
                                symbol=enter_tag_style["symbol"],
                                size=enter_tag_style["size"],
                                line=dict(width=0.5, color=faded_line_color),
                                color=faded_color
                            )
                        )
                        fig.add_trace(buys_faded, 1, 1)
                else:
                    buys = go.Scatter(
                        x=enter_tag_series.date,
                        y=enter_tag_series.close,
                        mode='markers',
                        text=enter_tag_series.enter_tag,
                        name='enter_long',
                        marker=dict(
                            symbol=enter_tag_style["symbol"],
                            size=enter_tag_style["size"],
                            line=dict(width=1),
                            color=enter_tag_style["color"]
                        )
                    )
                    fig.add_trace(buys, 1, 1)
                index+=1
        else:
            logger.warning("No buy-signals found.")

    if 'exit_long' in data.columns:
        df_sell = data[data['exit_long'] == 1]
        if len(df_sell) > 0:
            index = 0
            sell_colours_hex=["#8B0000"  ,  "#A52A2A"  , "#B22222" , "#DC143C", #bordo
                         "#CD5C5C" , "#DC143C" , "#B22222" , "#FF0000",   #red
                         "#FF0000" , "#FF0000","#FF0000", "#FF0000" , "#FF6347" , "#FF4500"
                           ]
            random.shuffle(sell_colours_hex)

            sell_symbols=["triangle-up"  ,  "triangle-down"  , "triangle-left" , "triangle-right",
                         "triangle-ne" , "triangle-se" , "triangle-sw" , "triangle-nw",
                         "arrow-left" , "arrow-right","diamond-wide" ,
                          "triangle-up-dot"  ,  "triangle-down-dot"  , "triangle-left-dot" , "triangle-right-dot",
                         "triangle-ne-dot" , "triangle-se-dot" , "triangle-sw-dot" , "triangle-nw-dot",
                         "diamond-wide-dot"
                         ]

            if("exit_tag" in df_sell):
                for exit_tag in df_sell.exit_tag.copy().drop_duplicates():
                    sell_reason_series = df_sell[df_sell['exit_tag'] == exit_tag]
                    sell_reason_style = generate_sell_reason_style(exit_tag, sell_colours_hex[index%len(sell_colours_hex)], sell_symbols[index%len(sell_symbols)])
                    
                    # If solo_fade_mask exists, split sells into active/faded
                    if solo_fade_mask is not None:
                        # Get the mask values for the sell signal indices
                        sell_indices = sell_reason_series.index
                        sell_active_mask = solo_fade_mask.loc[sell_indices]
                        
                        # Active sells - full opacity
                        sell_active = sell_reason_series[sell_active_mask]
                        if len(sell_active) > 0:
                            sells_active = go.Scatter(
                                x=sell_active.date,
                                y=sell_active.close,
                                mode='markers',
                                text=sell_active.exit_tag,
                                name='exit_long',
                                marker=dict(
                                    symbol=sell_reason_style["symbol"],
                                    size=sell_reason_style["size"],
                                    line=dict(width=1),
                                    color=sell_reason_style["color"],
                                )
                            )
                            fig.add_trace(sells_active, 1, 1)
                        
                        # Faded sells - reduced opacity
                        sell_faded = sell_reason_series[~sell_active_mask]
                        if len(sell_faded) > 0:
                            # Convert color to faded version
                            orig_color = sell_reason_style["color"]
                            if orig_color.startswith('#') and len(orig_color) == 7:
                                r = int(orig_color[1:3], 16)
                                g = int(orig_color[3:5], 16)
                                b = int(orig_color[5:7], 16)
                                faded_color = f'rgba({r}, {g}, {b}, 0.20)'
                                faded_line_color = f'rgba({r}, {g}, {b}, 0.20)'
                            else:
                                faded_color = 'rgba(139, 0, 0, 0.20)'
                                faded_line_color = 'rgba(139, 0, 0, 0.20)'
                            
                            sells_faded = go.Scatter(
                                x=sell_faded.date,
                                y=sell_faded.close,
                                mode='markers',
                                text=sell_faded.exit_tag,
                                name='exit_long (faded)',
                                showlegend=False,
                                marker=dict(
                                    symbol=sell_reason_style["symbol"],
                                    size=sell_reason_style["size"],
                                    line=dict(width=0.5, color=faded_line_color),
                                    color=faded_color,
                                )
                            )
                            fig.add_trace(sells_faded, 1, 1)
                    else:
                        sells = go.Scatter(
                            x=sell_reason_series.date,
                            y=sell_reason_series.close,
                            mode='markers',
                            text=sell_reason_series.exit_tag,
                            name='exit_long',
                            marker=dict(
                                symbol=sell_reason_style["symbol"],
                                size=sell_reason_style["size"],
                                line=dict(width=1),
                                color=sell_reason_style["color"],
                            )
                        )
                        fig.add_trace(sells, 1, 1)
                    index+=1
        else:
            logger.warning("No sell-signals found.")

    for  label in indicators1:
        if(label == "main"):
            ##Add main trend area
            fig = plot_area(fig, 1, data, 'bb_lowerband', 'bb_upperband',
                            label=label)
        elif(label.startswith('solo') ):
            ##Add  solo trend area
            fig = plot_area(fig, 1, data, 'bb_lowerband', 'bb_upperband',
                            label=label)


    #UNCOMMENT TO ENABLE FUTURES

    # longs = create_scatter(data, 'enter_long', 'green', 'up')
    # exit_longs = create_scatter(data, 'exit_long', 'red', 'down')
    # shorts = create_scatter(data, 'enter_short', 'blue', 'down')
    # exit_shorts = create_scatter(data, 'exit_short', 'violet', 'up')

    # for scatter in [longs, exit_longs, shorts, exit_shorts]:
    #     if scatter:
    #         fig.add_trace(scatter, 1, 1)

    # # Add Bollinger Bands
    # fig = plot_area(fig, 1, data, 'bb_lowerband', 'bb_upperband',
    #                 label="Bollinger Band")



    # prevent bb_lower and bb_upper from plotting
    try:
        del plot_config["main_plot"]["bb_lowerband"]
        del plot_config["main_plot"]["bb_upperband"]
    except KeyError:
        pass
    # main plot goes to row 1
    fig = add_indicators(fig=fig, row=1, indicators=plot_config["main_plot"], data=data, solo_fade_mask=solo_fade_mask)
    fig = add_areas(fig, 1, data, plot_config["main_plot"])
    fig = plot_trades(fig, trades)

    #  Disabled Volume, indicators 3 enabled
    # volume = go.Bar(
    #     x=data['date'],
    #     y=data['volume'],
    #     name='Volume',
    #     marker_color='DarkSlateGrey',
    #     marker_line_color='DarkSlateGrey'
    # )
    # fig.add_trace(volume, 2, 1)

    # add each sub plot to a separate row
    for i, label in enumerate(plot_config['subplots']):
        sub_config = plot_config['subplots'][label]
        row = 2 + i
        fig = add_indicators(fig=fig, row=row, indicators=sub_config,
                             data=data, solo_fade_mask=solo_fade_mask)
        # fill area between indicators ( 'fill_to': 'other_indicator')
        fig = add_areas(fig, row, data, sub_config)

    return fig

def generate_enter_tag_style(enter_tag, color, symbol):

    premade_tags = {
                    "LOW":          {"color":"#98FB98",
                                    "symbol":"circle-dot",
                                    "size":8},

                    "MID":          {"color":"#7CFC00",
                                    "symbol":"circle-dot",
                                    "size":9},

                    "HIGH":         {"color":"#228B22",
                                    "symbol":"circle-dot",
                                    "size":10},

                    "LONG_UPTREND":{"color":"RGBA(0,128,0,1)",
                                    "symbol":"star-triangle-up",
                                    "size":11},

                    "LONG_DOWNTREND":{"color":"#6B8E23",
                                    "symbol":"star-triangle-down",
                                    "size":10},

                    "SLOW_DOWNTREND":{"color":"#9ACD32",
                                    "symbol":"triangle-down",
                                    "size":8},

                    # "DOWNTREND_UPSWING":{"color":"#00FA9A",
                    #                 "symbol":"cross",
                    #                 "size":11},

                    "BOTTOM_DANGER":  {"color":"#006400",
                                    "symbol":"x",
                                    "size":11},

                    "UPPER_DANGER":{"color":"#8FBC8F",
                                    "symbol":"x",
                                    "size":11}
        }

    if(enter_tag in premade_tags.keys()):
        return premade_tags[enter_tag]
    else:
        return {"color":color, "symbol":symbol, "size":10}


def generate_sell_reason_style(sell_reason, color, symbol):

    premade_tags = {
                    "SELL_LOW":          {"color":"#F08080",
                                    "symbol":"triangle-sw-dot",
                                          "size":8},

                    "SELL_MID":          {"color":"#CD5C5C",
                                    "symbol":"triangle-right-dot",
                                          "size":9},

                    "SELL_HIGH":         {"color":"#B22222",
                                    "symbol":"triangle-up-dot",
                                          "size":9},

                    "SELL_LONG_UPTREND":{"color":"#FF4500",
                                    "symbol":"star-triangle-up-dot",
                                         "size":10},

                    "SELL_LONG_DOWNTREND":{"color":"#FF0000",
                                    "symbol":"star-triangle-down-dot",
                                           "size":10},

                    "SELL_SLOW_DOWNTREND":{"color":"#FF6347",
                                    "symbol":"triangle-down-dot",
                                    "size":9},

                    "SELL_DOWNTREND_UPSWING":{"color":"#F08080",
                                    "symbol":"cross-dot",
                                    "size":10},

                    "SELL_DANGER_ZONE":  {"color":"#800000",
                                    "symbol":"x-dot",
                                    "size":11},

                    "SELL_UPPER_DANGER_ZONE":{"color":"#800000",
                                    "symbol":"x-dot",
                                    "size":11}
        }

    if(sell_reason in premade_tags.keys()):
        return premade_tags[sell_reason]
    else:
        return {"color":color, "symbol":symbol,"size":9}



def generate_profit_graph(
    pairs: str,
    data: dict[str, pd.DataFrame],
    trades: pd.DataFrame,
    timeframe: str,
    stake_currency: str,
    starting_balance: float,
) -> go.Figure:
    # Combine close-values for all pairs, rename columns to "pair"
    try:
        df_comb = combine_dataframes_with_mean(data, "close")
    except ValueError:
        raise OperationalException(
            "No data found. Please make sure that data is available for "
            "the timerange and pairs selected."
        )

    # Trim trades to available OHLCV data
    trades = extract_trades_of_period(df_comb, trades, date_index=True)
    if len(trades) == 0:
        raise OperationalException("No trades found in selected timerange.")

    # Add combined cumulative profit
    df_comb = create_cum_profit(df_comb, trades, "cum_profit", timeframe)

    # Plot the pairs average close prices, and total profit growth
    avgclose = go.Scatter(
        x=df_comb.index,
        y=df_comb["mean"],
        name="Avg close price",
    )

    fig = make_subplots(
        rows=6,
        cols=1,
        shared_xaxes=True,
        row_heights=[1, 1, 1, 0.5, 0.75, 0.75],
        vertical_spacing=0.05,
        subplot_titles=[
            "AVG Close Price",
            "Combined Profit",
            "Profit per pair",
            "Parallelism",
            "Underwater",
            "Relative Drawdown",
        ],
    )
    fig["layout"].update(title="Freqtrade Profit plot")
    fig["layout"]["yaxis1"].update(title="Price")
    fig["layout"]["yaxis2"].update(title=f"Profit {stake_currency}")
    fig["layout"]["yaxis3"].update(title=f"Profit {stake_currency}")
    fig["layout"]["yaxis4"].update(title="Trade count")
    fig["layout"]["yaxis5"].update(title="Underwater Plot")
    fig["layout"]["yaxis6"].update(title="Underwater Plot Relative (%)", tickformat=",.2%")
    fig["layout"]["xaxis"]["rangeslider"].update(visible=False)
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])

    fig.add_trace(avgclose, 1, 1)
    fig = add_profit(fig, 2, df_comb, "cum_profit", "Profit")
    fig = add_max_drawdown(fig, 2, trades, df_comb, timeframe, starting_balance)
    fig = add_parallelism(fig, 4, trades, timeframe)
    # Two rows consumed
    fig = add_underwater(fig, 5, trades, starting_balance)

    for pair in pairs:
        profit_col = f"cum_profit_{pair}"
        try:
            df_comb = create_cum_profit(
                df_comb, trades[trades["pair"] == pair], profit_col, timeframe
            )
            fig = add_profit(fig, 3, df_comb, profit_col, f"Profit {pair}")
        except ValueError:
            pass
    return fig


def generate_plot_filename(pair: str, timeframe: str) -> str:
    """
    Generate filenames per pair/timeframe to be used for storing plots
    """
    pair_s = pair_to_filename(pair)
    file_name = "freqtrade-plot-" + pair_s + "-" + timeframe + ".html"

    logger.info("Generate plot file for %s", pair)

    return file_name


def store_plot_file(fig, filename: str, directory: Path, auto_open: bool = False) -> None:
    """
    Generate a plot html file from pre populated fig plotly object
    :param fig: Plotly Figure to plot
    :param filename: Name to store the file as
    :param directory: Directory to store the file in
    :param auto_open: Automatically open files saved
    :return: None
    """
    directory.mkdir(parents=True, exist_ok=True)

    _filename = directory.joinpath(filename)
    plot(fig, filename=str(_filename), auto_open=auto_open)
    logger.info(f"Stored plot as {_filename}")


def load_and_plot_trades(config: Config):
    """
    From configuration provided
    - Initializes plot-script
    - Get candle (OHLCV) data
    - Generate Dafaframes populated with indicators and signals based on configured strategy
    - Load trades executed during the selected period
    - Generate Plotly plot objects
    - Generate plot files
    :return: None
    """
    strategy = StrategyResolver.load_strategy(config)

    exchange = ExchangeResolver.load_exchange(config)
    IStrategy.dp = DataProvider(config, exchange)
    strategy.ft_bot_start()
    strategy_safe_wrapper(strategy.bot_loop_start)(current_time=datetime.now(UTC))
    plot_elements = init_plotscript(config, list(exchange.markets), strategy.startup_candle_count)
    timerange = plot_elements["timerange"]
    trades = plot_elements["trades"]
    pair_counter = 0
    for pair, data in plot_elements["ohlcv"].items():
        pair_counter += 1
        logger.info("analyse pair %s", pair)

        df_analyzed = strategy.analyze_ticker(data, {"pair": pair})
        df_analyzed = trim_dataframe(df_analyzed, timerange)
        if not trades.empty:
            trades_pair = trades.loc[trades["pair"] == pair]
            trades_pair = extract_trades_of_period(df_analyzed, trades_pair)
        else:
            trades_pair = trades

        fig = generate_candlestick_graph(
            pair=pair,
            data=df_analyzed,
            trades=trades_pair,
            indicators1=config.get('indicators1', []),
            indicators2=config.get('indicators2', []),
            indicators3=config.get('indicators3', []),
            plot_config=strategy.plot_config if hasattr(strategy, 'plot_config') else {}
        )

        store_plot_file(
            fig,
            filename=generate_plot_filename(pair, config["timeframe"]),
            directory=config["user_data_dir"] / "plot",
        )

    logger.info("End of plotting process. %s plots generated", pair_counter)


def plot_profit(config: Config) -> None:
    """
    Plots the total profit for all pairs.
    Note, the profit calculation isn't realistic.
    But should be somewhat proportional, and therefore useful
    in helping out to find a good algorithm.
    """
    if "timeframe" not in config:
        raise OperationalException("Timeframe must be set in either config or via --timeframe.")

    exchange = ExchangeResolver.load_exchange(config)
    plot_elements = init_plotscript(config, list(exchange.markets))
    trades = plot_elements["trades"]
    # Filter trades to relevant pairs
    # Remove open pairs - we don't know the profit yet so can't calculate profit for these.
    # Also, If only one open pair is left, then the profit-generation would fail.
    trades = trades[
        (trades["pair"].isin(plot_elements["pairs"])) & (~trades["close_date"].isnull())
    ]
    if len(trades) == 0:
        raise OperationalException(
            "No trades found, cannot generate Profit-plot without "
            "trades from either Backtest result or database."
        )

    # Create an average close price of all the pairs that were involved.
    # this could be useful to gauge the overall market trend
    fig = generate_profit_graph(
        plot_elements["pairs"],
        plot_elements["ohlcv"],
        trades,
        config["timeframe"],
        config.get("stake_currency", ""),
        config.get("available_capital", get_dry_run_wallet(config)),
    )
    store_plot_file(
        fig,
        filename="freqtrade-profit-plot.html",
        directory=config["user_data_dir"] / "plot",
        auto_open=config.get("plot_auto_open", False),
    )
