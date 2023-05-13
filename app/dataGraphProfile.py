'''
 # @ Author: Yixiang Zhang
 # @ Create Time: 2023-04-01 21:49:04
 # @ Modified by: Yixiang Zhang
 # @ Modified time: 2023-04-01 21:49:08
 # @ Description: a repo for a list of methods
 '''
 
import pandas as pd
import numpy as np

    
def get_num_cat_dtype(input_df):
    """_summary_
    return the two list containing columns of categorical data and numerical data

    :param _type_ input_df: _description_
    :return _type_: _description_
    """
    numerical_col = []
    categorical_col = []
    
    for col in input_df.columns:
        curr_type = input_df[col].dtype
        if curr_type in ["object","bool"]:
            categorical_col.append(col)
        else:
            numerical_col.append(col)
        print(curr_type)
        
    return numerical_col, categorical_col



def get_categorical_distribution(input_df,cat_col_list):
    """_summary_
    For a column with categorical values (), get the minimum and maximum length of the string
    for every column in df[[a,b,c]] and export in json format
    
    output looks like
    {
        'activeupondischarge': {'min': 4, 'max': 5},
        'diagnosisstring': {'min': 24, 'max': 146},
        'icd9code': {'min': 3, 'max': 35},
        'diagnosispriority': {'min': 5, 'max': 7}
    }
    
    :param _type_ input_df: _description_
    :param _type_ cat_col_list: _description_
    :return _type_: _description_
    """
    res = {}
    
    for col in cat_col_list:
        res[col] = {"min":input_df[col].apply(str).apply(len).min(),
                    "max":input_df[col].apply(str).apply(len).max()}
        
    return res
        
 
def get_pattern(input_df):
    """
    Finding the regex pattern for your dataframe, three types are implemented
    for now, for numerical column, for lowercase column, for uppercase column

    :param dataframe input_df: a dataframe you wish to find pattern from
    :return dataframe: a boolean dataframe for heatmap plot
    """

    # define your local methods
    contains_digit = lambda x: any([char.isdigit() for char in x])
    contains_lower = lambda x: any([char.islower() for char in x])
    contains_upper = lambda x: any([char.isupper() for char in x])

    methods_list = [contains_digit,contains_lower,contains_upper]
    
    res = pd.DataFrame()
    
    for i in range(3):
        temp = input_df.applymap(str).applymap(methods_list[i]).apply(any)
        res = pd.concat([res,temp],axis=1)

    # rename the columns    
    res.set_axis(["0","a","A"],axis=1,copy=False)
    
    return res

