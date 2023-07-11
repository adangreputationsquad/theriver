from enum import Enum


class POINT_ENUM(Enum):
    NAME_VALUE = "name_value"
    VALUE = "value"


class LIST_ENUM(Enum):
    ALL_VALUES = "all_values"


class DICT_ENUM(Enum):
    ALL_VALUES = "all_values"
    ALL_KEYS = "all_keys"
    ALL_KEYS_VALUES = "all_keys_values"
    TIMESERIES = "timeseries"


class DF_ENUM(Enum):
    TIMESERIES = "timeseries"
    SCATTER_PLOT = "scatter_plot"
    LINE_CHARTS = "line_charts"
    BAR_CHARTS = "bar_charts"


class PLOT:
    POINT = POINT_ENUM
    DICT = DICT_ENUM
    LIST = LIST_ENUM
    DF = DF_ENUM
