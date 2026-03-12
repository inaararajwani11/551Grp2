from dash import Dash, html, dcc, Input, Output
import pandas as pd
import os
import dash_vega_components as dvc

# allow both `python src/app.py` and `python -m src.app`
try:
    from . import plots, data_processing  # type: ignore
except ImportError:
    import plots  # type: ignore
    import data_processing  # type: ignore

app = Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap'
])
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

# ============ DESIGN TOKENS ============
FONT = '"DM Sans", sans-serif'
HEADER_H = '56px'
SIDEBAR_W = '210px'

# Sidebar styles
_section = lambda label, color: html.Div(label, style={
    'fontSize': '10px', 'fontWeight': '700', 'color': color, 'letterSpacing': '1.2px',
    'textTransform': 'uppercase', 'margin': '14px 0 6px', 'paddingBottom': '4px',
    'borderBottom': f'2px solid {color}'})

_label = lambda text: html.Label(text, style={
    'fontSize': '10px', 'fontWeight': '600', 'color': '#94a3b8',
    'marginBottom': '2px', 'display': 'block'})

_dd_style = {'fontSize': '10px', 'marginBottom': '8px'}

# Chart card style
CARD = {'flex': '1', 'minWidth': '0', 'padding': '8px', 'backgroundColor': 'white',
        'margin': '4px', 'borderRadius': '8px', 'border': '1px solid #e2e8f0',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.06)', 'overflow': 'hidden'}

