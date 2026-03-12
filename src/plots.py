"""
plots.py - Optimized compact charts for 2x3 grid
All charts sized to fit without scrolling: 350x250px
"""

import altair as alt
import pandas as pd


def create_health_outcome_chart(df, outcome_var='Gen_health_state'):
    """Chart 1: Health Outcome Distribution - Compact"""
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    chart_df = df.dropna(subset=[outcome_var, 'Total_income'])
    if len(chart_df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    agg_df = chart_df.groupby([outcome_var, 'Total_income']).size().reset_index(name='count')
    
    health_order = ['Excellent', 'Very good', 'Good', 'Fair', 'Poor']
    stress_order = ['Not at all stressful', 'Not very stressful', 'A bit stressful', 
                   'Quite a bit stressful', 'Extremely stressful']
    income_order = ['Less than $20,000', '$20,000 to $39,999', '$40,000 to $59,999', 
                   '$60,000 to $79,999', '$80,000 to $99,999', '$100,000 to $149,999', '$150,000 or more']
    
    sort_order = health_order if 'health' in outcome_var.lower() else (stress_order if 'stress' in outcome_var.lower() else None)
    
    chart = alt.Chart(agg_df).mark_bar().encode(
        x=alt.X(f'{outcome_var}:N', title=None, sort=sort_order,
                axis=alt.Axis(labelAngle=-30, labelLimit=100, labelFontSize=9)),
        y=alt.Y('count:Q', title='Count', stack='zero', axis=alt.Axis(titleFontSize=10, labelFontSize=9)),
        color=alt.Color('Total_income:N', title='Income', sort=income_order, scale=alt.Scale(scheme='tableau20'),
                       legend=alt.Legend(orient='right', titleFontSize=9, labelFontSize=8, labelLimit=100)),
        tooltip=[alt.Tooltip(f'{outcome_var}:N', title='Outcome'),
                 alt.Tooltip('Total_income:N', title='Income'),
                 alt.Tooltip('count:Q', title='Count', format=',')]
    ).properties(
        width=350, height=250,
        title=alt.TitleParams(text=f'{outcome_var.replace("_", " ").title()}', fontSize=11, anchor='start')
    ).configure_view(strokeWidth=0)
    
    return chart.to_dict()


def create_behavior_outcome_chart(df, behavior_var='Total_physical_act_time', outcome_var='Health_utility_index'):
    """Chart 2: Behavior × Outcome - Compact Scatter"""
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    chart_df = df.dropna(subset=[behavior_var, outcome_var, 'Total_income'])
    if len(chart_df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    scatter = alt.Chart(chart_df).mark_circle(size=30, opacity=0.6).encode(
        x=alt.X(f'{behavior_var}:Q', title=None, scale=alt.Scale(zero=False), axis=alt.Axis(labelFontSize=9)),
        y=alt.Y(f'{outcome_var}:Q', title=None, scale=alt.Scale(zero=False), axis=alt.Axis(labelFontSize=9)),
        color=alt.Color('Total_income:N', title='Income', scale=alt.Scale(scheme='category10'),
                       legend=alt.Legend(orient='right', labelFontSize=8, titleFontSize=9, labelLimit=80)),
        tooltip=[alt.Tooltip(f'{behavior_var}:Q', format='.0f'),
                 alt.Tooltip(f'{outcome_var}:Q', format='.2f'),
                 alt.Tooltip('Total_income:N')]
    )
    
    trend = scatter.transform_regression(behavior_var, outcome_var).mark_line(color='red', strokeDash=[5,5], size=1.5)
    
    chart = (scatter + trend).properties(
        width=350, height=250,
        title=alt.TitleParams(
            text=f'{behavior_var.replace("_", " ")[:18]}... vs {outcome_var.replace("_", " ")[:18]}...',
            fontSize=10, anchor='start'
        )
    ).configure_view(strokeWidth=0)
    
    return chart.to_dict()


def create_chronic_condition_heatmap(df):
    """Chart 3: Chronic Condition Heatmap - NO SCROLLING"""
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    conditions = ['High_BP', 'Diabetic', 'Mood_disorder', 'Anxiety_disorder']
    income_col = 'Total_income'
    
    available = [c for c in conditions if c in df.columns]
    if not available or income_col not in df.columns:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Chart 3: Data unavailable"}}}
    
    data_list = []
    for cond in available:
        for income in df[income_col].dropna().unique():
            subset = df[(df[income_col] == income) & (df[cond].notna())]
            if len(subset) > 0:
                prevalence = (subset[cond] == 'Yes').sum() / len(subset) * 100
                cond_short = cond.replace('_disorder', '').replace('_', ' ')
                data_list.append({'Condition': cond_short, 'Income': income, 'Prevalence': prevalence})
    
    if not data_list:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    heatmap_df = pd.DataFrame(data_list)
    
    chart = alt.Chart(heatmap_df).mark_rect().encode(
        x=alt.X('Condition:N', title='Condition', axis=alt.Axis(labelAngle=-30, labelLimit=80, labelFontSize=9)),
        y=alt.Y('Income:N', title=None, axis=alt.Axis(labelLimit=120, labelFontSize=8)),
        color=alt.Color('Prevalence:Q', title='%', scale=alt.Scale(scheme='reds'),
                       legend=alt.Legend(orient='right', titleFontSize=9, labelFontSize=8)),
        tooltip=[alt.Tooltip('Condition:N'), alt.Tooltip('Income:N'), 
                 alt.Tooltip('Prevalence:Q', format='.1f', title='Prevalence %')]
    ).properties(
        width=350, height=250,
        title=alt.TitleParams(text='Chronic Condition Prevalence', fontSize=11, anchor='start')
    ).configure_view(strokeWidth=0)
    
    return chart.to_dict()


def create_social_determinants_chart(df):
    """Chart 4: Social Determinants - Compact"""
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    required = ['Food_security', 'Immigrant']
    if not all(c in df.columns for c in required):
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Chart 4: Data unavailable"}}}
    
    chart_df = df.dropna(subset=required)
    if len(chart_df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    agg_df = chart_df.groupby(['Food_security', 'Immigrant']).size().reset_index(name='count')
    
    chart = alt.Chart(agg_df).mark_bar().encode(
        x=alt.X('Food_security:N', title=None, axis=alt.Axis(labelAngle=-30, labelFontSize=9, labelLimit=80)),
        y=alt.Y('count:Q', title='Count', axis=alt.Axis(labelFontSize=9, titleFontSize=10)),
        color=alt.Color('Immigrant:N', title='Status', scale=alt.Scale(scheme='set2'),
                       legend=alt.Legend(orient='right', labelFontSize=8, titleFontSize=9)),
        tooltip=[alt.Tooltip('Food_security:N'), alt.Tooltip('Immigrant:N'), alt.Tooltip('count:Q', format=',')]
    ).properties(
        width=350, height=250,
        title=alt.TitleParams(text='Food Security × Immigration', fontSize=11, anchor='start')
    ).configure_view(strokeWidth=0)
    
    return chart.to_dict()


def create_work_stress_substance_chart(df):
    """Chart 5: Work Stress × Substance Use - Compact Bubble"""
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    required = ['Work_stress', 'Weekly_alcohol', 'Life_satisfaction']
    if not all(c in df.columns for c in required):
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Chart 5: Data unavailable"}}}
    
    chart_df = df.dropna(subset=required)
    if len(chart_df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    agg_df = chart_df.groupby(['Work_stress', 'Weekly_alcohol']).agg({'Life_satisfaction': 'mean'}).reset_index()
    agg_df['count'] = chart_df.groupby(['Work_stress', 'Weekly_alcohol']).size().values
    
    agg_df['Category'] = 'Data'
    color_col = 'Category'
    
    chart = alt.Chart(agg_df).mark_circle(opacity=0.7).encode(
        x=alt.X('Work_stress:N', title=None, axis=alt.Axis(labelAngle=-30, labelFontSize=9, labelLimit=60)),
        y=alt.Y('Weekly_alcohol:N', title=None, axis=alt.Axis(labelFontSize=9, labelLimit=60)),
        size=alt.Size('count:Q', title='n', scale=alt.Scale(range=[80, 800]),
                     legend=alt.Legend(orient='right', labelFontSize=8, titleFontSize=9)),
        color=alt.Color(f'{color_col}:N', scale=alt.Scale(scheme='category10'),
                       legend=None),
        tooltip=[alt.Tooltip('Work_stress:N', title='Work Stress'),
                 alt.Tooltip('Weekly_alcohol:N', title='Alcohol'),
                 alt.Tooltip('Life_satisfaction:Q', title='Avg Life Sat', format='.2f'),
                 alt.Tooltip('count:Q', title='Count', format=',')]
    ).properties(
        width=350, height=250,
        title=alt.TitleParams(text='Work Stress × Alcohol Use', fontSize=11, anchor='start')
    ).configure_view(strokeWidth=0)
    
    return chart.to_dict()


def create_risk_ranking_chart(df):
    """Chart 6: Risk Ranking - Compact"""
    if len(df) == 0:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    if 'Province' not in df.columns or 'Gen_health_state' not in df.columns:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Chart 6: Coming Soon"}}}
    
    risk_data = []
    for province in df['Province'].dropna().unique():
        prov_df = df[df['Province'] == province].dropna(subset=['Gen_health_state'])
        if len(prov_df) > 0:
            poor_pct = (prov_df['Gen_health_state'].isin(['Fair', 'Poor'])).sum() / len(prov_df) * 100
            risk_data.append({'Province': province, 'Risk_Score': poor_pct})
    
    if not risk_data:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "No data"}}}
    
    risk_df = pd.DataFrame(risk_data).sort_values('Risk_Score', ascending=False)
    
    chart = alt.Chart(risk_df).mark_bar().encode(
        x=alt.X('Risk_Score:Q', title='Risk %', axis=alt.Axis(labelFontSize=9, titleFontSize=10)),
        y=alt.Y('Province:N', title=None, sort='-x', axis=alt.Axis(labelFontSize=8, labelLimit=100)),
        color=alt.Color('Risk_Score:Q', scale=alt.Scale(scheme='redyellowgreen', reverse=True), legend=None),
        tooltip=[alt.Tooltip('Province:N'), alt.Tooltip('Risk_Score:Q', format='.1f')]
    ).properties(
        width=350, height=250,
        title=alt.TitleParams(text='Health Risk Ranking', fontSize=11, anchor='start')
    ).configure_view(strokeWidth=0)
    
    return chart.to_dict()
