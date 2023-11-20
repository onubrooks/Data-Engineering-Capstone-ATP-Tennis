import os
import pyarrow.csv as pv
import pyarrow.parquet as pq

def convert_to_parquet(csv_file, parquet_file):
    """convert csv to parquet

    Args:
        csv_file (_type_): the csv file to convert
        parquet_file (_type_): the parquet file to write to

    Raises:
        ValueError: if the input file is not in csv format
    """
    if not csv_file.endswith('csv'):
        raise ValueError('The input file is not in csv format')
    
    print(f'Reading {csv_file}')
    table=pv.read_csv(os.path.abspath(csv_file))
    print(f'Writing {parquet_file}')
    pq.write_table(table, parquet_file)