import pandas as pd
import os

# Encoding mappings for categorical variables
PROVINCE_MAP = {
    10: 'Newfoundland and Labrador',
    11: 'Prince Edward Island',
    12: 'Nova Scotia',
    13: 'New Brunswick',
    24: 'Quebec',
    35: 'Ontario',
    46: 'Manitoba',
    47: 'Saskatchewan',
    48: 'Alberta',
    59: 'British Columbia',
    60: 'Yukon',
    61: 'Northwest Territories',
    62: 'Nunavut'
}

GENDER_MAP = {
    1: 'Male',
    2: 'Female'
}

GEN_HEALTH_MAP = {
    1: 'Excellent',
    2: 'Very good',
    3: 'Good',
    4: 'Fair',
    5: 'Poor'
}

MENTAL_HEALTH_MAP = {
    1: 'Excellent',
    2: 'Very good',
    3: 'Good',
    4: 'Fair',
    5: 'Poor'
}

STRESS_LEVEL_MAP = {
    1: 'Not at all stressful',
    2: 'Not very stressful',
    3: 'A bit stressful',
    4: 'Quite a bit stressful',
    5: 'Extremely stressful'
}

INCOME_MAP = {
    1: 'Less than $20,000',
    2: '$20,000 to $39,999',
    3: '$40,000 to $59,999',
    4: '$60,000 to $79,999',
    5: '$80,000 to $99,999',
    6: '$100,000 to $149,999',
    7: '$150,000 or more'
}

IMMIGRANT_MAP = {
    1: 'Yes',
    2: 'No'
}

ABORIGINAL_MAP = {
    1: 'Yes',
    2: 'No'
}

YES_NO_MAP = {
    1: 'Yes',
    2: 'No'
}

FOOD_SECURITY_MAP = {
    1: 'Food secure',
    2: 'Moderately food insecure',
    3: 'Severely food insecure'
}

SENSE_BELONGING_MAP = {
    1: 'Very strong',
    2: 'Somewhat strong',
    3: 'Somewhat weak',
    4: 'Very weak'
}

WORK_STRESS_MAP = {
    1: 'Not at all stressful',
    2: 'Not very stressful',
    3: 'A bit stressful',
    4: 'Quite a bit stressful',
    5: 'Extremely stressful'
}


