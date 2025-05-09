# cleaning_functions.py

import pandas as pd


def clean_state(df):
    df['state'] = df['state'].replace({
        'Cali': 'California',
        'AZ': 'Arizona',
        'WA': 'Washington'
    }).fillna('Unknown')
    return df

def fill_customer_lifetime_value(df):
    median_clv = df['customer_lifetime_value'].median()
    df['customer_lifetime_value'] = df['customer_lifetime_value'].fillna(median_clv)
    return df

def fill_categorical_with_mode(df, column):
    mode_val = df[column].mode()[0]
    df[column] = df[column].fillna(mode_val)
    return df

def remove_duplicates(df):
    df = df.drop_duplicates(subset=['customer'], keep='first')
    df = df.reset_index(drop=True)
    return df

def quick_data_report(df):
    print("\nDataFrame shape:", df.shape)
    print("\nData types:\n", df.dtypes)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDescriptive statistics:\n", df.describe())

def main_cleaning(df):
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Rename 'st' to 'state'
    df.rename(columns={ 'st' : 'state' }, inplace=True)

    # Fix customer_lifetime_value: remove % and convert to float
    df['customer_lifetime_value'] = (
        df['customer_lifetime_value']
        .str.replace('%', '')
        .astype(float)
    )

    # Now apply normal cleaning
    df = clean_state(df)
    df = fill_customer_lifetime_value(df)
    df = fill_categorical_with_mode(df, 'gender')
    df = fill_categorical_with_mode(df, 'education')
    df = fill_categorical_with_mode(df, 'vehicle_class')
    df = remove_duplicates(df)
    
    return df
