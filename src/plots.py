"""
plots.py - Complete chart functions with dual toggle support
All 6 charts respond to Health Focus and Compare By toggles
"""

import altair as alt
import pandas as pd

# ========== UNIFIED COLOR PALETTE ==========
# Single qualitative palette used across all categorical color encodings
QUAL_PALETTE = [
    '#3b82f6',  # blue
    '#f97316',  # orange
    '#a855f7',  # purple
    '#22c55e',  # green
    '#ef4444',  # red
    '#eab308',  # yellow
    '#06b6d4',  # cyan
]

# ========== HELPER FUNCTIONS ==========

def get_compare_column(compare_by):
    """Get the actual column name for compare_by"""
    mapping = {
        'Income': 'Total_income',
        'Education': 'Edu_level_text',  # 修正：使用 _text 版本
        'Age': 'Age_group',
        'Gender': 'Gender'
    }
    return mapping.get(compare_by, 'Total_income')


def get_compare_order(compare_by):
    """Get the sort order for compare_by variable"""
    orders = {
        'Income': ['Less than $20,000', '$20,000 to $39,999', '$40,000 to $59,999',
                  '$60,000 to $79,999', '$80,000 to $99,999', '$100,000 to $149,999', '$150,000 or more'],
        'Education': ['Less than secondary', 'Secondary graduation', 'Post-secondary'],
        'Age': ['12-19', '20-34', '35-49', '50-64', '65+'],
        'Gender': ['Male', 'Female']
    }
    return orders.get(compare_by, None)


# ========== CHART 1: Main Health Indicator Distribution ==========