def load_data():
    """Load and return cleaned health survey data with decoded labels"""
    # Get current directory
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, '..', 'data', 'raw', 'health_dataset.csv')

    # Load the dataset
    df = pd.read_csv(data_path)

    # ------------------------------------------------------------------
    # Ensure Health_utility_index exists (rename from raw column if needed)
    # ------------------------------------------------------------------
    if 'Health_utility_index' not in df.columns:
        # Common candidate names in raw health datasets
        candidates = [
            'Health_utility_indx',
            'HUI', 'hui', 'HUI_index', 'hui_index',
            'HUI3', 'hui3',
            'Health_utility', 'health_utility',
            'HealthUtilityIndex', 'healthutilityindex',
            'Health_Utility_Index', 'health_utility_index',
            'Health utility index', 'health utility index',
            'Utility_index', 'utility_index',
        ]
        found = next((c for c in candidates if c in df.columns), None)

        if found is not None:
            df = df.rename(columns={found: 'Health_utility_index'})
        else:
            # Create the column as missing to avoid KeyError downstream.
            # Charts that require it will drop NA rows automatically.
            df['Health_utility_index'] = pd.NA

    # Apply mappings to convert codes to labels
    if 'Province' in df.columns:
        df['Province'] = df['Province'].map(PROVINCE_MAP)

    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].map(GENDER_MAP)

    if 'Gen_health_state' in df.columns:
        df['Gen_health_state'] = df['Gen_health_state'].map(GEN_HEALTH_MAP)

    if 'Mental_health_state' in df.columns:
        df['Mental_health_state'] = df['Mental_health_state'].map(MENTAL_HEALTH_MAP)

    if 'Stress_level' in df.columns:
        df['Stress_level'] = df['Stress_level'].map(STRESS_LEVEL_MAP)

    if 'Total_income' in df.columns:
        df['Total_income'] = df['Total_income'].map(INCOME_MAP)

    if 'Immigrant' in df.columns:
        df['Immigrant'] = df['Immigrant'].map(IMMIGRANT_MAP)

    if 'Aboriginal_identity' in df.columns:
        df['Aboriginal_identity'] = df['Aboriginal_identity'].map(ABORIGINAL_MAP)

    if 'Food_security' in df.columns:
        df['Food_security'] = df['Food_security'].map(FOOD_SECURITY_MAP)

    if 'Sense_belonging' in df.columns:
        df['Sense_belonging'] = df['Sense_belonging'].map(SENSE_BELONGING_MAP)

    if 'Work_stress' in df.columns:
        df['Work_stress'] = df['Work_stress'].map(WORK_STRESS_MAP)

    # Map Yes/No fields
    yes_no_fields = [
        'Sleep_apnea', 'High_BP', 'High_cholesterol', 'Diabetic',
        'Fatigue_syndrome', 'Mood_disorder', 'Anxiety_disorder',
        'Respiratory_chronic_con', 'Musculoskeletal_con', 'Cardiovascular_con'
    ]

    for field in yes_no_fields:
        if field in df.columns:
            df[field] = df[field].map(YES_NO_MAP)

    # Basic cleaning - keep only essential filters non-null
    df = df.dropna(subset=['Province', 'Gender', 'Gen_health_state'])

    # Save processed data
    processed_path = os.path.join(current_dir, '..', 'data', 'processed', 'clean_health_data.csv')
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)

    return df


def get_filter_options(df):
    """Get unique values for filter dropdowns"""
    options = {}

    if 'Province' in df.columns:
        options['provinces'] = ['All'] + sorted([x for x in df['Province'].dropna().unique().tolist() if pd.notna(x)])

    if 'Gender' in df.columns:
        options['genders'] = ['All'] + sorted([x for x in df['Gender'].dropna().unique().tolist() if pd.notna(x)])

    if 'Total_income' in df.columns:
        # Keep income in logical order
        income_order = [
            'Less than $20,000',
            '$20,000 to $39,999',
            '$40,000 to $59,999',
            '$60,000 to $79,999',
            '$80,000 to $99,999',
            '$100,000 to $149,999',
            '$150,000 or more'
        ]
        available_incomes = [x for x in income_order if x in df['Total_income'].values]
        options['incomes'] = ['All'] + available_incomes

    if 'Immigrant' in df.columns:
        options['immigrant'] = ['All'] + sorted([x for x in df['Immigrant'].dropna().unique().tolist() if pd.notna(x)])

    if 'Aboriginal_identity' in df.columns:
        options['aboriginal'] = ['All'] + sorted([x for x in df['Aboriginal_identity'].dropna().unique().tolist() if pd.notna(x)])

    # Age range
    if 'Age' in df.columns:
        age_values = df['Age'].dropna()
        if len(age_values) > 0:
            options['age_min'] = int(age_values.min())
            options['age_max'] = int(age_values.max())
        else:
            options['age_min'] = 12
            options['age_max'] = 80

    # Outcome variables
    options['outcome_vars'] = [
        'Gen_health_state',
        'Mental_health_state',
        'Stress_level',
        'Health_utility_index',
        'Life_satisfaction'
    ]

    # Behavior variables
    options['behavior_vars'] = [
        'Total_physical_act_time',
        'Physical_vigorous_act_time',
        'Fruit_veg_con',
        'Work_hours'
    ]

    return options


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
    print(f"Immigrant: {options.get('immigrant', 'N/A')}")
    print(f"Aboriginal: {options.get('aboriginal', 'N/A')}")
    print(f"Age range: {options.get('age_min', 'N/A')} - {options.get('age_max', 'N/A')}")