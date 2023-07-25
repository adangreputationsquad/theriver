from enum import Enum, auto


class POINT_ENUM(Enum):
    NAME_VALUE = "name, value"
    VALUE = "value"


class LIST_ENUM(Enum):
    ALL_VALUES = "all values"


class DICT_ENUM(Enum):
    ALL_VALUES = "all values"
    ALL_KEYS = "all keys"
    ALL_KEYS_VALUES = "all keys and values"
    TIMESERIES = "timeseries"
    PIE_CHARTS = "piecharts"
    MAP = "map"


class DF_ENUM(Enum):
    TIMESERIES = "timeseries"
    SCATTER_PLOT = "scatter plot"
    LINE_CHARTS = "line charts"
    BAR_CHARTS = "bar charts"
    PIE_CHARTS = "pie charts"
    BUBBLE_CHARTS = "bubble charts"
    MAP = "map"


class PLOT:
    POINT = POINT_ENUM
    DICT = DICT_ENUM
    LIST = LIST_ENUM
    DF = DF_ENUM