def create_chart1(df, health_focus='Physical Health', compare_by='Income'):
    """Chart 1: Health indicator distribution - stacked bar chart"""
    
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    # Select outcome variable based on health_focus
    if health_focus == 'Physical Health':
        outcome_var = 'Gen_health_state'
        title = 'General Health Status'
        sort_order = ['Excellent', 'Very good', 'Good', 'Fair', 'Poor']
    elif health_focus == 'Mental Health':
        outcome_var = 'Mental_health_state'
        title = 'Mental Health Status'
        sort_order = ['Excellent', 'Very good', 'Good', 'Fair', 'Poor']
    else:  # Lifestyle Behaviors
        outcome_var = 'Life_satisfaction'
        title = 'Life Satisfaction Level'
        sort_order = None
    
    compare_col = get_compare_column(compare_by)
    compare_order = get_compare_order(compare_by)
    
    if outcome_var not in df.columns or compare_col not in df.columns:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
    
    # For Life_satisfaction, create categories
    if outcome_var == 'Life_satisfaction':
        chart_df = df[(df[outcome_var].notna()) & (df[outcome_var] < 90) & (df[compare_col].notna())].copy()
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No valid data"}}}
        chart_df['satisfaction_level'] = pd.cut(chart_df[outcome_var], 
                                               bins=[-0.1, 3, 6, 10],
                                               labels=['Low (0-3)', 'Medium (4-6)', 'High (7-10)'])
        outcome_var = 'satisfaction_level'
        sort_order = ['Low (0-3)', 'Medium (4-6)', 'High (7-10)']
    else:
        chart_df = df.dropna(subset=[outcome_var, compare_col])
    
    if len(chart_df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    agg_df = chart_df.groupby([outcome_var, compare_col]).size().reset_index(name='count')
    
    chart = alt.Chart(agg_df).mark_bar().encode(
        x=alt.X(f'{outcome_var}:N', title=None, sort=sort_order,
                axis=alt.Axis(labelAngle=-30, labelLimit=100, labelFontSize=9)),
        y=alt.Y('count:Q', title='Count', stack='zero',
                axis=alt.Axis(titleFontSize=10, labelFontSize=9)),
        color=alt.Color(f'{compare_col}:N', title=compare_by, sort=compare_order,
                       scale=alt.Scale(range=QUAL_PALETTE),
                       legend=alt.Legend(orient='right', titleFontSize=9, labelFontSize=8, labelLimit=100)),
        tooltip=[alt.Tooltip(f'{outcome_var}:N', title=title),
                 alt.Tooltip(f'{compare_col}:N', title=compare_by),
                 alt.Tooltip('count:Q', title='Count', format=',')]
    ).properties(
        width='container', height='container',
        title=alt.TitleParams(text=title, subtitle=f'Stacked by {compare_by}',
                              fontSize=11, subtitleFontSize=9, subtitleColor='#666', anchor='start', dx=12)
    ).configure_view(strokeWidth=0)

    return chart.to_dict()


# ========== CHART 2: Two-Variable Relationship ==========

def create_chart2(df, health_focus='Physical Health', compare_by='Income'):
    """Chart 2: Relationship between two health variables"""
    
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    compare_col = get_compare_column(compare_by)
    compare_order = get_compare_order(compare_by)
    
    if health_focus == 'Physical Health':
        # Grouped bar: Health status by compare_by
        y_var = 'Gen_health_state'
        title = 'Health Status Distribution'
        y_order = ['Excellent', 'Very good', 'Good', 'Fair', 'Poor']
        
        chart_df = df.dropna(subset=[y_var, compare_col])
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
        
        agg_df = chart_df.groupby([y_var, compare_col]).size().reset_index(name='count')
        
        chart = alt.Chart(agg_df).mark_bar().encode(
            x=alt.X(f'{y_var}:N', title=None, sort=y_order,
                   axis=alt.Axis(labelAngle=-30, labelFontSize=9)),
            y=alt.Y('count:Q', title='Count', axis=alt.Axis(labelFontSize=9)),
            color=alt.Color(f'{compare_col}:N', title=compare_by, sort=compare_order,
                           scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=8, titleFontSize=9)),
            xOffset=alt.XOffset(f'{compare_col}:N'),
            tooltip=[alt.Tooltip(f'{y_var}:N'), alt.Tooltip(f'{compare_col}:N'),
                    alt.Tooltip('count:Q', format=',')]
        )

    elif health_focus == 'Mental Health':
        # Stress level distribution
        x_var = 'Stress_level'
        title = 'Stress Level Distribution'
        x_order = ['Not at all stressful', 'Not very stressful', 'A bit stressful',
                  'Quite a bit stressful', 'Extremely stressful']
        
        chart_df = df.dropna(subset=[x_var, compare_col])
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
        
        agg_df = chart_df.groupby([x_var, compare_col]).size().reset_index(name='count')
        
        chart = alt.Chart(agg_df).mark_bar().encode(
            x=alt.X(f'{x_var}:N', title=None, sort=x_order,
                   axis=alt.Axis(labelAngle=-30, labelFontSize=8, labelLimit=60)),
            y=alt.Y('count:Q', title='Count', axis=alt.Axis(labelFontSize=9)),
            color=alt.Color(f'{compare_col}:N', title=compare_by, sort=compare_order,
                           scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=8, titleFontSize=9)),
            xOffset=alt.XOffset(f'{compare_col}:N'),
            tooltip=[alt.Tooltip(f'{x_var}:N'), alt.Tooltip(f'{compare_col}:N'),
                    alt.Tooltip('count:Q', format=',')]
        )

    else:  # Lifestyle - Diet scatter
        x_var = 'Fruit_veg_con'
        y_var = 'Life_satisfaction'
        title = 'Diet vs Life Satisfaction'
        
        chart_df = df[(df[x_var].notna()) & (df[x_var] < 9000) &
                     (df[y_var].notna()) & (df[y_var] < 90) &
                     (df[compare_col].notna())].copy()
        if len(chart_df) < 10:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Insufficient data"}}}
        
        if len(chart_df) > 2000:
            chart_df = chart_df.sample(n=2000, random_state=42)
        
        chart = alt.Chart(chart_df).mark_circle(size=20, opacity=0.4).encode(
            x=alt.X(f'{x_var}:Q', title='Fruit & Veg (servings/day)', 
                   scale=alt.Scale(zero=True), axis=alt.Axis(labelFontSize=9)),
            y=alt.Y(f'{y_var}:Q', title='Life Satisfaction', 
                   scale=alt.Scale(zero=True, domain=[0, 10]), axis=alt.Axis(labelFontSize=9)),
            color=alt.Color(f'{compare_col}:N', title=compare_by, sort=compare_order,
                           scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=8)),
            tooltip=[alt.Tooltip(f'{x_var}:Q', format='.1f'),
                    alt.Tooltip(f'{y_var}:Q', format='.1f'),
                    alt.Tooltip(f'{compare_col}:N')]
        )
    
    chart = chart.properties(
        width='container', height='container',
        title=alt.TitleParams(text=title, subtitle=f'Compared by {compare_by}',
                              fontSize=11, subtitleFontSize=9, subtitleColor='#666', anchor='start', dx=12)
    ).configure_view(strokeWidth=0)

    return chart.to_dict()


