from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_vega_components as dvc
from plots import behavior_outcome_scatter

# Import data processing functions
import data_processing

# Initialize app
app = Dash(__name__)
server = app.server  # For deployment

# Load data
try:
    df = data_processing.load_data()
    filter_options = data_processing.get_filter_options(df)
    data_status = f"✅ Data loaded successfully! {len(df):,} records from {len(df.columns)} variables"
    data_loaded = True
except Exception as e:
    data_status = f"❌ Data loading failed: {str(e)}"
    filter_options = {}
    data_loaded = False
    df = pd.DataFrame()


def vega_text(message: str, font_size: int = 16):
    """Return a valid Vega-Lite spec that displays a centered text message."""
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": 700,
        "height": 450,
        "data": {"values": [{"text": message}]},
        "mark": {"type": "text", "fontSize": font_size, "align": "center", "baseline": "middle"},
        "encoding": {
            "text": {"field": "text"}
        },
    }


def apply_global_filters(
    df_in: pd.DataFrame,
    province: str,
    age_group: str,
    gender: str,
    income: str,
    immigrant: str,
    aboriginal: str,
) -> pd.DataFrame:
    """Apply the same filter logic used by Chart 1 so Chart 2 is connected to global filters."""
    filtered_df = df_in.copy()

    if province and province != "All":
        filtered_df = filtered_df[filtered_df["Province"] == province]

    # Age group filter (NOTE: requires Age to be real years)
    if age_group and age_group != "All":
        if age_group == "12-19":
            filtered_df = filtered_df[(filtered_df["Age"] >= 12) & (filtered_df["Age"] <= 19)]
        elif age_group == "20-34":
            filtered_df = filtered_df[(filtered_df["Age"] >= 20) & (filtered_df["Age"] <= 34)]
        elif age_group == "35-49":
            filtered_df = filtered_df[(filtered_df["Age"] >= 35) & (filtered_df["Age"] <= 49)]
        elif age_group == "50-64":
            filtered_df = filtered_df[(filtered_df["Age"] >= 50) & (filtered_df["Age"] <= 64)]
        elif age_group == "65+":
            filtered_df = filtered_df[filtered_df["Age"] >= 65]

    if gender and gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]

    if income and income != "All":
        filtered_df = filtered_df[filtered_df["Total_income"] == income]

    if immigrant and immigrant != "All":
        filtered_df = filtered_df[filtered_df["Immigrant"] == immigrant]

    if aboriginal and aboriginal != "All":
        filtered_df = filtered_df[filtered_df["Aboriginal_identity"] == aboriginal]

    return filtered_df


