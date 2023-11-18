import os
import pyarrow.csv as pv
import pyarrow.parquet as pq

def convert_to_parquet(csv_file, parquet_file):
    if not csv_file.endswith('csv'):
        raise ValueError('The input file is not in csv format')
    
    print(f'Reading {csv_file}')
    table=pv.read_csv(os.path.abspath(csv_file))
    print(f'Writing {parquet_file}')
    pq.write_table(table, parquet_file)