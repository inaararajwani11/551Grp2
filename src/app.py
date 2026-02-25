from dash import Dash, html, dcc, Input, Output
import pandas as pd
import os

# directly import data_processing（same folder）
import data_processing

# Initialize app
app = Dash(__name__)
server = app.server  # For deployment

# Load data
try:
    df = data_processing.load_data()
    filter_options = data_processing.get_filter_options(df)
    data_status = f"✅ Data loaded successfully! {len(df)} records from {len(df.columns)} variables"
    data_loaded = True
except Exception as e:
    data_status = f"❌ Data loading failed: {str(e)}"
    filter_options = {}
    data_loaded = False
    df = pd.DataFrame()

# App Layout
app.layout = html.Div([
    html.H1('Healthcare Survey Analysis Dashboard', 
            style={'textAlign': 'center', 'color': '#2c3e50', 'padding': '20px'}),
    
    html.Div([
        html.H3('System Status'),
        html.P(data_status, style={'fontSize': '16px'}),
        html.P('✅ App infrastructure is running!', style={'color': 'green'}),
    ], style={
        'padding': '20px', 
        'border': '2px solid #3498db', 
        'margin': '20px',
        'backgroundColor': '#ecf0f1'
    }),
    
    html.Div([
        # Left Sidebar - Control Panel
        html.Div([
            html.H3('Global Filters', style={'color': '#2c3e50'}),
            
            html.Div([
                html.Label('Province', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='province-filter',
                    options=[{'label': p, 'value': p} for p in filter_options.get('provinces', [])] if data_loaded else [],
                    placeholder='Select Province...',
                    style={'marginBottom': '15px'}
                ),
                
                html.Label('Gender', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='gender-filter',
                    options=[{'label': g, 'value': g} for g in filter_options.get('genders', [])] if data_loaded else [],
                    placeholder='Select Gender...',
                    style={'marginBottom': '15px'}
                ),
                
                html.Label('Income Level', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='income-filter',
                    options=[{'label': i, 'value': i} for i in filter_options.get('incomes', [])] if data_loaded else [],
                    placeholder='Select Income...',
                    style={'marginBottom': '20px'}
                ),
                
                html.Button('Reset Filters', 
                           id='reset-button', 
                           n_clicks=0,
                           style={
                               'width': '100%',
                               'padding': '10px',
                               'backgroundColor': '#e74c3c',
                               'color': 'white',
                               'border': 'none',
                               'borderRadius': '5px',
                               'cursor': 'pointer',
                               'fontSize': '14px',
                               'fontWeight': 'bold'
                           })
            ])
        ], style={
            'width': '22%', 
            'float': 'left', 
            'padding': '20px',
            'backgroundColor': '#c8e6c9',
            'minHeight': '600px'
        }),
        
        # Main Chart Area
        html.Div([
            html.H3('Visualization Area', style={'textAlign': 'center'}),
            
            html.Div([
                html.Div('📊 Chart 1: Health Outcome Distribution\n(Stacked Bar Chart)', 
                        style={
                            'border': '2px dashed #95a5a6', 
                            'padding': '80px', 
                            'margin': '10px',
                            'textAlign': 'center',
                            'backgroundColor': '#ffffff',
                            'fontSize': '16px',
                            'color': '#7f8c8d'
                        }),
            ]),
            
            html.Div([
                html.Div('📈 Chart 2: Behavior × Outcome\n(Scatter Plot)', 
                        style={
                            'border': '2px dashed #95a5a6', 
                            'padding': '80px', 
                            'margin': '10px',
                            'textAlign': 'center',
                            'backgroundColor': '#ffffff',
                            'fontSize': '16px',
                            'color': '#7f8c8d'
                        }),
            ]),
            
            html.Div([
                html.Div('📋 Chart 3: Social Determinants\n(Grouped Bar Chart)', 
                        style={
                            'border': '2px dashed #95a5a6', 
                            'padding': '80px', 
                            'margin': '10px',
                            'textAlign': 'center',
                            'backgroundColor': '#ffffff',
                            'fontSize': '16px',
                            'color': '#7f8c8d'
                        }),
            ])
        ], style={
            'width': '75%', 
            'float': 'right',
            'padding': '20px'
        })
    ], style={'display': 'flex'}),
    
    # Footer
    html.Div([
        html.P(f'Data Dictionary: {len(df.columns) if data_loaded else 0} variables available', 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': '20px'})
    ])
])

# Callback for reset button
@app.callback(
    [Output('province-filter', 'value'),
     Output('gender-filter', 'value'),
     Output('income-filter', 'value')],
    [Input('reset-button', 'n_clicks')]
)
def reset_filters(n_clicks):
    """Reset all filters when button is clicked"""
    return None, None, None

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)