# ============ LAYOUT ============
app.layout = html.Div([
    # ===== HEADER =====
    html.Div([
        html.Div([
            html.H1('Healthcare Survey Analysis',
                     style={'margin': '0', 'fontSize': '18px', 'fontWeight': '700',
                            'color': 'white', 'letterSpacing': '-0.3px'}),
            html.Span('Dashboard', style={'fontSize': '18px', 'fontWeight': '300',
                                          'color': 'rgba(255,255,255,0.7)', 'marginLeft': '6px'}),
        ], style={'display': 'flex', 'alignItems': 'baseline'}),
        html.Div([
            html.Span(data_status, style={'fontSize': '11px', 'color': '#6ee7b7'}),
            html.Span(' | ', style={'color': 'rgba(255,255,255,0.2)', 'margin': '0 8px'}),
            html.Span(id='filtered-count', style={'fontSize': '11px', 'color': '#93c5fd', 'fontWeight': '600'}),
        ]),
    ], style={'background': '#0f172a', 'display': 'flex', 'justifyContent': 'space-between',
              'alignItems': 'center', 'padding': '0 20px', 'height': HEADER_H,
              'borderBottom': '1px solid #1e293b'}),

    html.Div([
        # ===== SIDEBAR =====
        html.Div([
            html.Div([
                _section('Demographics', '#38bdf8'),
                _label('Province'),
                dcc.Dropdown(id='province-filter',
                             options=[{'label': p, 'value': p} for p in filter_options.get('provinces', ['All'])] if data_loaded else [],
                             value='All', clearable=False, style=_dd_style),
                _label('Age'),
                dcc.Dropdown(id='age-filter',
                             options=[{'label': a, 'value': a} for a in filter_options.get('age_groups', ['All'])] if data_loaded else [],
                             value='All', clearable=False, style=_dd_style),
                _label('Gender'),
                dcc.Dropdown(id='gender-filter',
                             options=[{'label': g, 'value': g} for g in filter_options.get('genders', ['All'])] if data_loaded else [],
                             value='All', clearable=False, style=_dd_style),

                _section('Socioeconomic', '#34d399'),
                _label('Education'),
                dcc.Dropdown(id='education-filter',
                             options=[{'label': e, 'value': e} for e in filter_options.get('educations', ['All'])] if data_loaded else [],
                             value='All', clearable=False, style=_dd_style),
                _label('Marital'),
                dcc.Dropdown(id='marital-filter',
                             options=[{'label': m, 'value': m} for m in filter_options.get('maritals', ['All'])] if data_loaded else [],
                             value='All', clearable=False, style=_dd_style),
                _label('Income'),
                dcc.Dropdown(id='income-filter',
                             options=[{'label': i, 'value': i} for i in filter_options.get('incomes', ['All'])] if data_loaded else [],
                             value='All', clearable=False, style=_dd_style),

                _section('Identity', '#fb923c'),
                _label('Immigrant'),
                dcc.Dropdown(id='immigrant-filter',
                             options=[{'label': i, 'value': i} for i in filter_options.get('immigrant', ['All'])] if data_loaded else [],
                             value='All', clearable=False, style=_dd_style),
                _label('Aboriginal'),
                dcc.Dropdown(id='aboriginal-filter',
                             options=[{'label': a, 'value': a} for a in filter_options.get('aboriginal', ['All'])] if data_loaded else [],
                             value='All', clearable=False, style=_dd_style),

                _section('Analysis', '#a78bfa'),
                _label('Health Focus'),
                dcc.Dropdown(id='health-focus',
                             options=[{'label': h, 'value': h} for h in filter_options.get('health_focus', [])] if data_loaded else [],
                             value='Physical Health', clearable=False, style=_dd_style),
                _label('Compare By'),
                dcc.Dropdown(id='compare-by',
                             options=[{'label': c, 'value': c} for c in filter_options.get('compare_by', [])] if data_loaded else [],
                             value='Income', clearable=False, style=_dd_style),

                html.Button('Reset All Filters', id='reset-button', n_clicks=0,
                            style={'width': '100%', 'padding': '8px 0', 'marginTop': '12px',
                                   'backgroundColor': 'transparent', 'color': '#f87171',
                                   'border': '1px solid #f87171', 'borderRadius': '6px',
                                   'cursor': 'pointer', 'fontSize': '11px', 'fontWeight': '600',
                                   'letterSpacing': '0.3px'}),
            ], style={'padding': '8px 12px 16px'})
        ], className='sidebar-dark', style={
            'width': SIDEBAR_W, 'minWidth': SIDEBAR_W, 'maxWidth': SIDEBAR_W,
            'backgroundColor': '#0f172a', 'color': '#e2e8f0',
            'height': f'calc(100vh - {HEADER_H})', 'overflowY': 'auto',
            'position': 'fixed', 'left': '0', 'top': HEADER_H,
        }),

        # ===== CHARTS =====
        html.Div([
            html.Div([
                html.Div([dvc.Vega(id='chart1', spec={}, style={'width': '100%', 'height': '100%'})],
                         className='chart-card', style=CARD),
                html.Div([dvc.Vega(id='chart2', spec={}, style={'width': '100%', 'height': '100%'})],
                         className='chart-card', style=CARD),
                html.Div([dvc.Vega(id='chart3', spec={}, style={'width': '100%', 'height': '100%'})],
                         className='chart-card', style=CARD),
            ], style={'display': 'flex', 'height': '50%'}),
            html.Div([
                html.Div([dvc.Vega(id='chart4', spec={}, style={'width': '100%', 'height': '100%'})],
                         className='chart-card', style=CARD),
                html.Div([dvc.Vega(id='chart5', spec={}, style={'width': '100%', 'height': '100%'})],
                         className='chart-card', style=CARD),
                html.Div([dvc.Vega(id='chart6', spec={}, style={'width': '100%', 'height': '100%'})],
                         className='chart-card', style=CARD),
            ], style={'display': 'flex', 'height': '50%'}),
        ], style={
            'marginLeft': SIDEBAR_W, 'padding': '4px',
            'height': f'calc(100vh - {HEADER_H})', 'overflow': 'hidden',
            'display': 'flex', 'flexDirection': 'column',
            'backgroundColor': '#f1f5f9',
        }),
    ], style={'position': 'relative'}),
], style={'fontFamily': FONT, 'margin': '0', 'padding': '0',
         'height': '100vh', 'width': '100vw', 'overflow': 'hidden',
         'backgroundColor': '#0f172a'})

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
