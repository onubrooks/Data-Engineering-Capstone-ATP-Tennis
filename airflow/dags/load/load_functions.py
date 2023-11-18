import pandas as pd
import pycountry

def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_3=code).name
    except:
        try:
            return pycountry.historic_countries.get(alpha_3=code).name
        except:
            return None
        
def str_to_datetime(x):
    if pd.isnull(x):
        return None
    else:
        try:
            return pd.to_datetime(x, format='%Y%m%d')
        except:
            return None
        
def print_df(df):
    print(df.head())