# build_df_estimate, find_candidates, find_final_candidates, process_candidates


from itertools import permutations
import pandas as pd
import numpy as np


def build_df_estimate(pdc):
    '''
    Returns df with all compositions for which aiphad did a prediction + column with phases
    '''
    df_estimate = pd.DataFrame(data=pdc.composition_data_list)
    df_estimate['phase']=pdc.predicted_all_labels
    df_estimate = round(df_estimate,2)
    df_estimate['diff'] = df_estimate['phase'].diff()
    return  df_estimate


def find_candidates(elements, df_estimate, step_limit=0.06):
    '''
    Returns all points on intersection of k+1 phases
    '''
    list_indexes = []
    for perm in list(permutations(range(len(elements)))):
        #sorted_df = df_estimate.sort_values(by=[df_estimate.columns[perm[0]],df_estimate.columns[perm[1]],df_estimate.columns[perm[2]],df_estimate.columns[perm[3]],df_estimate.columns[perm[4]]])
        sorted_df = df_estimate.sort_values(by=[df_estimate.columns[perm[i]] for i in range(len(elements))])
        sorted_df['diff'] = sorted_df['phase'].diff()
        #drop rows where nonzero diff is caused by 'resetting' composition in some columns (e.g. 0.2-0.98,0.2-0.99,0.2-1.0,0.21-0.0,0.21-0.01 )
        dif=set(range(0,len(elements))) - {perm[0]}
        for d in range(len(dif)):
            col_to_check = list(dif)[d]
            sorted_df['diff_compo_'+str(d)] = sorted_df[df_estimate.columns[col_to_check]].diff()
            sorted_df = sorted_df.drop(sorted_df[np.abs(sorted_df['diff_compo_'+str(d)])>step_limit].index).copy()
    
        df_nonzero_diffs=sorted_df[sorted_df['diff']!=0]
        diff_indexes = df_nonzero_diffs.index[1:]
        phases = df_nonzero_diffs['phase'].values[1:]
        diffs = df_nonzero_diffs['diff'].values[1:]
        list_indexes.append([diff_indexes, phases, diffs])
    
    return list_indexes

def process_candidates(list_indexes):
    '''
    takes the candidates (the list of indexes-phases-and diffs) and creates an organised dataframe
    '''
    all_indexes = []
    all_phases = []
    all_diffs = []
    for i in range(len(list_indexes)):
        all_indexes.append([x for x in list_indexes[i][0]])
        all_phases.append([x for x in list_indexes[i][1]])
        all_diffs.append([x for x in list_indexes[i][2]])
    
    all_indexes_flatten = []
    all_phases_flatten = []
    all_diffs_flatten = []
    all_indexes_flatten.append([x for xs in all_indexes for x in xs])
    all_phases_flatten.append([x for xs in all_phases for x in xs])
    all_diffs_flatten.append([x for xs in all_diffs for x in xs])

    df_indexes = pd.DataFrame()
    df_indexes['indexes'] = pd.Series(all_indexes_flatten[0])
    df_indexes['phases'] = pd.Series(all_phases_flatten[0])
    df_indexes['diffs'] = pd.Series(all_diffs_flatten[0])

    return df_indexes


def find_final_candidates(df_indexes, n_phases=3):
    df_unique = df_indexes.drop_duplicates().copy()
    df_indexes_counts = pd.DataFrame(df_unique['indexes'].value_counts())
    return df_indexes_counts[df_indexes_counts['count']>=n_phases].index.get_level_values(0)