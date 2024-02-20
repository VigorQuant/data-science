# -*- coding: utf-8 -*-
"""
03 data cleaning

@author: WEI
"""

import pandas as pd
import numpy as np
import re
import math

def load_csv(file_path, selected_columns=None): 
    df = pd.read_csv(file_path)

    if selected_columns: 
        df = df[selected_columns] 
    return df

def drop_columns(df, columns_to_drop): 
    return df.drop(columns=columns_to_drop)

def process_host_verifications(df, host_verifications_set, column_name='host_verifications'): 
    def extract_verification(entry, verification): 
        entry_list = str(entry).replace("[", "").replace("]", "").replace("'", "").replace('"', "").replace(" ", "").split(',')
        return 1 if (verification in entry_list) else 0
    
    for verification in host_verifications_set: 
        df[verification] = df[column_name].apply(lambda x: extract_verification(x, verification)) 
    return df.drop(columns=[column_name])

def clean_percent_column(df, column_name): 
    df[column_name] = df[column_name].apply(lambda x: str(x).replace('%', '') if pd.notna(x) else '0') 
    return df

def convert_boolean_to_binary(df, columns): 
    df[columns] = df[columns].applymap(lambda x: 1 if x == 't' else 0) 
    return df

def log_transform_price(df, column_name='price'): 
    df[column_name] = df[column_name].apply(lambda x: np.log(float(x.replace('$', '').replace(',', ''))) if pd.notna(x) else -55) 
    return df

def fill_na_with_zero(df, columns): 
    df[columns] = df[columns].fillna(0) 
    return df

def fill_beds_based_on_accommodates(df, column_to_fill='beds', based_on_column='accommodates'): 
    df[column_to_fill].fillna(df[based_on_column], inplace=True) 
    return df

# ... (You can add more utility functions here for bathrooms, reviews, etc.)

if __name__ == '__main__': 
    folder_path = 'D:/.../dataset/new york/June' 
    csv_file = f"{folder_path}/Detailed Listings.csv" 
    
    # Define sets and columns to be used
    host_verification_set = {'email_verification', 'phone_verification'} # Define your verification set columns_to_drop = ['host_name', 'host_about', 'calendar_updated'] # Define columns to drop
    boolean_columns = ['host_is_superhost', 'host_has_profile_pic', 'host_identity_verified', 'has_availability','instant_bookable']
    
    # Load CSV file
    listings_df = load_csv(csv_file)
    
    # Filter data
    listings_df = listings_df[listings_df['neighbourhood_group_cleansed'] == 'Manhattan']
    listings_df = drop_columns(listings_df, ['neighbourhood_group_cleansed'])
   
    # Preprocessing
    listings_df = process_host_verifications(listings_df, host_verification_set)
    listings_df = clean_percent_column(listings_df, 'host_response_rate')
    listings_df = convert_boolean_to_binary(listings_df, boolean_columns)
    listings_df = log_transform_price(listings_df)
    listings_df = fill_na_with_zero(listings_df, ['reviews_per_month'])
    listings_df = fill_beds_based_on_accommodates(listings_df)
    
    # ... (You can add more preprocessing steps here)
    # Resulting DataFrame 
    print(listings_df.head())
    
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy.stats import skew
from scipy.special import boxcox1p
import datetime as dt

def classify_property(data, column_name='property_type'): 
    def _classify_type(entry):
        if 'Entire' in entry: 
            return 'Entire Unit Rentals' 
        elif 'Private room' in entry: 
            return 'Private Rooms' 
        elif 'Shared room' in entry: 
            return 'Shared Rooms' 
        elif 'Room' in entry: 
            return 'Hotel-like' 
        else:
            return 'Unique Stays' 
        
    data[column_name] = data[column_name].apply(_classify_type) 
    return data

def process_host_since(data, column_name='host_since', dummy_date=dt.datetime(2018, 11, 10)): 
    data[column_name] = data[column_name].apply(lambda x: np.nan if pd.isna(x) else x)
    data.dropna(subset=[column_name], inplace=True)
    data[column_name] = (dummy_date - pd.to_datetime(data[column_name])).apply(lambda x: float(x.days)) 
    return data

def fill_missing_scores(data, score_cols): 
    for col in score_cols: 
        data[col] = data[col].apply(lambda x: 0 if np.isnan(x) else x) 
        return data 
    
def encode_labels(data, cols): 
    for col in cols:
        lbl = LabelEncoder()
        lbl.fit(list(data[col].values))
        data[col] = lbl.transform(list(data[col].values)) 
        return data 
    
def boxcox_transform(data, threshold=0.75): 
    numeric_feats = data.dtypes[data.dtypes != "object"].index
    skewed_feats = data[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False) 
    skewness = skewed_feats[abs(skewed_feats) > threshold] 
    skewed_features = skewness.index
    lam = 0.15
    for feat in skewed_features: 
        data[feat] = boxcox1p(data[feat], lam) 
    return data 

def one_hot_encode(data, cols): 
    for col in cols: 
        parsed_cols = pd.get_dummies(data[col])
        data = pd.concat([data.drop(columns=[col]), parsed_cols], axis=1) 
    return data

# Assuming 'data' DataFrame is previously loaded
data = pd.DataFrame() # Load your data here

# Classify property types 
data = classify_property(data)

# Process host_since column
data = process_host_since(data)

# Fill missing review scores
score_cols = ['review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
              'review_scores_checkin', 'review_scores_communication', 'review_scores_location','review_scores_value']
data = fill_missing_scores(data, score_cols)

# Label Encoding 
encode_cols = ['beds', 'bathrooms']
data = encode_labels(data, encode_cols)

# Box-Cox Transformation
data = boxcox_transform(data)

# One-Hot Encoding 
one_hot_cols = ['property_type', 'room_type', 'neighbourhood_cleansed', 'host_response_time']
data = one_hot_encode(data, one_hot_cols)

# Now 'data' contains processed features

import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler 

def normalize_dataframes(dfs): 
    """Normalize list of DataFrames using MinMaxScaler."""
    scaler = MinMaxScaler() 
    return [pd.DataFrame(scaler.fit_transform(df.values), columns=df.columns) for df in dfs]


def split_and_normalize(dataset, target_col='price', val_frac=0.1, test_frac=0.1, random_state=1): 
    """Split dataset into training, validation, and test sets, and normalize features.""" 
    # Define feature and target columns
    feature_cols = [col for col in dataset.columns if col not in [target_col, 'id', 'host_id', 'Unnamed: 0']]
    X = dataset[feature_cols]
    y = dataset[target_col]
    
    # Split into training, validation, and test sets 
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=val_frac + test_frac, random_state=random_state)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=test_frac / (val_frac + test_frac), random_state=random_state)
    
    # Normalize features 
    X_train, X_val, X_test = normalize_dataframes([X_train, X_val, X_test]) 
    return X_train, y_train, X_val, y_val, X_test, y_test
    
    
if __name__ == '__main__': 
    random.seed(13)

    # Load cleaned data 
    dataset = pd.read_csv('data_cleaned.csv')
    # Split and normalize data 
    X_train, y_train, X_val, y_val, X_test, y_test = split_and_normalize(dataset)
    
    # Save to CSV files X_train.to_csv('data_cleaned_train_X.csv', index=False)
    y_train.to_csv('data_cleaned_train_y.csv', index=False)
    X_val.to_csv('data_cleaned_val_X.csv', index=False)
    y_val.to_csv('data_cleaned_val_y.csv', index=False)
    X_test.to_csv('data_cleaned_test_X.csv', index=False)
    y_test.to_csv('data_cleaned_test_y.csv', index=False)
    
    
    