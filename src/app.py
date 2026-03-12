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
HEADER_H = '52px'
SIDEBAR_W = '208px'

_dd_style = {'fontSize': '10px', 'marginBottom': '6px'}

def _filter_group(title, color, children, open_default=False):
    """Collapsible filter section using native HTML <details>"""
    return html.Details([
        html.Summary([
            html.Span([
                html.Span(style={'width': '3px', 'height': '10px', 'backgroundColor': color,
                                  'borderRadius': '2px', 'display': 'inline-block',
                                  'marginRight': '6px', 'verticalAlign': 'middle'}),
                title,
            ]),
            html.Span(className='filter-summary-icon'),
        ], className=''),
        html.Div(children, className='filter-body'),
    ], open=open_default, className='filter-section')

# Chart card
CARD = {'flex': '1', 'minWidth': '0', 'padding': '8px', 'backgroundColor': 'white',
        'margin': '4px', 'borderRadius': '10px', 'border': '1px solid #e8ecf1',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.04)', 'overflow': 'hidden'}

# ============ LAYOUT ============
app.layout = html.Div([
    # ===== HEADER =====
    html.Div([
        # Teal accent line
        html.Div(style={'position': 'absolute', 'top': '0', 'left': '0', 'right': '0',
                         'height': '3px', 'background': 'linear-gradient(90deg, #0d9488, #06b6d4, #0d9488)'}),
        html.Div([
            html.H1('Healthcare Survey Analysis',
                     style={'margin': '0', 'fontSize': '17px', 'fontWeight': '700',
                            'color': '#1e293b', 'letterSpacing': '-0.3px'}),
            html.Span('Dashboard', style={'fontSize': '17px', 'fontWeight': '400',
                                          'color': '#94a3b8', 'marginLeft': '6px'}),
        ], style={'display': 'flex', 'alignItems': 'baseline'}),
        html.Div([
            html.Span(data_status, style={'fontSize': '11px', 'color': '#0d9488', 'fontWeight': '500'}),
            html.Span(' | ', style={'color': '#e2e8f0', 'margin': '0 8px'}),
            html.Span(id='filtered-count', style={'fontSize': '11px', 'color': '#475569', 'fontWeight': '600'}),
        ]),
    ], style={'background': 'white', 'display': 'flex', 'justifyContent': 'space-between',
              'alignItems': 'center', 'padding': '0 20px', 'height': HEADER_H,
              'borderBottom': '1px solid #e8ecf1', 'position': 'relative'}),

    html.Div([
        # ===== SIDEBAR =====
        html.Div([
            html.Div([

                # --- Health Focus pills (most prominent) ---
                html.Div('Health Focus', className='filter-label'),
                dcc.RadioItems(
                    id='health-focus',
                    options=[
                        {'label': 'Physical', 'value': 'Physical Health'},
                        {'label': 'Mental',   'value': 'Mental Health'},
                        {'label': 'Lifestyle','value': 'Lifestyle Behaviors'},
                    ],
                    value='Physical Health',
                    className='radio-pills',
                    inputStyle={'display': 'none'},
                ),

                # --- Compare By pills ---
                html.Div('Compare By', className='filter-label', style={'marginTop': '8px'}),
                dcc.RadioItems(
                    id='compare-by',
                    options=[
                        {'label': 'Income',    'value': 'Income'},
                        {'label': 'Education', 'value': 'Education'},
                        {'label': 'Age',       'value': 'Age'},
                        {'label': 'Gender',    'value': 'Gender'},
                    ],
                    value='Income',
                    className='radio-pills',
                    inputStyle={'display': 'none'},
                ),

                html.Hr(style={'border': 'none', 'borderTop': '1px solid #e2e8f0',
                               'margin': '12px 0 10px'}),

                # --- Collapsible filter groups ---
                _filter_group('Demographics', '#0d9488', [
                    html.Label('Province', className='filter-label'),
                    dcc.Dropdown(id='province-filter',
                                 options=[{'label': p, 'value': p} for p in filter_options.get('provinces', ['All'])] if data_loaded else [],
                                 value='All', clearable=False, style=_dd_style),
                    html.Label('Age', className='filter-label'),
                    dcc.Dropdown(id='age-filter',
                                 options=[{'label': a, 'value': a} for a in filter_options.get('age_groups', ['All'])] if data_loaded else [],
                                 value='All', clearable=False, style=_dd_style),
                    html.Label('Gender', className='filter-label'),
                    dcc.Dropdown(id='gender-filter',
                                 options=[{'label': g, 'value': g} for g in filter_options.get('genders', ['All'])] if data_loaded else [],
                                 value='All', clearable=False, style=_dd_style),
                ], open_default=True),

                _filter_group('Socioeconomic', '#0891b2', [
                    html.Label('Education', className='filter-label'),
                    dcc.Dropdown(id='education-filter',
                                 options=[{'label': e, 'value': e} for e in filter_options.get('educations', ['All'])] if data_loaded else [],
                                 value='All', clearable=False, style=_dd_style),
                    html.Label('Marital Status', className='filter-label'),
                    dcc.Dropdown(id='marital-filter',
                                 options=[{'label': m, 'value': m} for m in filter_options.get('maritals', ['All'])] if data_loaded else [],
                                 value='All', clearable=False, style=_dd_style),
                    html.Label('Income', className='filter-label'),
                    dcc.Dropdown(id='income-filter',
                                 options=[{'label': i, 'value': i} for i in filter_options.get('incomes', ['All'])] if data_loaded else [],
                                 value='All', clearable=False, style=_dd_style),
                ], open_default=False),

                _filter_group('Identity', '#d97706', [
                    html.Label('Immigrant', className='filter-label'),
                    dcc.Dropdown(id='immigrant-filter',
                                 options=[{'label': i, 'value': i} for i in filter_options.get('immigrant', ['All'])] if data_loaded else [],
                                 value='All', clearable=False, style=_dd_style),
                    html.Label('Aboriginal', className='filter-label'),
                    dcc.Dropdown(id='aboriginal-filter',
                                 options=[{'label': a, 'value': a} for a in filter_options.get('aboriginal', ['All'])] if data_loaded else [],
                                 value='All', clearable=False, style=_dd_style),
                ], open_default=False),

                html.Button('Reset All Filters', id='reset-button', n_clicks=0,
                            style={'width': '100%', 'padding': '7px 0', 'marginTop': '10px',
                                   'backgroundColor': 'transparent', 'color': '#0d9488',
                                   'border': '1.5px solid #0d9488', 'borderRadius': '6px',
                                   'cursor': 'pointer', 'fontSize': '11px', 'fontWeight': '600'}),

            ], style={'padding': '10px 10px 16px'})
        ], className='sidebar-light', style={
            'width': SIDEBAR_W, 'minWidth': SIDEBAR_W, 'maxWidth': SIDEBAR_W,
            'backgroundColor': '#f8fafc',
            'height': f'calc(100vh - {HEADER_H})', 'overflowY': 'auto',
            'position': 'fixed', 'left': '0', 'top': HEADER_H,
            'borderRight': '1px solid #e8ecf1',
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
            'marginLeft': SIDEBAR_W, 'padding': '6px',
            'height': f'calc(100vh - {HEADER_H})', 'overflow': 'hidden',
            'display': 'flex', 'flexDirection': 'column',
            'backgroundColor': '#eef2f6',
        }),
    ], style={'position': 'relative'}),
], style={'fontFamily': FONT, 'margin': '0', 'padding': '0',
         'height': '100vh', 'width': '100vw', 'overflow': 'hidden',
         'backgroundColor': '#eef2f6'})

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
