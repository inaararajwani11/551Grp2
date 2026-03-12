from dash import Dash, html, dcc, Input, Output
import pandas as pd
import os
import plots
import dash_vega_components as dvc
import data_processing

app = Dash(__name__)
server = app.server

# Load data
try:
    df = data_processing.load_data()
    filter_options = data_processing.get_filter_options(df)
    data_status = f"✅ {len(df):,} records loaded"
    data_loaded = True
except Exception as e:
    data_status = f"❌ Error: {str(e)}"
    filter_options = {}
    data_loaded = False
    df = pd.DataFrame()

# Age group mapping
AGE_GROUP_MAP = {'12-19': 1, '20-34': 2, '35-49': 3, '50-64': 4, '65+': 5}

def apply_global_filters(df_in, province, age_group, gender, education, marital, income, immigrant, aboriginal):
    """Apply global filters to dataframe"""
    filtered_df = df_in.copy()

    if province and province != "All":
        filtered_df = filtered_df[filtered_df["Province"] == province]

    if age_group and age_group != "All":
        age_code = AGE_GROUP_MAP.get(age_group)
        if age_code:
            filtered_df = filtered_df[filtered_df["Age"] == age_code]

    if gender and gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]
    if education and education != "All":
        filtered_df = filtered_df[filtered_df["Edu_level_text"] == education]
    if marital and marital != "All":
        filtered_df = filtered_df[filtered_df["Marital_status_text"] == marital]
    if income and income != "All":
        filtered_df = filtered_df[filtered_df["Total_income"] == income]
    if immigrant and immigrant != "All":
        filtered_df = filtered_df[filtered_df["Immigrant"] == immigrant]
    if aboriginal and aboriginal != "All":
        filtered_df = filtered_df[filtered_df["Aboriginal_identity"] == aboriginal]

    return filtered_df