# ========== CHART 3: Heatmap ==========

def create_chart3(df, health_focus='Physical Health', compare_by='Income'):
    """Chart 3: Condition prevalence heatmap"""
    
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    compare_col = get_compare_column(compare_by)
    
    if health_focus == 'Physical Health':
        conditions = ['High_BP', 'Diabetic', 'Cardiovascular_con']
        title = 'Chronic Condition Prevalence'
    elif health_focus == 'Mental Health':
        conditions = ['Mood_disorder', 'Anxiety_disorder']
        title = 'Mental Health Condition Prevalence'
    else:  # Lifestyle
        conditions = ['Smoked_bin', 'Cannabis_bin', 'Drug_bin']
        title = 'Substance Use Prevalence'
    
    available = [c for c in conditions if c in df.columns]
    if not available or compare_col not in df.columns:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
    
    data_list = []
    for cond in available:
        for compare_val in df[compare_col].dropna().unique():
            subset = df[(df[compare_col] == compare_val) & (df[cond].notna())]
            if len(subset) > 0:
                prevalence = (subset[cond] == 'Yes').sum() / len(subset) * 100
                cond_short = cond.replace('_disorder', '').replace('_con', '').replace('_bin', '').replace('_', ' ').title()
                data_list.append({'Condition': cond_short, 'Group': compare_val, 'Prevalence': prevalence})
    
    if not data_list:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    heatmap_df = pd.DataFrame(data_list)
    
    base = alt.Chart(heatmap_df)

    rect = base.mark_rect().encode(
        x=alt.X('Condition:N', title='Condition', axis=alt.Axis(labelAngle=-30, labelLimit=80, labelFontSize=9)),
        y=alt.Y('Group:N', title=compare_by, axis=alt.Axis(labelLimit=120, labelFontSize=8)),
        color=alt.Color('Prevalence:Q', title='Prevalence %', scale=alt.Scale(scheme='reds'),
                       legend=alt.Legend(orient='right', titleFontSize=9, labelFontSize=8)),
        tooltip=[alt.Tooltip('Condition:N'), alt.Tooltip('Group:N', title=compare_by),
                 alt.Tooltip('Prevalence:Q', format='.1f', title='Prevalence %')]
    )

    text = base.mark_text(fontSize=9, fontWeight='bold').encode(
        x=alt.X('Condition:N'),
        y=alt.Y('Group:N'),
        text=alt.Text('Prevalence:Q', format='.1f'),
        color=alt.condition(
            alt.datum.Prevalence > 30,
            alt.value('white'),
            alt.value('#333')
        )
    )

    chart = (rect + text).properties(
        width='container', height='container',
        title=alt.TitleParams(text=title, subtitle=f'Grouped by {compare_by} · Prevalence (%) in each cell',
                              fontSize=11, subtitleFontSize=9, subtitleColor='#666', anchor='start', dx=12)
    ).configure_view(strokeWidth=0)

    return chart.to_dict()


# ========== CHART 4: Grouped Comparison ==========

