# compo_grid,  save_df_liquidus_phases, prepare_df_for_aiphad, update_df
# update_aiphad_df


from itertools import product
import pandas as pd
import numpy as np
import os

def compo_grid(composition_grid, elements):
    compo_list = []
    for i in range(len(elements)-1): #len(elements)-1 - We don't add the first element which is the balance !
        compo_list.append(composition_grid)
    
    combinations = product(*compo_list) #Generate all combinations
    
    df = pd.DataFrame(combinations, columns=elements[1:])
    
    df = df[df.sum(axis=1) <= 1].reset_index(drop=True) #Remove all impossible compositions with a global composition > 100%...
    df[elements[0]] = 1-df.sum(axis=1) # We calculate the balance !
    df.insert(0, elements[0], df.pop(elements[0])) #We move the balance as the first column
    df = round(df,5)
    return df


def save_df_liquidus_phases(df, elements, liquidus_temperature_l, primary_cryst_phase_l):
    df['Liquidus temperature in K'] = liquidus_temperature_l
    for col in df.columns.tolist():
        df[col]=round(df[col],2)
    filtered_l = [[item for item in sublist if "liq" not in item.lower()] for sublist in primary_cryst_phase_l]   
    print(filtered_l)
    flat_list = [item[0] for item in filtered_l]
    print(flat_list)
    df['Primary Crystallization Phase'] = flat_list  
    df['Primary Crystallization Phase'] = df['Primary Crystallization Phase'].str.split('#').str[0] 
    df = df.drop(df[df.iloc[:,len(elements)+1]=='none'].index).copy()
    df.to_csv('-'.join(elements)+'_Primary_Cryst_Domains.csv', index = False)


def prepare_df_for_aiphad(df, elements, prediction_precision): #, proposal_to_skip=[]):
    df_from_tc = pd.read_csv('-'.join(elements)+'_Primary_Cryst_Domains.csv')
    df_from_tc.iloc[:,:len(elements)] = round(df_from_tc.iloc[:,:len(elements)],2)
    composition_grid = np.linspace(0,1,prediction_precision)
    df_grid = compo_grid(composition_grid, elements)
    df_grid.insert(len(elements), 'Primary Crystallization Phase', '')
    df_grid = round(df_grid,3)

    for ind in range(len(df_from_tc)):
        if sum((df_grid.iloc[:,:len(elements)]==tuple(df_from_tc.iloc[ind,:len(elements)])).all(axis=1))>0:
            index_in_grid = df_grid[(df_grid.iloc[:,:len(elements)]==tuple(df_from_tc.iloc[ind,:len(elements)])).all(axis=1)].index[0]
            df_grid.iloc[index_in_grid,len(elements)] = df_from_tc.iloc[ind,len(elements)+1]
        else:
            df_grid.loc[len(df_grid)] = df_from_tc.iloc[ind, df.columns != 'Liquidus temperature in K']
    df_grid.to_csv('-'.join(elements)+'data_aiphad_input.csv', index=False)
    return df_grid


def update_df(df, liquidus_temperature, primary_phase, proposals_X):
    ''' df: dataframe with primary crystal phases (not all grid)'''
    if tuple(proposals_X) not in list(zip(*[df[col] for col in df.columns[:len(elements)]])):
        flat_list = [item for item in primary_phase if "liq" not in item.lower()]
        new_row = [ round(prX,2) for prX in proposals_X[:len(elements)]]
        new_row.append(liquidus_temperature)
        new_row.append(flat_list[0].split('#')[0])
        df.loc[len(df)] = new_row
        print(new_row)
        df.to_csv('-'.join(elements)+'_Primary_Cryst_Domains.csv', index = False)
    return df


def update_aiphad_df(df, liquidus_temperature, primary_phase, proposals_X, elements):
    ''' df: dataframe with primary crystal phases (not all grid)'''
    df_aiphad = pd.read_csv('-'.join(elements)+'data_aiphad_input.csv')
    if tuple(proposals_X) not in list(zip(*[df[col] for col in df.columns[:len(elements)]])):
        flat_list = [item for item in primary_phase if "liq" not in item.lower()]
        new_row = [ round(prX,2) for prX in proposals_X[:len(elements)]]
        new_row.append(liquidus_temperature)
        new_row.append(flat_list[0].split('#')[0])
        df.loc[len(df)] = new_row
        print(new_row)

        if sum((df_aiphad.iloc[:,:len(elements)]==tuple(new_row[:len(elements)])).all(axis=1))>0:
            index_in_grid = df_aiphad[(df_aiphad.iloc[:,:len(elements)]==tuple(new_row[:len(elements)])).all(axis=1)].index[0]
            df_aiphad.iloc[index_in_grid,len(elements)] = new_row[len(elements)+1]
        else:
            df_aiphad.loc[len(df_aiphad)] = [new_row[i] for i in range(len(new_row)) if i != (len(new_row)-2)]
            
    round(df.iloc[:,:len(elements)],2).to_csv('-'.join(elements)+'_Primary_Cryst_Domains.csv', index = False)
    df_aiphad.to_csv('-'.join(elements)+'data_aiphad_input.csv', index=False)
    
    return df, df_aiphad

