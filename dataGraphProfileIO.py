import dataprofiler as dp
import pathlib
import json
import pandas as pd
import gzip
import os

from collections import defaultdict

def find_csvs(data_direcotry):
    """
    find every .csv and .csv.gz file in the directory and return it
    as a list
    Args:
        data_direcotry (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Define the directory to search in
    path = pathlib.Path(data_direcotry)

    # Find all .csv and .csv.gz files in the directory
    gz_files = list(path.rglob('*.csv.gz'))

    csv_files = list(path.rglob('*.csv'))
    
    # # merge two list
    files = csv_files + gz_files

    # # convert from POSIX to str
    files = [str(file) for file in files]
    return files


# files = find_csvs(data_direcotry="../rawdata/")


def get_report(filepath):
    """
    input filepath for a csv, use dataprofiler to grab it's profile before outputing
    Args:
        filepath (_type_): _description_

    Returns:
        (pandas.dataframe): _description_
    """
    # overcome dataprofiler can't read .csv.gz file
    
    # if os.path.splitext(filepath)[1] == ".csv":
    #     # read it with data profiler
    #     df = dp.Data(filepath)
    # else:
    #     # open the compressed file
    #     with gzip.open(filepath,'rb') as f:
    #         # read the csv file
    #         df = pd.read_csv(f)
    #     # automatically close afterwords

    # .csv or .csv.gz file --> dataframe --> dataprofiler --> dict()
    data = pd.read_csv(filepath)
    profile = dp.Profiler(data)
    report = profile.report(report_options={"output_format":"pretty"})
    
    # dict() --> pd.dataframe, then transform with apply
    df = pd.DataFrame.from_dict(report["data_stats"])
    
    df['min'] = df['statistics'].apply(lambda x: x["min"])
    df['max'] = df['statistics'].apply(lambda x: x["max"])
    df['null_count'] = df['statistics'].apply(lambda x: x["null_count"])
    df['unique_count'] = df['statistics'].apply(lambda x: x["unique_count"])
    df['unique_ratio'] = df['statistics'].apply(lambda x: x["unique_ratio"])

    df.drop(["statistics","samples"],axis =1,inplace=True)
    
    return df 

# testing
# df = get_report(files[0])