def create_chart4(df, health_focus='Physical Health', compare_by='Income'):
    """Chart 4: Grouped comparison bar chart"""
    
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    compare_col = get_compare_column(compare_by)
    
    if health_focus == 'Physical Health':
        # Food Security × Immigration
        x_var = 'Food_security'
        color_var = 'Immigrant'
        title = 'Food Security × Immigration'
        
        required = [x_var, color_var]
        if not all(c in df.columns for c in required):
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        chart_df = df.dropna(subset=required)
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
        
        agg_df = chart_df.groupby([x_var, color_var]).size().reset_index(name='count')
        
        chart = alt.Chart(agg_df).mark_bar().encode(
            x=alt.X(f'{x_var}:N', title=None, axis=alt.Axis(labelAngle=-30, labelFontSize=9, labelLimit=80)),
            y=alt.Y('count:Q', title='Count', axis=alt.Axis(labelFontSize=9, titleFontSize=10)),
            color=alt.Color(f'{color_var}:N', title='Status', scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=8, titleFontSize=9)),
            tooltip=[alt.Tooltip(f'{x_var}:N'), alt.Tooltip(f'{color_var}:N'), alt.Tooltip('count:Q', format=',')]
        )
    
    elif health_focus == 'Mental Health':
        # Food Security × Sense of Belonging
        x_var = 'Food_security'
        color_var = 'Sense_belonging'
        title = 'Food Security × Sense of Belonging'
        
        required = [x_var, color_var]
        if not all(c in df.columns for c in required):
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        chart_df = df.dropna(subset=required)
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
        
        agg_df = chart_df.groupby([x_var, color_var]).size().reset_index(name='count')
        
        chart = alt.Chart(agg_df).mark_bar().encode(
            x=alt.X(f'{x_var}:N', title=None, axis=alt.Axis(labelAngle=-30, labelFontSize=9, labelLimit=60)),
            y=alt.Y('count:Q', title='Count', axis=alt.Axis(labelFontSize=9)),
            color=alt.Color(f'{color_var}:N', title='Belonging', scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=7, titleFontSize=9, labelLimit=80)),
            tooltip=[alt.Tooltip(f'{x_var}:N'), alt.Tooltip(f'{color_var}:N'), alt.Tooltip('count:Q', format=',')]
        )
    
    else:  # Lifestyle - Physical activity levels
        x_var = 'Total_physical_act_time'
        title = 'Physical Activity Levels'
        
        if x_var not in df.columns or compare_col not in df.columns:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        chart_df = df[(df[x_var].notna()) & (df[x_var] < 9000) & (df[compare_col].notna())].copy()
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No valid data"}}}
        
        chart_df['activity_level'] = pd.cut(chart_df[x_var], 
                                            bins=[-0.1, 150, 300, 10000],
                                            labels=['Low (<150min)', 'Moderate (150-300min)', 'High (>300min)'])
        
        agg_df = chart_df.groupby(['activity_level', compare_col]).size().reset_index(name='count')
        
        chart = alt.Chart(agg_df).mark_bar().encode(
            x=alt.X('activity_level:N', title='Activity Level', 
                   axis=alt.Axis(labelAngle=-20, labelFontSize=9)),
            y=alt.Y('count:Q', title='Count', axis=alt.Axis(labelFontSize=9)),
            color=alt.Color(f'{compare_col}:N', title=compare_by, scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=8, titleFontSize=9)),
            xOffset=alt.XOffset(f'{compare_col}:N'),
            tooltip=[alt.Tooltip('activity_level:N'), alt.Tooltip(f'{compare_col}:N'),
                    alt.Tooltip('count:Q', format=',')]
        )
    
    chart4_subtitle = f'Colored by {compare_by}' if health_focus == 'Lifestyle Behaviors' else 'Cross-factor comparison'
    chart = chart.properties(
        width='container', height='container',
        title=alt.TitleParams(text=title, subtitle=chart4_subtitle,
                              fontSize=11, subtitleFontSize=9, subtitleColor='#666', anchor='start', dx=12)
    ).configure_view(strokeWidth=0)

    return chart.to_dict()


# ========== CHART 5: Bubble/Relationship Chart ==========

