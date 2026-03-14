"""
data_processing.py - Data loading (適配已編碼的資料)
"""

import pandas as pd
import os


def load_data():
    """Load and process health survey data.

    Reads the raw CSV from data/processed/clean_health_data.csv, decodes
    numeric codes into human-readable text labels, and derives binary
    indicator columns for lifestyle behaviours.

    Returns:
        pd.DataFrame: Processed survey DataFrame with added text columns
            (Age_group, Edu_level_text, Marital_status_text, Smoked_bin,
            Cannabis_bin, Drug_bin) and normalised Immigrant /
            Aboriginal_identity labels.
    """
    
    data_path = os.path.join('data', 'processed', 'clean_health_data.csv')
    df = pd.read_csv(data_path)
    
    # ========== 只編碼數字欄位 ==========
    
    # Age (1-5 → 文字)
    age_map = {
        1: '12-19', 2: '20-34', 3: '35-49', 4: '50-64', 5: '65+'
    }
    
    # Education (1-3, 9 → 文字)
    edu_map = {
        1: 'Less than secondary',
        2: 'Secondary graduation',
        3: 'Post-secondary',
        9: 'Not stated'
    }
    
    # Marital Status (1, 2, 6, 9 → 文字)
    marital_map = {
        1: 'Married/Common-law',
        2: 'Single/Never married',
        6: 'Widowed/Separated/Divorced',
        9: 'Not stated'
    }
    
    # 套用編碼
    df['Age_group'] = df['Age'].map(age_map)
    df['Edu_level_text'] = df['Edu_level'].map(edu_map)
    df['Marital_status_text'] = df['Marital_status'].map(marital_map)
    
    # 統一 Immigrant/Aboriginal 命名
    df['Immigrant'] = df['Immigrant'].replace({'Yes': 'Immigrant', 'No': 'Non-immigrant'})
    df['Aboriginal_identity'] = df['Aboriginal_identity'].replace({'Yes': 'Aboriginal', 'No': 'Non-Aboriginal'})

    # Lifestyle binary indicators (numeric codes → Yes/No)
    # Smoked: values <900 = currently smokes; 996/999 = non-smoker or not stated
    df['Smoked_bin'] = df['Smoked'].apply(
        lambda x: 'Yes' if pd.notna(x) and x < 900 else ('No' if pd.notna(x) else None)
    )
    # Cannabies_use: 1=Yes, 2=No, 9=not applicable
    df['Cannabis_bin'] = df['Cannabies_use'].map({1: 'Yes', 2: 'No'})
    # Drug_use: 1=Yes (used in past year), 2/6=No, 9=not applicable
    df['Drug_bin'] = df['Drug_use'].map({1: 'Yes', 2: 'No', 6: 'No'})

    return df


def get_filter_options(df):
    """Get unique values for filter dropdowns.

    Extracts and orders the distinct category values for each sidebar
    filter from the processed DataFrame, prepending 'All' to each list.

    Args:
        df (pd.DataFrame): Processed survey DataFrame returned by load_data().

    Returns:
        dict: Mapping of filter name to ordered list of option strings.
            Keys: 'provinces', 'age_groups', 'genders', 'educations',
            'maritals', 'incomes', 'immigrant', 'aboriginal',
            'health_focus', 'compare_by'.
    """
    
    # 定義順序（只保留資料中實際存在的）
    all_incomes = [
        'Less than $20,000', '$20,000 to $39,999', '$40,000 to $59,999',
        '$60,000 to $79,999', '$80,000 to $99,999', '$100,000 to $149,999',
        '$150,000 or more'
    ]
    actual_incomes = [i for i in all_incomes if i in df['Total_income'].unique()]
    
    age_order = ['12-19', '20-34', '35-49', '50-64', '65+']
    actual_ages = [a for a in age_order if a in df['Age_group'].dropna().unique()]
    
    edu_order = ['Less than secondary', 'Secondary graduation', 'Post-secondary']
    actual_edu = [e for e in edu_order if e in df['Edu_level_text'].dropna().unique()]
    
    marital_order = ['Married/Common-law', 'Single/Never married', 'Widowed/Separated/Divorced']
    actual_marital = [m for m in marital_order if m in df['Marital_status_text'].dropna().unique()]
    
    return {
        'provinces': ['All'] + sorted([p for p in df['Province'].dropna().unique() if p and str(p) != 'nan']),
        'age_groups': ['All'] + actual_ages,
        'genders': ['All'] + sorted([g for g in df['Gender'].dropna().unique() if g and str(g) != 'nan']),
        'educations': ['All'] + actual_edu,
        'maritals': ['All'] + actual_marital,
        'incomes': ['All'] + actual_incomes,
        'immigrant': ['All'] + sorted([i for i in df['Immigrant'].dropna().unique() if i and str(i) != 'nan']),
        'aboriginal': ['All'] + sorted([a for a in df['Aboriginal_identity'].dropna().unique() if a and str(a) != 'nan']),
        
        'health_focus': ['Physical Health', 'Mental Health', 'Lifestyle Behaviors'],
        'compare_by': ['Income', 'Education', 'Age', 'Gender']
    }
