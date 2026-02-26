# Reflection — Milestone 2

## What We Have Implemented

Our dashboard is a single-page Dash application deployed on [Render](https://five51grp2.onrender.com/). It features a left sidebar with six global filters (Province, Age Group, Gender, Total Income, Immigrant Status, Aboriginal Identity) and two variable toggles (Outcome Variable, Behavior Variable), plus a Reset Filters button. All filters dynamically update the three charts in the main panel:

- **Chart 1 — Stacked Bar Chart:** Shows the distribution of a user-selected health outcome variable (e.g., general health, mental health, stress level) broken down by income level. Users can switch the outcome variable via the sidebar toggle.
- **Chart 2 — Scatter Plot:** Displays the relationship between physical activity time and health utility index, colored by income level. Large datasets are down-sampled to 5,000 points for performance.
- **Chart 3 — Grouped Bar Chart:** Explores the association between food security status and average mental health score, grouped by immigrant status. This chart addresses the social-determinants research question.

All charts are built with Altair and rendered via `dash-vega-components` (Charts 1 & 2) or an embedded HTML iframe (Chart 3). The data pipeline (`data_processing.py`) loads the raw CSV, maps numeric codes to human-readable labels using a codebook, and provides filter options to the layout.

## What Is Not Yet Implemented

Three of the six originally proposed chart panels remain unimplemented: the chronic-condition heatmap, the work-stress bubble chart, and the high-risk demographic ranking panel. The Behavior Variable toggle currently does not affect Chart 2, which is hardcoded to physical activity time vs. health utility index. We plan to wire this toggle in a future milestone.

## Known Limitations

- Chart 3 uses an `html.Iframe` instead of `dvc.Vega`, which is inconsistent with the other two charts and slightly limits interactivity.
- The Age filter relies on numeric age values and predefined bins, which may not perfectly align with the coded age groups in the raw data.
- On Render's free tier, the app may experience cold-start delays of up to a minute.

## Strengths

The dashboard already provides a usable, end-to-end workflow: load data, filter interactively, and explore three distinct analytical perspectives. The sidebar design is clean and self-documenting with clear labels. Coordinated filtering across all charts lets users drill into specific subpopulations easily.

## Future Improvements

- Implement the remaining three chart panels (heatmap, bubble chart, ranking).
- Connect the Behavior Variable toggle to Chart 2 so users can explore different x-axis variables.
- Migrate Chart 3 to `dvc.Vega` for consistency.
- Improve the layout to a 2×3 grid as originally proposed.
- Add a brief in-app description or help section for first-time users.
