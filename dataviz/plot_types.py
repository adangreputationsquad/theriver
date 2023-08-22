from enum import Enum
import dataviz.src.components as cp
from dataviz.src.components.iplot import IPlot


class POINT_ENUM(Enum):
    NAME_VALUE = cp.point_name_value.PointNameValue
    VALUE = cp.point_value.PointValue


class LIST_ENUM(Enum):
    ALL_VALUES = cp.all_values.AllValues


class DICT_ENUM(Enum):
    ALL_VALUES = cp.all_values.AllValues
    ALL_KEYS = cp.all_keys.AllKeys
    ALL_KEYS_VALUES = cp.all_keys_values.AllKeysValues
    TIMESERIES = cp.timeseries.Timeseries
    PIE_CHARTS = cp.pie_charts.PieChart
    MAP = cp.map.Map


class DF_ENUM(Enum):
    TIMESERIES = cp.timeseries.Timeseries
    SCATTER_PLOT = cp.scatter_plot.ScatterPlot
    LINE_CHARTS = cp.line_charts.LineChart
    BAR_CHARTS = cp.bar_charts.BarChart
    PIE_CHARTS = cp.pie_charts.PieChart
    BUBBLE_CHARTS = cp.bubble_charts.BubbleChart
    MAP = cp.map.Map


class PLOT:
    POINT = POINT_ENUM
    DICT = DICT_ENUM
    LIST = LIST_ENUM
    DF = DF_ENUM


def name_to_plot(name: str) -> IPlot:
    """
    Gives the PLOT class given the name
    :param name:
    :return:
    """
    for cls in [POINT_ENUM, DICT_ENUM, LIST_ENUM, DF_ENUM]:
        for plot_type in cls:
            if plot_type.value.name() == name:
                return plot_type.value
    raise ValueError(f"name '{name}' not found")
