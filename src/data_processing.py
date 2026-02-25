import pandas as pd
import os

def load_data():
    """Load and return cleaned health survey data"""
    # current directory
    current_dir = os.path.dirname(__file__)
    # data/raw
    data_path = os.path.join(current_dir, '..', 'data', 'raw', 'health_dataset.csv')
    
    # Load the dataset
    df = pd.read_csv(data_path)
    
    # Basic cleaning - remove rows with missing values
    df = df.dropna(subset=[
        'Province', 
        'Gender', 
        'Age', 
        'Gen_health_state',
        'Total_income'
    ])
    
    # Save processed data
    processed_path = os.path.join(current_dir, '..', 'data', 'processed', 'clean_health_data.csv')
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)
    
    return df

def get_filter_options(df):
    """Get unique values for filter dropdowns"""
    return {
        'provinces': sorted(df['Province'].dropna().unique().tolist()),
        'genders': sorted(df['Gender'].dropna().unique().tolist()),
        'incomes': sorted(df['Total_income'].dropna().unique().tolist()),
        'education': sorted(df['Edu_level'].dropna().unique().tolist())
    }

if __name__ == '__main__':
    # Test data loading
    print("Loading data...")
    df = load_data()
    print(f"✅ Data loaded successfully! {len(df)} records")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData shape: {df.shape}")
    
    # Show filter options
    options = get_filter_options(df)
    print(f"\n📊 Filter Options:")
    print(f"Provinces: {options['provinces']}")
    print(f"Genders: {options['genders']}")
    print(f"Income levels: {len(options['incomes'])} unique values")