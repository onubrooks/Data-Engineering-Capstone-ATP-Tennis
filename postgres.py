from time import time

from sqlalchemy import create_engine
import pandas as pd

# Create a function that will create a DB connection to our postgres DB and  ingestion into it

def get_db_conn_engine(user, password, host, port, db):
    # Create a function that will create a DB connection to our postgres DB and  ingestion into it

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    print("connection was made successfully ")

    return engine

def create_db_table(engine, table_name, df):
    """Creates a table in the database using the dataframe column headers as the table column headers

    Args:
        engine (_type_): _description_
        table_name (_type_): _description_
        df (_type_): _description_
    """

    #Creates a table with the column headers
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    print(f"Created table: {table_name}")


def insert_into_db(engine, table_name, df):
    """Inserts data into the table in the database using the dataframe column headers as the table column headers

    Args:
        engine (_type_): _description_
        table_name (_type_): _description_
        df (_type_): _description_
    """

    df.to_sql(name=table_name, con=engine, if_exists='append')

    print(f"Inserted data into the table: {table_name}")