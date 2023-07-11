from enum import Enum, auto


class POINT_ENUM(Enum):
    NAME_VALUE = auto()
    VALUE = auto()


class LIST_ENUM(Enum):
    ALL_VALUES = auto()


class DICT_ENUM(Enum):
    ALL_VALUES = auto()
    ALL_KEYS = auto()
    ALL_KEYS_VALUES = auto()
    TIMESERIES = auto()
    PIE_CHARTS = auto()
    MAP = auto()


class DF_ENUM(Enum):
    TIMESERIES = auto()
    SCATTER_PLOT = auto()
    LINE_CHARTS = auto()
    BAR_CHARTS = auto()
    PIE_CHARTS = auto()
    BUBBLE_CHARTS = auto()
    MAP = auto()


class PLOT:
    POINT = POINT_ENUM
    DICT = DICT_ENUM
    LIST = LIST_ENUM
    DF = DF_ENUM
