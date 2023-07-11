import pandas as pd

__df = pd.read_csv(
    'countries_codes.csv',
    sep='\t', header=0
    )


def code_to_alpha3(code: int) -> str:
    return __df.set_index('Country Code')['Alpha-3'][code]