def create_chart5(df, health_focus='Physical Health', compare_by='Income'):
    """Chart 5: Bubble or relationship chart"""
    
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    compare_col = get_compare_column(compare_by)
    
    if health_focus == 'Physical Health':
        # Physical activity × Age group (bubble)
        x_var = 'Age_group'
        y_var = 'Total_physical_act_time'
        title = 'Physical Activity by Age'
        
        if y_var not in df.columns or 'Age_group' not in df.columns or compare_col not in df.columns:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        chart_df = df[(df[y_var].notna()) & (df[y_var] < 9000) & 
                     (df['Age_group'].notna()) & (df[compare_col].notna())].copy()
        
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No valid data"}}}
        
        # When compare_by is Age, avoid duplicate groupby on same column
        same_as_x = (compare_col == 'Age_group')
        group_cols = ['Age_group'] if same_as_x else ['Age_group', compare_col]
        agg_df = chart_df.groupby(group_cols)[y_var].mean().reset_index(name='avg_activity')
        agg_df['count'] = chart_df.groupby(group_cols).size().values
        if same_as_x:
            agg_df[compare_col] = agg_df['Age_group']

        age_order = ['12-19', '20-34', '35-49', '50-64', '65+']

        chart = alt.Chart(agg_df).mark_circle(opacity=0.7).encode(
            x=alt.X('Age_group:N', title='Age Group', sort=age_order,
                   axis=alt.Axis(labelAngle=0, labelFontSize=9)),
            y=alt.Y('avg_activity:Q', title='Avg Physical Activity (min/week)',
                   axis=alt.Axis(labelFontSize=9)),
            size=alt.Size('count:Q', title='Sample Size', scale=alt.Scale(range=[100, 800]),
                         legend=alt.Legend(orient='right', labelFontSize=8)),
            color=alt.Color(f'{compare_col}:N', title=compare_by, scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=8)),
            tooltip=[alt.Tooltip('Age_group:N'), alt.Tooltip(f'{compare_col}:N'),
                    alt.Tooltip('avg_activity:Q', format='.0f', title='Avg Activity'),
                    alt.Tooltip('count:Q', format=',')]
        )
    
    elif health_focus == 'Mental Health':
        # Work stress × Life satisfaction
        x_var = 'Work_stress'
        y_var = 'Life_satisfaction'
        title = 'Work Stress vs Life Satisfaction'
        
        required = [x_var, y_var, compare_col]
        if not all(c in df.columns for c in required):
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        chart_df = df[(df[x_var].notna()) & (df[y_var].notna()) & 
                     (df[y_var] < 90) & (df[compare_col].notna())].copy()
        
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No valid data"}}}
        
        agg_df = chart_df.groupby([x_var, compare_col])[y_var].mean().reset_index(name='avg_satisfaction')
        agg_df['count'] = chart_df.groupby([x_var, compare_col]).size().values
        agg_df = agg_df[agg_df['count'] >= 5]
        
        if len(agg_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Insufficient data"}}}
        
        chart = alt.Chart(agg_df).mark_circle(opacity=0.7).encode(
            x=alt.X(f'{x_var}:N', title='Work Stress', 
                   axis=alt.Axis(labelAngle=-30, labelFontSize=8, labelLimit=60)),
            y=alt.Y('avg_satisfaction:Q', title='Avg Life Satisfaction',
                   scale=alt.Scale(domain=[0, 10]), axis=alt.Axis(labelFontSize=9)),
            size=alt.Size('count:Q', title='Sample Size', scale=alt.Scale(range=[100, 800]),
                         legend=alt.Legend(orient='right', labelFontSize=8)),
            color=alt.Color(f'{compare_col}:N', title=compare_by, scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=8)),
            tooltip=[alt.Tooltip(f'{x_var}:N'), alt.Tooltip(f'{compare_col}:N'),
                    alt.Tooltip('avg_satisfaction:Q', format='.2f', title='Avg Satisfaction'),
                    alt.Tooltip('count:Q', format=',')]
        )
    
    else:  # Lifestyle - Work hours × Alcohol
        x_var = 'Work_hours'
        y_var = 'weekly_alcohol'
        title = 'Work Hours vs Alcohol Consumption'
        
        # Strip spaces from Work_hours column name
        x_var_actual = 'Work_hours '  # Original has space
        
        if x_var_actual not in df.columns or y_var not in df.columns or compare_col not in df.columns:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        chart_df = df[(df[x_var_actual].notna()) & (df[x_var_actual] < 90) &
                     (df[y_var].notna()) & (df[y_var] < 900) &
                     (df[compare_col].notna())].copy()
        
        if len(chart_df) == 0:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No valid data"}}}
        
        # Create bins
        chart_df['work_hours_bin'] = pd.cut(chart_df[x_var_actual],
                                            bins=[-0.1, 20, 40, 100],
                                            labels=['Part-time (<20h)', 'Full-time (20-40h)', 'Overtime (>40h)'])
        
        agg_df = chart_df.groupby(['work_hours_bin', compare_col])[y_var].mean().reset_index(name='avg_alcohol')
        agg_df['count'] = chart_df.groupby(['work_hours_bin', compare_col]).size().values
        
        chart = alt.Chart(agg_df).mark_circle(opacity=0.7).encode(
            x=alt.X('work_hours_bin:N', title='Work Hours',
                   axis=alt.Axis(labelAngle=-20, labelFontSize=9)),
            y=alt.Y('avg_alcohol:Q', title='Avg Alcohol (drinks/week)',
                   axis=alt.Axis(labelFontSize=9)),
            size=alt.Size('count:Q', title='Sample Size', scale=alt.Scale(range=[100, 800]),
                         legend=alt.Legend(orient='right', labelFontSize=8)),
            color=alt.Color(f'{compare_col}:N', title=compare_by, scale=alt.Scale(range=QUAL_PALETTE),
                           legend=alt.Legend(orient='right', labelFontSize=8)),
            tooltip=[alt.Tooltip('work_hours_bin:N'), alt.Tooltip(f'{compare_col}:N'),
                    alt.Tooltip('avg_alcohol:Q', format='.1f', title='Avg Alcohol'),
                    alt.Tooltip('count:Q', format=',')]
        )
    
    chart = chart.properties(
        width='container', height='container',
        title=alt.TitleParams(text=title, subtitle=f'Bubble size = sample count · Color = {compare_by}',
                              fontSize=11, subtitleFontSize=9, subtitleColor='#666', anchor='start', dx=12)
    ).configure_view(strokeWidth=0)

    return chart.to_dict()


