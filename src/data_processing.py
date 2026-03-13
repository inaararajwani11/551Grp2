"""
data_processing.py - Data loading with memory optimization for Render.com
"""

import pandas as pd
import os


def load_data(sample_fraction=None, random_state=42):
    """
    Load and process health survey data
    
    Parameters:
    -----------
    sample_fraction : float, optional
        Fraction of data to sample (0.1 = 10%, 1.0 = 100%)
        If None, auto-detect: Render.com uses 10%, local uses 100%
    random_state : int, default 42
        Random seed for reproducible sampling
    """
    
    # Auto-detect environment if not specified
    if sample_fraction is None:
        IS_RENDER = os.environ.get('RENDER') == 'true'
        sample_fraction = 0.1 if IS_RENDER else 1.0
    
    data_path = os.path.join('data', 'processed', 'clean_health_data.csv')
    df = pd.read_csv(data_path)
    original_size = len(df)
    
    # ========== SAMPLING FOR MEMORY OPTIMIZATION ==========
    if sample_fraction < 1.0:
        df = df.sample(frac=sample_fraction, random_state=random_state).reset_index(drop=True)
        print(f"📊 Sampled {len(df):,} records ({sample_fraction*100:.0f}%) from {original_size:,}")
    else:
        print(f"📊 Full dataset: {len(df):,} records")
    
    # ========== ENCODE NUMERIC FIELDS ==========
    
    # Age (1-5 → word)
    age_map = {
        1: '12-19', 2: '20-34', 3: '35-49', 4: '50-64', 5: '65+'
    }
    
    # Education (1-3, 9 → word)
    edu_map = {
        1: 'Less than secondary',
        2: 'Secondary graduation',
        3: 'Post-secondary',
        9: 'Not stated'
    }
    
    # Marital Status (1, 2, 6, 9 → word)
    marital_map = {
        1: 'Married/Common-law',
        2: 'Single/Never married',
        6: 'Widowed/Separated/Divorced',
        9: 'Not stated'
    }
    
    # Apply coding
    df['Age_group'] = df['Age'].map(age_map)
    df['Edu_level_text'] = df['Edu_level'].map(edu_map)
    df['Marital_status_text'] = df['Marital_status'].map(marital_map)
    
    # Unify Immigrant/Aboriginal naming
    df['Immigrant'] = df['Immigrant'].replace({'Yes': 'Immigrant', 'No': 'Non-immigrant'})
    df['Aboriginal_identity'] = df['Aboriginal_identity'].replace({'Yes': 'Aboriginal', 'No': 'Non-Aboriginal'})

    # Lifestyle binary indicators (numeric codes → Yes/No)
    df['Smoked_bin'] = df['Smoked'].apply(
        lambda x: 'Yes' if pd.notna(x) and x < 900 else ('No' if pd.notna(x) else None)
    )
    df['Cannabis_bin'] = df['Cannabies_use'].map({1: 'Yes', 2: 'No'})
    df['Drug_bin'] = df['Drug_use'].map({1: 'Yes', 2: 'No', 6: 'No'})
    
    # ========== MEMORY OPTIMIZATION ==========
    # Convert string columns to category type to save memory
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() < len(df) * 0.5:  # Only if < 50% unique values
            df[col] = df[col].astype('category')
    
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    print(f"💾 Memory usage: {memory_mb:.2f} MB")

    return df


def get_filter_options(df):
    """Get unique values for filter dropdowns"""
    
    # Helper function to extract unique values from category or object columns
    def get_unique(col):
        if col not in df.columns:
            return []
        if df[col].dtype.name == 'category':
            return [str(x) for x in df[col].cat.categories if str(x) != 'nan']
        else:
            return [str(x) for x in df[col].dropna().unique() if str(x) != 'nan']
    
    # Income order
    all_incomes = [
        'Less than $20,000', '$20,000 to $39,999', '$40,000 to $59,999',
        '$60,000 to $79,999', '$80,000 to $99,999', '$100,000 to $149,999',
        '$150,000 or more'
    ]
    actual_incomes = [i for i in all_incomes if i in get_unique('Total_income')]
    
    # Age order
    age_order = ['12-19', '20-34', '35-49', '50-64', '65+']
    actual_ages = [a for a in age_order if a in get_unique('Age_group')]
    
    # Education order
    edu_order = ['Less than secondary', 'Secondary graduation', 'Post-secondary']
    actual_edu = [e for e in edu_order if e in get_unique('Edu_level_text')]
    
    # Marital order
    marital_order = ['Married/Common-law', 'Single/Never married', 'Widowed/Separated/Divorced']
    actual_marital = [m for m in marital_order if m in get_unique('Marital_status_text')]
    
    return {
        'provinces': ['All'] + sorted(get_unique('Province')),
        'age_groups': ['All'] + actual_ages,
        'genders': ['All'] + sorted(get_unique('Gender')),
        'educations': ['All'] + actual_edu,
        'maritals': ['All'] + actual_marital,
        'incomes': ['All'] + actual_incomes,
        'immigrant': ['All'] + sorted(get_unique('Immigrant')),
        'aboriginal': ['All'] + sorted(get_unique('Aboriginal_identity')),
        
        'health_focus': ['Physical Health', 'Mental Health', 'Lifestyle Behaviors'],
        'compare_by': ['Income', 'Education', 'Age', 'Gender']
    }
