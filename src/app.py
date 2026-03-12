from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_vega_components as dvc

# Import local modules (works both as script and module)
try:
    from .plots import behavior_outcome_scatter
    from . import data_processing
except ImportError:
    from plots import behavior_outcome_scatter
    import data_processing

app = Dash(__name__)
server = app.server

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
    """Return a simple Vega-Lite spec for displaying a message."""
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": 700,
        "height": 450,
        "data": {"values": [{"text": message}]},
        "mark": {
            "type": "text",
            "fontSize": font_size,
            "align": "center",
            "baseline": "middle",
        },
        "encoding": {"text": {"field": "text"}},
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
    """Apply shared global filters across charts."""
    filtered_df = df_in.copy()

    if province and province != "All":
        filtered_df = filtered_df[filtered_df["Province"] == province]

    # Keep original logic to avoid breaking the existing app
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
        # LEFT SIDEBAR
        html.Div([
            html.H3(
                "Global Controls",
                style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "20px"},
            ),

            html.H4(
                "Filters",
                style={
                    "color": "#34495e",
                    "marginBottom": "15px",
                    "borderBottom": "2px solid #95a5a6",
                    "paddingBottom": "5px",
                },
            ),

            html.Div([
                html.Label("Province", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="province-filter",
                    options=[{"label": p, "value": p} for p in filter_options.get("provinces", ["All"])] if data_loaded else [],
                    value="All",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

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
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            html.Div([
                html.Label("Gender", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="gender-filter",
                    options=[{"label": g, "value": g} for g in filter_options.get("genders", ["All"])] if data_loaded else [],
                    value="All",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            html.Div([
                html.Label("Total Income", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="income-filter",
                    options=[{"label": i, "value": i} for i in filter_options.get("incomes", ["All"])] if data_loaded else [],
                    value="All",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            html.Div([
                html.Label("Immigrant Status", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="immigrant-filter",
                    options=[{"label": i, "value": i} for i in filter_options.get("immigrant", ["All"])] if data_loaded else [],
                    value="All",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            html.Div([
                html.Label("Aboriginal Identity", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="aboriginal-filter",
                    options=[{"label": a, "value": a} for a in filter_options.get("aboriginal", ["All"])] if data_loaded else [],
                    value="All",
                    style={"marginBottom": "20px", "fontSize": "12px"},
                ),
            ]),

            html.Hr(style={"margin": "20px 0", "border": "1px solid #95a5a6"}),

            html.H4(
                "Variable Toggles",
                style={
                    "color": "#34495e",
                    "marginBottom": "15px",
                    "borderBottom": "2px solid #95a5a6",
                    "paddingBottom": "5px",
                },
            ),

            html.Div([
                html.Label("Outcome Variable", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="outcome-var",
                    options=[{"label": v.replace("_", " ").title(), "value": v} for v in filter_options.get("outcome_vars", [])] if data_loaded else [],
                    value="Gen_health_state",
                    style={"marginBottom": "15px", "fontSize": "12px"},
                ),
            ]),

            html.Div([
                html.Label("Behavior Variable", style={"fontWeight": "bold", "fontSize": "13px", "color": "#555"}),
                dcc.Dropdown(
                    id="behavior-var",
                    options=[{"label": v.replace("_", " ").title(), "value": v} for v in filter_options.get("behavior_vars", [])] if data_loaded else [],
                    value="Total_physical_act_time",
                    style={"marginBottom": "25px", "fontSize": "12px"},
                ),
            ]),

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
                },
            ),
        ], style={
            "width": "23%",
            "float": "left",
            "padding": "20px",
            "backgroundColor": "#c8e6c9",
            "minHeight": "800px",
        }),

        # MAIN CHART AREA
        html.Div([
            html.H3(
                "Visualization Area",
                style={"textAlign": "center", "marginBottom": "20px", "color": "#2c3e50"},
            ),

            html.Div(
                [dvc.Vega(id="chart1", spec={}, style={"width": "100%"})],
                style={
                    "backgroundColor": "white",
                    "padding": "20px",
                    "margin": "10px",
                    "borderRadius": "5px",
                    "minHeight": "520px",
                },
            ),

            html.Div(
                [dvc.Vega(id="chart2", spec={}, style={"width": "100%"})],
                style={
                    "backgroundColor": "white",
                    "padding": "20px",
                    "margin": "10px",
                    "borderRadius": "5px",
                    "minHeight": "520px",
                },
            ),

            html.Div([
                html.H4(
                    "Chart 3: Social Determinants — Food Security × Mental Health (Immigrant status)",
                    style={"marginBottom": "10px", "color": "#2c3e50", "textAlign": "left"},
                ),
                html.Iframe(id="chart3", style={"width": "100%", "height": "520px", "border": "none"}),
                html.P(
                    "Y-axis shows the average mental health score (1 = Excellent, 5 = Poor) for each food security category, grouped by immigrant status.",
                    style={"fontSize": "12px", "color": "#7f8c8d", "marginTop": "8px"},
                ),
            ], style={
                "backgroundColor": "white",
                "padding": "20px",
                "margin": "10px",
                "borderRadius": "5px",
                "minHeight": "520px",
            }),

            html.Div([
                html.H4(
                    "⑥ Risk Ranking Panel",
                    style={
                        "marginBottom": "8px",
                        "color": "#2c3e50",
                        "textAlign": "left",
                        "fontWeight": "bold",
                    },
                ),
                html.Div(
                    dvc.Vega(id="chart6", spec={}, style={"width": "100%"}),
                    style={
                        "height": "340px",
                        "overflowY": "auto",
                        "paddingRight": "6px",
                    },
                ),
            ], style={
                "backgroundColor": "white",
                "padding": "20px",
                "margin": "10px",
                "borderRadius": "5px",
                "minHeight": "420px",
                "border": "1px solid #d9d9d9",
            }),

        ], style={"width": "75%", "float": "right", "padding": "20px"})
    ], style={"display": "flex", "minHeight": "800px"}),

    html.Div([
        html.P(
            f"📊 Data Dictionary: {len(df.columns) if data_loaded else 0} variables available | Records: {len(df):,} after filtering"
            if data_loaded else "",
            style={
                "textAlign": "center",
                "color": "#7f8c8d",
                "marginTop": "20px",
                "fontSize": "12px",
            },
        )
    ], style={"clear": "both"}),
])


@app.callback(
    [
        Output("province-filter", "value"),
        Output("age-filter", "value"),
        Output("gender-filter", "value"),
        Output("income-filter", "value"),
        Output("immigrant-filter", "value"),
        Output("aboriginal-filter", "value"),
        Output("outcome-var", "value"),
        Output("behavior-var", "value"),
    ],
    [Input("reset-button", "n_clicks")]
)
def reset_filters(n_clicks):
    return "All", "All", "All", "All", "All", "All", "Gen_health_state", "Total_physical_act_time"


@app.callback(
    Output("chart1", "spec"),
    [
        Input("province-filter", "value"),
        Input("age-filter", "value"),
        Input("gender-filter", "value"),
        Input("income-filter", "value"),
        Input("immigrant-filter", "value"),
        Input("aboriginal-filter", "value"),
        Input("outcome-var", "value"),
    ]
)
def update_chart1(province, age_group, gender, income, immigrant, aboriginal, outcome_var):
    import altair as alt

    if not data_loaded:
        return vega_text("Data not loaded")

    filtered_df = apply_global_filters(df, province, age_group, gender, income, immigrant, aboriginal)
    filtered_df = filtered_df.dropna(subset=[outcome_var, "Total_income"])

    if len(filtered_df) == 0:
        return vega_text("No data matches the current filter selection")

    chart_data = filtered_df.groupby([outcome_var, "Total_income"]).size().reset_index(name="count")

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X(
            f"{outcome_var}:N",
            title=outcome_var.replace("_", " ").title(),
            axis=alt.Axis(labelAngle=-45, labelLimit=200),
        ),
        y=alt.Y("count:Q", title="Number of Respondents"),
        color=alt.Color("Total_income:N", title="Income Level"),
        tooltip=[
            alt.Tooltip(f"{outcome_var}:N"),
            alt.Tooltip("Total_income:N"),
            alt.Tooltip("count:Q", format=","),
        ],
    ).properties(width=700, height=450)

    return chart.to_dict()


@app.callback(
    Output("chart2", "spec"),
    [
        Input("province-filter", "value"),
        Input("age-filter", "value"),
        Input("gender-filter", "value"),
        Input("income-filter", "value"),
        Input("immigrant-filter", "value"),
        Input("aboriginal-filter", "value"),
    ]
)
def update_chart2(province, age_group, gender, income, immigrant, aboriginal):
    if not data_loaded:
        return vega_text("Data not loaded")

    filtered_df = apply_global_filters(df, province, age_group, gender, income, immigrant, aboriginal)
    filtered_df = filtered_df.dropna(subset=["Total_physical_act_time", "Health_utility_index", "Total_income"])

    if len(filtered_df) == 0:
        return vega_text("No data matches the current filter selection")

    if len(filtered_df) > 5000:
        filtered_df = filtered_df.sample(5000, random_state=42)

    try:
        return behavior_outcome_scatter(filtered_df).to_dict()
    except Exception as e:
        return vega_text(f"Chart 2 error: {type(e).__name__}: {str(e)[:120]}", font_size=12)


@app.callback(
    Output("chart3", "srcDoc"),
    [
        Input("province-filter", "value"),
        Input("age-filter", "value"),
        Input("gender-filter", "value"),
        Input("income-filter", "value"),
        Input("immigrant-filter", "value"),
        Input("aboriginal-filter", "value"),
    ]
)
def update_chart3(province, age_group, gender, income, immigrant, aboriginal):
    import altair as alt

    if not data_loaded:
        return '<html><body><h3 style="text-align:center;color:#95a5a6;">Data not loaded</h3></body></html>'

    filtered_df = apply_global_filters(df, province, age_group, gender, income, immigrant, aboriginal)
    filtered_df = filtered_df.dropna(subset=["Food_security", "Mental_health_state", "Immigrant"])

    if len(filtered_df) == 0:
        return '<html><body style="display:flex;justify-content:center;align-items:center;height:100%;"><h3 style="color:#95a5a6;">No data matches the current filter selection</h3></body></html>'

    mental_score_map = {"Excellent": 1, "Very good": 2, "Good": 3, "Fair": 4, "Poor": 5}
    filtered_df = filtered_df.copy()
    filtered_df["Mental_health_score"] = filtered_df["Mental_health_state"].map(mental_score_map)

    grouped = (
        filtered_df
        .groupby(["Food_security", "Immigrant"])
        .agg(
            avg_score=("Mental_health_score", "mean"),
            respondent_count=("Mental_health_state", "size"),
        )
        .reset_index()
    )

    food_order = ["Food secure", "Moderately food insecure", "Severely food insecure"]
    immigrant_order = ["Yes", "No"]
    available_food = [f for f in food_order if f in grouped["Food_security"].unique()]
    age_label = age_group if age_group != "All" else "All ages"

    bars = (
        alt.Chart(grouped)
        .mark_bar(size=60)
        .encode(
            x=alt.X(
                "Food_security:N",
                title="Food security status",
                sort=available_food if available_food else food_order,
                axis=alt.Axis(labelAngle=0, labelLimit=240, labelPadding=10),
                scale=alt.Scale(paddingInner=0.15, paddingOuter=0.2),
            ),
            xOffset=alt.XOffset("Immigrant:N", title=None),
            y=alt.Y(
                "avg_score:Q",
                title="Average mental health (1 = Excellent, 5 = Poor)",
                scale=alt.Scale(domain=[0, 5], nice=False),
            ),
            y2=alt.Y2(value=0),
            color=alt.Color(
                "Immigrant:N",
                title="Immigrant status",
                sort=immigrant_order,
                scale=alt.Scale(range=["#1f77b4", "#ff7f0e"]),
            ),
            tooltip=[
                alt.Tooltip("Food_security:N", title="Food security"),
                alt.Tooltip("Immigrant:N", title="Immigrant status"),
                alt.Tooltip("avg_score:Q", title="Average mental health", format=".2f"),
                alt.Tooltip("respondent_count:Q", title="Respondents", format=","),
            ],
        )
    )

    baseline = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(
        color="#666",
        strokeWidth=1,
        opacity=0.8,
    ).encode(y="y:Q")

    chart = (
        (bars + baseline)
        .properties(
            width=640,
            height=430,
            title={
                "text": "Social determinants: mental health by food security (immigrant status)",
                "subtitle": f"Total: {len(filtered_df):,} respondents | Filter: {age_label}",
            },
        )
        .configure_axis(labelFontSize=11, titleFontSize=13, gridColor="#e5e7eb", gridOpacity=0.7)
        .configure_view(strokeWidth=0)
        .configure_legend(titleFontSize=12, labelFontSize=10, orient="right", offset=10)
    )

    return chart.to_html()


@app.callback(
    Output("chart6", "spec"),
    [
        Input("province-filter", "value"),
        Input("age-filter", "value"),
        Input("gender-filter", "value"),
        Input("income-filter", "value"),
        Input("immigrant-filter", "value"),
        Input("aboriginal-filter", "value"),
        Input("outcome-var", "value"),
    ]
)
def update_chart6(province, age_group, gender, income, immigrant, aboriginal, outcome_var):
    import altair as alt

    if not data_loaded:
        return vega_text("Data not loaded")

    filtered_df = apply_global_filters(
        df, province, age_group, gender, income, immigrant, aboriginal
    )

    group_col = "Province"

    if group_col not in filtered_df.columns or outcome_var not in filtered_df.columns:
        return vega_text("Required columns are missing")

    filtered_df = filtered_df.dropna(subset=[group_col, outcome_var]).copy()

    if len(filtered_df) == 0:
        return vega_text("No data matches the current filter selection")

    health_map = {
        "Excellent": 1,
        "Very good": 2,
        "Good": 3,
        "Fair": 4,
        "Poor": 5,
    }
    stress_map = {
        "Not at all stressful": 1,
        "Not very stressful": 2,
        "A bit stressful": 3,
        "Quite a bit stressful": 4,
        "Extremely stressful": 5,
    }

    descending_is_worse = True

    if outcome_var in ["Gen_health_state", "Mental_health_state"]:
        filtered_df["risk_score"] = filtered_df[outcome_var].map(health_map)
    elif outcome_var == "Stress_level":
        filtered_df["risk_score"] = filtered_df[outcome_var].map(stress_map)
    elif outcome_var == "Health_utility_index":
        filtered_df["risk_score"] = pd.to_numeric(filtered_df[outcome_var], errors="coerce")
        descending_is_worse = False
    else:
        filtered_df["risk_score"] = pd.to_numeric(filtered_df[outcome_var], errors="coerce")

    filtered_df = filtered_df.dropna(subset=["risk_score"])

    if len(filtered_df) == 0:
        return vega_text("Outcome variable has no usable values under current filters")

    grouped = (
        filtered_df
        .groupby(group_col, dropna=False)
        .agg(
            mean_risk=("risk_score", "mean"),
            respondent_count=("risk_score", "size"),
        )
        .reset_index()
    )

    grouped = grouped[grouped["respondent_count"] >= 50]

    if len(grouped) == 0:
        return vega_text("Not enough data per group after filtering")

    if descending_is_worse:
        grouped = grouped.sort_values("mean_risk", ascending=False).head(10)
    else:
        grouped = grouped.sort_values("mean_risk", ascending=True).head(10)

    max_risk = grouped["mean_risk"].max()
    if pd.isna(max_risk) or max_risk == 0:
        return vega_text("Unable to compute ranking")

    grouped["risk_percent"] = grouped["mean_risk"] / max_risk * 100
    grouped = grouped.reset_index(drop=True)
    grouped["rank"] = grouped.index + 1

    chart = (
        alt.Chart(grouped)
        .mark_bar(size=28)
        .encode(
            y=alt.Y(
                f"{group_col}:N",
                sort="-x",
                axis=alt.Axis(labelFontSize=12, labelLimit=180),
            ),
            x=alt.X(
                "risk_percent:Q",
                title="Risk Score (%)",
                axis=alt.Axis(format=".0f"),
            ),
            color=alt.Color(
                "rank:N",
                scale=alt.Scale(range=[
                    "#e45756", "#f58549", "#f2b134", "#b7c95b", "#7dbf6a",
                    "#5fb49c", "#4c78a8", "#6c5ce7", "#9b59b6", "#c06c84"
                ]),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip(f"{group_col}:N", title="Province"),
                alt.Tooltip("mean_risk:Q", title="Mean risk score", format=".2f"),
                alt.Tooltip("risk_percent:Q", title="Risk score (%)", format=".1f"),
                alt.Tooltip("respondent_count:Q", title="Respondents", format=","),
            ],
        )
        .properties(
            width=420,
            height=420,
        )
        .configure_view(stroke=None)
        .configure_axis(
            grid=False,
            labelColor="#333",
            titleColor="#333",
        )
    )

    return chart.to_dict()


if __name__ == "__main__":
    app.run(debug=True, port=8050)