# ========== CHART 6: Provincial Risk Ranking ==========

def create_chart6(df, health_focus='Physical Health', compare_by='Income'):
    """Chart 6: Provincial health risk ranking"""
    
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    if 'Province' not in df.columns:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Province data unavailable"}}}
    
    risk_data = []
    
    if health_focus == 'Physical Health':
        # % Fair/Poor general health
        outcome_var = 'Gen_health_state'
        risk_categories = ['Fair', 'Poor']
        title = 'Provincial Physical Health Risk'
        subtitle = '% Fair/Poor Health'
        
        if outcome_var not in df.columns:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        for province in df['Province'].dropna().unique():
            prov_df = df[(df['Province'] == province) & (df[outcome_var].notna())]
            if len(prov_df) > 0:
                risk_pct = (prov_df[outcome_var].isin(risk_categories)).sum() / len(prov_df) * 100
                risk_data.append({'Province': province, 'Risk_Score': risk_pct})
    
    elif health_focus == 'Mental Health':
        # % High stress
        outcome_var = 'Stress_level'
        risk_categories = ['Quite a bit stressful', 'Extremely stressful']
        title = 'Provincial Mental Health Risk'
        subtitle = '% High Stress'
        
        if outcome_var not in df.columns:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        for province in df['Province'].dropna().unique():
            prov_df = df[(df['Province'] == province) & (df[outcome_var].notna())]
            if len(prov_df) > 0:
                risk_pct = (prov_df[outcome_var].isin(risk_categories)).sum() / len(prov_df) * 100
                risk_data.append({'Province': province, 'Risk_Score': risk_pct})
    
    else:  # Lifestyle
        # % Low life satisfaction
        outcome_var = 'Life_satisfaction'
        title = 'Provincial Lifestyle Risk'
        subtitle = '% Low Life Satisfaction'
        
        if outcome_var not in df.columns:
            return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Data unavailable"}}}
        
        for province in df['Province'].dropna().unique():
            prov_df = df[(df['Province'] == province) & 
                        (df[outcome_var].notna()) & 
                        (df[outcome_var] < 90)]
            if len(prov_df) > 0:
                risk_pct = (prov_df[outcome_var] < 5).sum() / len(prov_df) * 100
                risk_data.append({'Province': province, 'Risk_Score': risk_pct})
    
    if not risk_data:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    risk_df = pd.DataFrame(risk_data).sort_values('Risk_Score', ascending=False)
    
    base = alt.Chart(risk_df)

    bars = base.mark_bar().encode(
        x=alt.X('Risk_Score:Q', title='Risk %', axis=alt.Axis(labelFontSize=9, titleFontSize=10)),
        y=alt.Y('Province:N', title=None, sort='-x', axis=alt.Axis(labelFontSize=8, labelLimit=100)),
        color=alt.Color('Risk_Score:Q', scale=alt.Scale(scheme='oranges'), legend=None),
        tooltip=[alt.Tooltip('Province:N'), alt.Tooltip('Risk_Score:Q', format='.1f', title='Risk %')]
    )

    text = base.mark_text(align='left', dx=3, fontSize=9).encode(
        x=alt.X('Risk_Score:Q'),
        y=alt.Y('Province:N', sort='-x'),
        text=alt.Text('Risk_Score:Q', format='.1f')
    )

    chart = (bars + text).properties(
        width='container', height='container',
        title=alt.TitleParams(text=title, subtitle=subtitle,
                              fontSize=11, subtitleFontSize=9, subtitleColor='#666', anchor='start', dx=12)
    ).configure_view(strokeWidth=0)

    return chart.to_dict()
