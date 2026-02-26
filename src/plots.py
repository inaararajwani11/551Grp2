import altair as alt


def behavior_outcome_scatter(df):
    """
    Chart 2: Behavior × Outcome Scatter Plot
    Requirements:
      - Altair scatter plot
      - X: Total_physical_act_time
      - Y: Health_utility_index
      - Color: Total_income (income level)
      - Tooltips included
      - Connected to filters (handled in app.py by passing filtered df)
    """
    x_col = "Total_physical_act_time"
    y_col = "Health_utility_index"
    income_col = "Total_income"

    required = [x_col, y_col, income_col]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns for Chart 2: {missing}")

    chart = (
        alt.Chart(df)
        .mark_circle(size=60, opacity=0.7)
        .encode(
            x=alt.X(f"{x_col}:Q", title="Total physical activity time"),
            y=alt.Y(f"{y_col}:Q", title="Health utility index"),
            color=alt.Color(f"{income_col}:N", title="Income level"),
            tooltip=[
                alt.Tooltip(f"{x_col}:Q", title="Physical act time"),
                alt.Tooltip(f"{y_col}:Q", title="Health utility index"),
                alt.Tooltip(f"{income_col}:N", title="Income level"),
            ],
        )
        .properties(
            width=700,
            height=450,
            title={
                "text": "Behavior × Outcome: Physical Activity vs Health Utility",
                "subtitle": "Colored by income level"
            },
        )
        .interactive()
    )

    return chart