# ============ COMPACT LAYOUT ============
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Healthcare Survey Analysis Dashboard', 
               style={'margin': '0', 'padding': '12px', 'fontSize': '20px', 'color': '#2c3e50'}),
        html.Div([
            html.Span(data_status, style={'fontSize': '11px', 'color': '#27ae60', 'marginRight': '20px'}),
            html.Span(id='filtered-count', style={'fontSize': '11px', 'color': '#3498db', 'fontWeight': 'bold'}),
        ], style={'padding': '3px'}),
    ], style={'backgroundColor': '#ecf0f1', 'textAlign': 'center', 'borderBottom': '2px solid #3498db'}),

    html.Div([
        # ========== SIDEBAR (緊湊版) ==========
        html.Div([
            html.Div([
                # === FILTERS ===
                html.H4("Filters", style={'fontSize': '12px', 'margin': '8px 0 5px', 'color': '#2c3e50', 
                                         'borderBottom': '2px solid #3498db', 'paddingBottom': '3px'}),
                
                # Province
                html.Label('Province', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(id='province-filter', 
                            options=[{'label': p, 'value': p} for p in filter_options.get('provinces', ['All'])] if data_loaded else [],
                            value='All', clearable=False, style={'fontSize': '9px', 'marginBottom': '6px'}),
                
                # Age
                html.Label('Age', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(id='age-filter', 
                            options=[{'label': a, 'value': a} for a in filter_options.get('age_groups', ['All'])] if data_loaded else [],
                            value='All', clearable=False, style={'fontSize': '9px', 'marginBottom': '6px'}),
                
                # Gender
                html.Label('Gender', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(id='gender-filter', 
                            options=[{'label': g, 'value': g} for g in filter_options.get('genders', ['All'])] if data_loaded else [],
                            value='All', clearable=False, style={'fontSize': '9px', 'marginBottom': '6px'}),
                
                # Education
                html.Label('Education', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(id='education-filter', 
                            options=[{'label': e, 'value': e} for e in filter_options.get('educations', ['All'])] if data_loaded else [],
                            value='All', clearable=False, style={'fontSize': '9px', 'marginBottom': '6px'}),
                
                # Marital
                html.Label('Marital', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(id='marital-filter', 
                            options=[{'label': m, 'value': m} for m in filter_options.get('maritals', ['All'])] if data_loaded else [],
                            value='All', clearable=False, style={'fontSize': '9px', 'marginBottom': '6px'}),
                
                # Income
                html.Label('Income', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(id='income-filter', 
                            options=[{'label': i, 'value': i} for i in filter_options.get('incomes', ['All'])] if data_loaded else [],
                            value='All', clearable=False, style={'fontSize': '9px', 'marginBottom': '6px'}),
                
                # Immigrant
                html.Label('Immigrant', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(id='immigrant-filter', 
                            options=[{'label': i, 'value': i} for i in filter_options.get('immigrant', ['All'])] if data_loaded else [],
                            value='All', clearable=False, style={'fontSize': '9px', 'marginBottom': '6px'}),
                
                # Aboriginal
                html.Label('Aboriginal', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(id='aboriginal-filter', 
                            options=[{'label': a, 'value': a} for a in filter_options.get('aboriginal', ['All'])] if data_loaded else [],
                            value='All', clearable=False, style={'fontSize': '9px', 'marginBottom': '8px'}),
                
                html.Hr(style={'margin': '8px 0', 'border': '1px solid #bdc3c7'}),
                
                # === TOGGLES (改成下拉選單) ===
                html.H4("Theme", style={'fontSize': '12px', 'margin': '8px 0 5px', 'color': '#2c3e50',
                                       'borderBottom': '2px solid #3498db', 'paddingBottom': '3px'}),
                
                # Health Focus (Dropdown)
                html.Label('Health Focus', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(
                    id='health-focus',
                    options=[{'label': h, 'value': h} for h in filter_options.get('health_focus', [])] if data_loaded else [],
                    value='Physical Health',
                    clearable=False,
                    style={'fontSize': '9px', 'marginBottom': '6px'}
                ),
                
                # Compare By (Dropdown)
                html.Label('Compare By', style={'fontSize': '9px', 'fontWeight': 'bold', 'marginBottom': '2px', 'display': 'block'}),
                dcc.Dropdown(
                    id='compare-by',
                    options=[{'label': c, 'value': c} for c in filter_options.get('compare_by', [])] if data_loaded else [],
                    value='Income',
                    clearable=False,
                    style={'fontSize': '9px', 'marginBottom': '10px'}
                ),
                
                html.Button('RESET ALL', id='reset-button', n_clicks=0, 
                           style={'width': '100%', 'padding': '8px', 'backgroundColor': '#e74c3c', 
                                  'color': 'white', 'border': 'none', 'borderRadius': '4px', 
                                  'cursor': 'pointer', 'fontSize': '10px', 'fontWeight': 'bold'}),
            ], style={'padding': '10px'})
        ], style={
            'width': '18%',
            'minWidth': '180px',
            'maxWidth': '220px',
            'backgroundColor': '#d5f4e6',
            'height': 'calc(100vh - 64px)',
            'overflowY': 'auto',
            'position': 'fixed',
            'left': '0',
            'top': '64px',
            'boxShadow': '2px 0 5px rgba(0,0,0,0.1)'
        }),
        
        # ========== CHARTS ==========
        html.Div([
            html.Div([
                html.Div([dvc.Vega(id='chart1', spec={}, style={'width': '100%', 'height': '100%'})], 
                        style={'flex': '1', 'minWidth': '0', 'padding': '5px', 'backgroundColor': 'white', 
                               'margin': '3px', 'borderRadius': '5px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'overflow': 'hidden'}),
                html.Div([dvc.Vega(id='chart2', spec={}, style={'width': '100%', 'height': '100%'})], 
                        style={'flex': '1', 'minWidth': '0', 'padding': '5px', 'backgroundColor': 'white', 
                               'margin': '3px', 'borderRadius': '5px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'overflow': 'hidden'}),
                html.Div([dvc.Vega(id='chart3', spec={}, style={'width': '100%', 'height': '100%'})], 
                        style={'flex': '1', 'minWidth': '0', 'padding': '5px', 'backgroundColor': 'white', 
                               'margin': '3px', 'borderRadius': '5px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'overflow': 'hidden'}),
            ], style={'display': 'flex', 'flexWrap': 'nowrap', 'height': '49%', 'gap': '0'}),
            
            html.Div([
                html.Div([dvc.Vega(id='chart4', spec={}, style={'width': '100%', 'height': '100%'})], 
                        style={'flex': '1', 'minWidth': '0', 'padding': '5px', 'backgroundColor': 'white', 
                               'margin': '3px', 'borderRadius': '5px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'overflow': 'hidden'}),
                html.Div([dvc.Vega(id='chart5', spec={}, style={'width': '100%', 'height': '100%'})], 
                        style={'flex': '1', 'minWidth': '0', 'padding': '5px', 'backgroundColor': 'white', 
                               'margin': '3px', 'borderRadius': '5px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'overflow': 'hidden'}),
                html.Div([dvc.Vega(id='chart6', spec={}, style={'width': '100%', 'height': '100%'})], 
                        style={'flex': '1', 'minWidth': '0', 'padding': '5px', 'backgroundColor': 'white', 
                               'margin': '3px', 'borderRadius': '5px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'overflow': 'hidden'}),
            ], style={'display': 'flex', 'flexWrap': 'nowrap', 'height': '49%', 'gap': '0'}),
        ], style={
            'marginLeft': '18%', 'padding': '4px',
            'height': 'calc(100vh - 64px)', 'overflow': 'hidden',
            'display': 'flex', 'flexDirection': 'column', 'gap': '0'
        }),
    ], style={'position': 'relative'}),
], style={'fontFamily': 'Arial, sans-serif', 'margin': '0', 'padding': '0', 
         'height': '100vh', 'width': '100vw', 'overflow': 'hidden'})

# ============ CALLBACKS ============

@app.callback(
    [Output('province-filter', 'value'), Output('age-filter', 'value'), Output('gender-filter', 'value'),
     Output('education-filter', 'value'), Output('marital-filter', 'value'),
     Output('income-filter', 'value'), Output('immigrant-filter', 'value'), Output('aboriginal-filter', 'value'),
     Output('health-focus', 'value'), Output('compare-by', 'value')],
    [Input('reset-button', 'n_clicks')]
)
def reset_all(n_clicks):
    return 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'Physical Health', 'Income'

@app.callback(
    Output('filtered-count', 'children'),
    [Input('province-filter', 'value'), Input('age-filter', 'value'), Input('gender-filter', 'value'),
     Input('education-filter', 'value'), Input('marital-filter', 'value'),
     Input('income-filter', 'value'), Input('immigrant-filter', 'value'), Input('aboriginal-filter', 'value')]
)
def update_count(province, age, gender, edu, marital, income, imm, ab):
    if not data_loaded:
        return ""
    filtered = apply_global_filters(df, province, age, gender, edu, marital, income, imm, ab)
    pct = len(filtered) / len(df) * 100
    return f"📊 {len(filtered):,} records ({pct:.1f}%)"

ALL_INPUTS = [
    Input('province-filter', 'value'), Input('age-filter', 'value'), Input('gender-filter', 'value'),
    Input('education-filter', 'value'), Input('marital-filter', 'value'),
    Input('income-filter', 'value'), Input('immigrant-filter', 'value'), Input('aboriginal-filter', 'value'),
    Input('health-focus', 'value'), Input('compare-by', 'value')
]

@app.callback(Output('chart1', 'spec'), ALL_INPUTS)
def update_chart1(province, age, gender, edu, marital, income, imm, ab, health_focus, compare_by):
    if not data_loaded:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Loading..."}}}
    try:
        filtered = apply_global_filters(df, province, age, gender, edu, marital, income, imm, ab)
        return plots.create_chart1(filtered, health_focus, compare_by)
    except Exception as e:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": f"Error: {str(e)[:80]}"}}}

@app.callback(Output('chart2', 'spec'), ALL_INPUTS)
def update_chart2(province, age, gender, edu, marital, income, imm, ab, health_focus, compare_by):
    if not data_loaded:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Loading..."}}}
    try:
        filtered = apply_global_filters(df, province, age, gender, edu, marital, income, imm, ab)
        return plots.create_chart2(filtered, health_focus, compare_by)
    except Exception as e:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": f"Error: {str(e)[:80]}"}}}

@app.callback(Output('chart3', 'spec'), ALL_INPUTS)
def update_chart3(province, age, gender, edu, marital, income, imm, ab, health_focus, compare_by):
    if not data_loaded:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Loading..."}}}
    try:
        filtered = apply_global_filters(df, province, age, gender, edu, marital, income, imm, ab)
        return plots.create_chart3(filtered, health_focus, compare_by)
    except Exception as e:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": f"Error: {str(e)[:80]}"}}}

@app.callback(Output('chart4', 'spec'), ALL_INPUTS)
def update_chart4(province, age, gender, edu, marital, income, imm, ab, health_focus, compare_by):
    if not data_loaded:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Loading..."}}}
    try:
        filtered = apply_global_filters(df, province, age, gender, edu, marital, income, imm, ab)
        return plots.create_chart4(filtered, health_focus, compare_by)
    except Exception as e:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": f"Error: {str(e)[:80]}"}}}

@app.callback(Output('chart5', 'spec'), ALL_INPUTS)
def update_chart5(province, age, gender, edu, marital, income, imm, ab, health_focus, compare_by):
    if not data_loaded:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Loading..."}}}
    try:
        filtered = apply_global_filters(df, province, age, gender, edu, marital, income, imm, ab)
        return plots.create_chart5(filtered, health_focus, compare_by)
    except Exception as e:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": f"Error: {str(e)[:80]}"}}}

@app.callback(Output('chart6', 'spec'), ALL_INPUTS)
def update_chart6(province, age, gender, edu, marital, income, imm, ab, health_focus, compare_by):
    if not data_loaded:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": "Loading..."}}}
    try:
        filtered = apply_global_filters(df, province, age, gender, edu, marital, income, imm, ab)
        return plots.create_chart6(filtered, health_focus, compare_by)
    except Exception as e:
        return {"data": {"values": []}, "mark": "text", "encoding": {"text": {"value": f"Error: {str(e)[:80]}"}}}

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
