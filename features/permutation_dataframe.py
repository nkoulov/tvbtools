from math import perm
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append('C:\\Users\\Wayne\\tvb\\TVB_workflow\\functions')
from bootstrap import BootstrapTest
from permutation import PermutationTest
import pandas as pd
from scipy.stats import mannwhitneyu
import os
import itertools


def add_star(data):
    if data <= 0.001:
        tmp_data = str(data) + '***'
    elif data <= 0.01:
        tmp_data = str(data) + '**'
    elif data < 0.05:
        tmp_data = str(data) + '*'
    else:
        tmp_data = data
    return tmp_data





def stats_calculator(datatable):
    """
    Args:
        datatable, including grouping variable
    Output
        the permutation resutls for each groups
    """
    groups = pd.unique(datatable.loc[:,'groups'])
    groups_num = range(len(groups))

    comba = list(itertools.combinations(groups_num, 2))

    # give labels to comba
    comba_with_name = []
    for a, x in enumerate(comba):
        tmp_one = (groups[x[0]], groups[x[1]])
        comba_with_name.append(tmp_one)

    overall_permu =np.zeros((len(datatable.columns), len(comba)))
    for a,col in enumerate(datatable.columns):
        if isinstance(datatable.iloc[0,a], (np.integer, np.float64)):
            deList = [[] for i in groups_num]
            for x in groups_num:
                deList[x] = datatable.loc[datatable['groups'].isin([groups[x]]), [col]].values.flatten()
            tmp_list = np.array([])
            for y in comba:
                p_value = PermutationTest(deList[y[0]], deList[y[1]], iteration = 10000, visualization = False)
                tmp_list = np.append(tmp_list, p_value)
            overall_permu[a, :] = tmp_list

        else:
            continue
    dataframe = pd.DataFrame(overall_permu, index=datatable.columns, columns=comba_with_name)
    # drop the 0 value columns in original datatable
    for col in datatable.columns:
        if np.all(dataframe.loc[col, :].values):
            continue
        else:
            dataframe.drop([col], axis=0, inplace = True)
    
    # add asterisk sign
    for i in range(np.shape(dataframe)[0]):
        for k in range(np.shape(dataframe)[1]):
            dataframe.iloc[i,k] = add_star(dataframe.iloc[i,k])
    return dataframe


G_table = pd.read_excel('C:/Users/Wayne/tvb/stat_data/Gc_Go.xlsx', sheet_name='Gc_Go')
Mix_table = pd.read_excel('C:/Users/Wayne/tvb/stat_data/mix_final.xlsx')
amp = pd.read_excel('C:/Users/Wayne/tvb/amp_abs.xlsx')
freq = pd.read_excel('C:/Users/Wayne/tvb/freq.xlsx')

stats_calculator(amp).to_excel('amplitude_abs_average.xlsx')


