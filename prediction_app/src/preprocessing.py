# Import libraries
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer  

# Define column types
target_col = 'binary_target'
categorical_cols = ['регион', 'использование', 'pack']
continuous_cols = ['сумма', 'частота_пополнения', 'доход','сегмент_arpu', 'частота', 'объем_данных', 'on_net', 'продукт_1',
        'продукт_2','секретный_скор', 'pack_freq']
drop_col = ['client_id', 'зона_1', 'зона_2', 'mrg_']

def import_data(path_to_file):

    # Get input dataframe
    input_df = pd.read_csv(path_to_file).drop(columns=drop_col)

    return input_df

# Main preprocessing function
def run_preproc(input_df):

    output_df = input_df

    for col in categorical_cols:
        output_df[col] = output_df[col].fillna('missed')

    imp_mean = SimpleImputer(missing_values=np.nan, strategy='median')
    for col in continuous_cols:
        output_df[col] = imp_mean.fit_transform(output_df[col].values.reshape(-1,1))
   
    # Return resulting dataset
    return output_df