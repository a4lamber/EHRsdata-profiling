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
    """
    return the two list containing columns of categorical data and numerical data
    Args:
        input_df (pandas dataframe): dataframe you wish to determine 
        whether it's cateogircal or numerical

    Returns:
        numerical_col (list): a list of columnnames for numerical data 
        categorical_col (list): a list of columnnames for categorical data 
    Note:
        is implemented with selected_dtypes better? revisit later
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
    """
    get the minimum and maximum for every column in df[[a,b,c]] and export
    in json format
    Args:
        input_df (_type_): _description_
        cat_list (_type_): a list of categorical distribution
    Returns:
        res (dict): a nested json containing result
    Example:
        output looks like
        {'activeupondischarge': {'min': 4, 'max': 5},
        'diagnosisstring': {'min': 24, 'max': 146},
        'icd9code': {'min': 3, 'max': 35},
        'diagnosispriority': {'min': 5, 'max': 7}}
    """
    res = {}
    
    for col in cat_col_list:
        res[col] = {"min":input_df[col].apply(str).apply(len).min(),
                    "max":input_df[col].apply(str).apply(len).max()}
        

    return res
        
        
def get_pattern(input_df):
    """
    find the patterns for this this dataset
    Args:
        input_df (_type_): the dataframe you wish to compute pattern

    Returns:
        res (dataframe): a boolean dataframe for heatmap plot
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

