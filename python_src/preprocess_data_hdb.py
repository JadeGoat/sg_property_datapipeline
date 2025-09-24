import pandas as pd

def preprocess_hdb_rental_data(data):
    process_data = data.copy()

    # Split 'month' column and convert to integer
    columns_name = ['approval_year', 'approval_month']
    process_data[columns_name] = process_data['rent_approval_date'].str.split('-', expand=True)
    process_data['approval_year'] = pd.to_numeric(process_data['approval_year'], errors='coerce')
    process_data['approval_month'] = pd.to_numeric(process_data['approval_month'], errors='coerce')

    # Drop unnecessary columns
    process_data.drop(columns='rent_approval_date', inplace=True)

    return process_data

def preprocess_hdb_resale_data(data):
    process_data = data.copy()

    # Split 'month' column and convert to integer
    columns_name = ['transact_year', 'transact_month']
    process_data[columns_name] = process_data['month'].str.split('-', expand=True)
    process_data['transact_year'] = pd.to_numeric(process_data['transact_year'], errors='coerce')
    process_data['transact_month'] = pd.to_numeric(process_data['transact_month'], errors='coerce')
    
    # Split 'remaining_lease' column and convert to integer
    columns_name = ['lease_year', 'lease_month']
    process_data[columns_name] = process_data['remaining_lease'].str.split('years', expand=True)
    process_data['lease_month'] = process_data['lease_month'].str.replace(r'\bmonths?\b', '', regex=True)
    process_data['lease_month'] = pd.to_numeric(process_data['lease_month'], errors='coerce')
    process_data['lease_year'] = pd.to_numeric(process_data['lease_year'], errors='coerce')
    
    # Final cleanup on data type
    process_data = process_data.fillna(0)
    process_data['lease_month'] = process_data['transact_year'].astype(int)
    process_data['lease_month'] = process_data['transact_month'].astype(int)
    process_data['lease_month'] = process_data['lease_year'].astype(int)
    process_data['lease_month'] = process_data['lease_month'].astype(int)

    # Drop unnecessary columns
    process_data.drop(columns='month', inplace=True)
    process_data.drop(columns='remaining_lease', inplace=True)

    return process_data

def average_hdb_rental_data_by_year(data):
    process_data = data.copy()

    # Grouped resale price by year and town
    grouped_columns = ['approval_year', 'town']
    agg_methods = {'monthly_rent': ['mean', 'median']}
    final_data = process_data.groupby(grouped_columns).agg(agg_methods)

    # Final cleanup on grouped data
    final_data = final_data.round(2)
    final_data.columns = ['_'.join(col).strip() 
                          if isinstance(col, tuple) else col 
                          for col in final_data.columns]
    final_data = final_data.reset_index()

    return final_data

def average_hdb_resale_data_by_year(data):
    process_data = data.copy()

    # Feature engineered new resale price
    process_data['resale_per_sqm'] = process_data['resale_price'] / process_data['floor_area_sqm']
    process_data['lease_remaining'] = (process_data['lease_year'] + (process_data['lease_month'] / 12 ))
    process_data['resale_per_lease'] = process_data['resale_price'] / process_data['lease_remaining']
    process_data['resale_per_sqm_per_lease'] = process_data['resale_per_sqm'] / process_data['lease_remaining'] * 100

    # Grouped resale price by year and town
    grouped_columns = ['transact_year', 'town']
    agg_methods = {'resale_price': ['mean', 'median'], 
                   'resale_per_sqm': ['mean', 'median'],
                   'resale_per_lease': ['mean', 'median'],
                   'resale_per_sqm_per_lease': ['mean', 'median']}
    final_data = process_data.groupby(grouped_columns).agg(agg_methods)

    # Final cleanup on grouped data
    final_data = final_data.round(2)
    final_data.columns = ['_'.join(col).strip() 
                          if isinstance(col, tuple) else col 
                          for col in final_data.columns]
    final_data = final_data.reset_index()

    return final_data

def average_hdb_rental_data_by_town(data):
    process_data = data.copy()

    # Grouped resale price by year and town
    grouped_columns = ['approval_year', 'town', 'flat_type']
    agg_methods = {'monthly_rent': ['mean', 'median']}
    final_data = process_data.groupby(grouped_columns).agg(agg_methods)

    # Final cleanup on grouped data
    final_data = final_data.round(2)
    final_data.columns = ['_'.join(col).strip() 
                          if isinstance(col, tuple) else col 
                          for col in final_data.columns]
    final_data = final_data.reset_index()

    return final_data

def average_hdb_resale_data_by_town(data):
    process_data = data.copy()

    # Feature engineered new resale price
    process_data['resale_per_sqm'] = process_data['resale_price'] / process_data['floor_area_sqm']
    process_data['lease_remaining'] = (process_data['lease_year'] + (process_data['lease_month'] / 12 ))
    process_data['resale_per_lease'] = process_data['resale_price'] / process_data['lease_remaining']
    process_data['resale_per_sqm_per_lease'] = process_data['resale_per_sqm'] / process_data['lease_remaining'] * 100

    # Grouped resale price by year and town
    grouped_columns = ['transact_year', 'town', 'flat_type']
    agg_methods = {'resale_price': ['mean'], 
                   'resale_per_sqm': ['mean'],
                   'resale_per_lease': ['mean'],
                   'resale_per_sqm_per_lease': ['mean'],
                   'lease_remaining': ['mean']}
    final_data = process_data.groupby(grouped_columns).agg(agg_methods)

    # Final cleanup on grouped data
    final_data = final_data.round(2)
    final_data.columns = ['_'.join(col).strip() 
                          if isinstance(col, tuple) else col 
                          for col in final_data.columns]
    final_data = final_data.reset_index()

    return final_data