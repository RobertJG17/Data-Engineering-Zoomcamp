import pandas as pd
import sys
from sqlalchemy import create_engine
from time import time
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # TRIPS URL: "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet"
    # ZONES URL: "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

    # DEFINE WHAT TO NAME FILE DOWNLOADED IN CURL REQUEST
    file_name = 'output.parquet'
    
    # EXECUTES CURL CMD TO FETCH PARQUET AND DOWNLOAD IT TO ROOT PROJECT DIRECTORY
    os.system(f"curl {url} --output {file_name}")

    # ESTABLISHING POSTGRES DATABASE CONNECTION
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # READING IN LOCAL PARQUET FILE
    df = pd.read_parquet(file_name)

    # INITIALIZING CHUNKSIZE AND TIME ELAPSED VARIABLES
    chunksize = 10000
    time_elapsed = 0
    
    # LOADING DATA CHUNKS OF SIZE 100000 FROM DF TO POSTGRES DATABASE
    print('Data Migration in process...')
    start = time()
    df.to_sql(table_name, con=engine, if_exists = 'replace', chunksize=chunksize)
    end = time()
    
    # PRINT SMALL REPORT NOTING HOW LONG THE EXECUTION OF THE SCRIPT TOOK
    time_elapsed = end - start
    print(f'Data loaded into Postgres, {len(df)} records took {time_elapsed} seconds.')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user
    # password
    # host
    # port
    # database name
    # table name
    # url of tbe csv

    for arg in ['--user', '--password', '--host', '--port', '--db', '--table_name', '--url']:
        parser.add_argument(arg, f'{arg} for Postgres') 

    args = parser.parse_args()

    main(args)