# App Layout
app.layout = html.Div([
    html.H1(
        "Healthcare Survey Analysis Dashboard",
        style={
            "textAlign": "center",
            "color": "#2c3e50",
            "padding": "20px",
            "margin": "0",
            "backgroundColor": "#ecf0f1",
        },
    ),

    # System Status
    html.Div([
        html.H3("System Status", style={"margin": "10px 0"}),
        html.P(data_status, style={"fontSize": "14px", "margin": "5px 0"}),
        html.P("✅ App infrastructure is running!", style={"color": "green", "margin": "5px 0"}),
    ], style={
        "padding": "15px",
        "border": "2px solid #3498db",
        "margin": "20px",
        "backgroundColor": "#ecf0f1",
        "borderRadius": "5px",
    }),

    html.Div([
        # ============ LEFT SIDEBAR ============
        html.Div([
            html.H3(
                "Global Controls",
                style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "20px"},
            ),

            # === FILTERS SECTION ===
            html.H4(
                "Filters",
                style={
                    "color": "#34495e",
                    "marginBottom": "15px",
                    "borderBottom": "2px solid #95a5a6",
                    "paddingBottom": "5px",
                },
            ),

            # Province Filter
            html.Div([
                html.Label("Province", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="province-filter",
                    options=[{"label": p, "value": p} for p in filter_options.get("provinces", ["All"])] if data_loaded else [],
                    value="All",
                    placeholder="Select Province...",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            # Age Group Filter
            html.Div([
                html.Label("Age Group", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="age-filter",
                    options=[
                        {"label": "All", "value": "All"},
                        {"label": "12-19 (Youth)", "value": "12-19"},
                        {"label": "20-34 (Young Adult)", "value": "20-34"},
                        {"label": "35-49 (Adult)", "value": "35-49"},
                        {"label": "50-64 (Middle Age)", "value": "50-64"},
                        {"label": "65+ (Senior)", "value": "65+"},
                    ],
                    value="All",
                    placeholder="Select Age Group...",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            # Gender Filter
            html.Div([
                html.Label("Gender", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="gender-filter",
                    options=[{"label": g, "value": g} for g in filter_options.get("genders", ["All"])] if data_loaded else [],
                    value="All",
                    placeholder="Select Gender...",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            # Income Filter
            html.Div([
                html.Label("Total Income", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="income-filter",
                    options=[{"label": i, "value": i} for i in filter_options.get("incomes", ["All"])] if data_loaded else [],
                    value="All",
                    placeholder="Select Income...",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            # Immigrant Status Filter
            html.Div([
                html.Label("Immigrant Status", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="immigrant-filter",
                    options=[{"label": i, "value": i} for i in filter_options.get("immigrant", ["All"])] if data_loaded else [],
                    value="All",
                    placeholder="Select Status...",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            # Aboriginal Identity Filter
            html.Div([
                html.Label("Aboriginal Identity", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="aboriginal-filter",
                    options=[{"label": a, "value": a} for a in filter_options.get("aboriginal", ["All"])] if data_loaded else [],
                    value="All",
                    placeholder="Select Identity...",
                    style={"marginBottom": "20px", "fontSize": "12px"},
                ),
            ]),

            html.Hr(style={"margin": "20px 0", "border": "1px solid #95a5a6"}),

            # === VARIABLE TOGGLES SECTION ===
            html.H4(
                "Variable Toggles",
                style={
                    "color": "#34495e",
                    "marginBottom": "15px",
                    "borderBottom": "2px solid #95a5a6",
                    "paddingBottom": "5px",
                },
            ),

            # Outcome Variable
            html.Div([
                html.Label("Outcome Variable", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="outcome-var",
                    options=[{"label": v.replace("_", " ").title(), "value": v}
                             for v in filter_options.get("outcome_vars", [])] if data_loaded else [],
                    value="Gen_health_state",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            # Behavior Variable (kept for future charts; Chart 2 is fixed by spec)
            html.Div([
                html.Label("Behavior Variable", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="behavior-var",
                    options=[{"label": v.replace("_", " ").title(), "value": v}
                             for v in filter_options.get("behavior_vars", [])] if data_loaded else [],
                    value="Total_physical_act_time",
                    style={"marginBottom": "25px", "fontSize": "12px"},
                ),
            ]),

            # Reset Button
            html.Button(
                "RESET FILTERS",
                id="reset-button",
                n_clicks=0,
                style={
                    "width": "100%",
                    "padding": "12px",
                    "backgroundColor": "#e74c3c",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "5px",
                    "cursor": "pointer",
                    "fontSize": "14px",
                    "fontWeight": "bold",
                    "marginTop": "10px",
                    "transition": "background-color 0.3s",
                },
            ),
        ], style={
            "width": "23%",
            "float": "left",
            "padding": "20px",
            "backgroundColor": "#c8e6c9",
            "minHeight": "800px",
            "boxShadow": "2px 0 5px rgba(0,0,0,0.1)",
        }),

        # ============ MAIN CHART AREA ============
        html.Div([
            html.H3(
                "Visualization Area",
                style={"textAlign": "center", "marginBottom": "20px", "color": "#2c3e50"},
            ),

            # Chart 1: Health Outcome Distribution
            html.Div([
                dvc.Vega(id="chart1", spec={}, style={"width": "100%"}),
            ], style={
                "backgroundColor": "white",
                "padding": "20px",
                "margin": "10px",
                "borderRadius": "5px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "minHeight": "520px",
            }),

            # Chart 2: Behavior × Outcome Scatter
            html.Div([
                dvc.Vega(id="chart2", spec={}, style={"width": "100%"}),
            ], style={
                "backgroundColor": "white",
                "padding": "20px",
                "margin": "10px",
                "borderRadius": "5px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "minHeight": "520px",
            }),

            # Placeholder for future charts
            html.Div([
                html.Div("📊 Chart 3: Social Determinants (Coming Soon)",
                         style={
                             "border": "2px dashed #bdc3c7",
                             "padding": "60px",
                             "textAlign": "center",
                             "color": "#95a5a6",
                             "fontSize": "16px",
                             "borderRadius": "5px",
                         }),
            ], style={"margin": "10px"}),

        ], style={
            "width": "75%",
            "float": "right",
            "padding": "20px",
        }),
    ], style={"display": "flex", "minHeight": "800px"}),

    # Footer
    html.Div([
        html.P(
            f"📊 Data Dictionary: {len(df.columns) if data_loaded else 0} variables available | "
            f"Records: {len(df):,} after filtering" if data_loaded else "",
            style={"textAlign": "center", "color": "#7f8c8d", "marginTop": "20px", "fontSize": "12px"},
        )
    ], style={"clear": "both"}),
])


# ============ CALLBACKS ============

@app.callback(
    [Output("province-filter", "value"),
     Output("age-filter", "value"),
     Output("gender-filter", "value"),
     Output("income-filter", "value"),
     Output("immigrant-filter", "value"),
     Output("aboriginal-filter", "value"),
     Output("outcome-var", "value"),
     Output("behavior-var", "value")],
    [Input("reset-button", "n_clicks")]
)
def reset_filters(n_clicks):
    """Reset all filters when button is clicked"""
    return "All", "All", "All", "All", "All", "All", "Gen_health_state", "Total_physical_act_time"


@app.callback(
    Output("chart1", "spec"),
    [Input("province-filter", "value"),
     Input("age-filter", "value"),
     Input("gender-filter", "value"),
     Input("income-filter", "value"),
     Input("immigrant-filter", "value"),
     Input("aboriginal-filter", "value"),
     Input("outcome-var", "value")]
)
def update_chart1(province, age_group, gender, income, immigrant, aboriginal, outcome_var):
    """Update Chart 1: Health Outcome Distribution"""
    import altair as alt

    if not data_loaded:
        return vega_text("Data not loaded")

    filtered_df = apply_global_filters(df, province, age_group, gender, income, immigrant, aboriginal)
    filtered_df = filtered_df.dropna(subset=[outcome_var, "Total_income"])

    if len(filtered_df) == 0:
        return vega_text("No data matches the current filter selection")

    chart_data = filtered_df.groupby([outcome_var, "Total_income"]).size().reset_index(name="count")

    health_order = ["Excellent", "Very good", "Good", "Fair", "Poor"]
    stress_order = ["Not at all stressful", "Not very stressful", "A bit stressful",
                    "Quite a bit stressful", "Extremely stressful"]

    if "health" in outcome_var.lower():
        sort_order = health_order
    elif "stress" in outcome_var.lower():
        sort_order = stress_order
    else:
        sort_order = None

    income_order = [
        "Less than $20,000",
        "$20,000 to $39,999",
        "$40,000 to $59,999",
        "$60,000 to $79,999",
        "$80,000 to $99,999",
        "$100,000 to $149,999",
        "$150,000 or more",
    ]

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X(
            f"{outcome_var}:N",
            title=outcome_var.replace("_", " ").title(),
            sort=sort_order if sort_order else alt.EncodingSortField(field="count", order="descending"),
            axis=alt.Axis(labelAngle=-45, labelLimit=200),
        ),
        y=alt.Y("count:Q", title="Number of Respondents", stack="zero"),
        color=alt.Color(
            "Total_income:N",
            title="Income Level",
            sort=income_order,
            scale=alt.Scale(scheme="tableau20"),
        ),
        tooltip=[
            alt.Tooltip(f"{outcome_var}:N", title=outcome_var.replace("_", " ").title()),
            alt.Tooltip("Total_income:N", title="Income Level"),
            alt.Tooltip("count:Q", title="Count", format=","),
        ],
    ).properties(
        width=700,
        height=450,
        title={
            "text": f"{outcome_var.replace('_', ' ').title()} Distribution by Income Level",
            "subtitle": f"Total respondents: {len(filtered_df):,} | Filter: {age_group if age_group != 'All' else 'All ages'}",
        },
    )

    return chart.to_dict()


@app.callback(
    Output("chart2", "spec"),
    [Input("province-filter", "value"),
     Input("age-filter", "value"),
     Input("gender-filter", "value"),
     Input("income-filter", "value"),
     Input("immigrant-filter", "value"),
     Input("aboriginal-filter", "value")]
)
def update_chart2(province, age_group, gender, income, immigrant, aboriginal):
    """Update Chart 2: Behavior × Outcome scatter plot"""
    if not data_loaded:
        return vega_text("Data not loaded")

    filtered_df = apply_global_filters(df, province, age_group, gender, income, immigrant, aboriginal)

    required_cols = ["Total_physical_act_time", "Health_utility_index", "Total_income"]
    missing = [c for c in required_cols if c not in filtered_df.columns]
    if missing:
        return vega_text(f"Chart 2 missing columns: {missing}", font_size=14)

    filtered_df = filtered_df.dropna(subset=required_cols)

    if len(filtered_df) == 0:
        return vega_text("No data matches the current filter selection")

    # Downsample for performance / avoid Altair/Vega issues with too many points
    if len(filtered_df) > 5000:
        filtered_df = filtered_df.sample(5000, random_state=42)

    try:
        chart = behavior_outcome_scatter(filtered_df)
        return chart.to_dict()
    except Exception as e:
        return vega_text(f"Chart 2 error: {type(e).__name__}: {str(e)[:120]}", font_size=12)


if __name__ == "__main__":
    app.run(debug=True, port=8050)