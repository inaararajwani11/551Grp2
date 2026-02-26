# Healthcare Survey Analysis Dashboard

**Deployed App:** [https://five51grp2.onrender.com/](https://five51grp2.onrender.com/)

------------------------------------------------------------------------

## 📊 Project Overview

This project aims to analyze and visualize the Healthcare Survey Dataset to uncover insights regarding public health trends, mental health states, and lifestyle factors. Our team is developing an interactive dashboard to make these complex data relationships accessible and actionable for health researchers and policymakers.

------------------------------------------------------------------------

## Dataset Source:

Kaggle - Healthcare Survey <https://www.kaggle.com/datasets/aradhanahirapara/healthcare-survey>

------------------------------------------------------------------------

## 👥 Group Members

Xuanrui Qiu (Harry)

Inaara Rajwani

Yin-Wen Tsai (Ella)

Sage Yang

------------------------------------------------------------------------

## 📝 Important Project Notes

------------------------------------------------------------------------

## 📱 Description of App & Sketch

This dashboard is designed as an interactive health equity exploration tool based on a national healthcare survey dataset. The app presents a single-page interface with a left-hand filter panel and a main visualization area containing six coordinated plot panels arranged in a 2×3 grid.

The sidebar allows users to filter the dataset by province, age range, gender, income bracket, immigrant status, and Indigenous identity. Additional toggle controls allow users to switch between key outcome variables (e.g., general health, mental health, stress level, health utility index) and behavior variables (e.g., physical activity, diet, work hours). All filters dynamically update the visualizations.

The main panel includes: 

- a stacked bar chart showing the distribution of health outcomes across demographic groups;
- a scatter plot exploring relationships between health behaviors and outcomes;
- a heatmap showing chronic condition prevalence across socioeconomic groups;
- a grouped bar chart illustrating social determinants such as food security and sense of belonging;
- a bubble chart examining work stress and substance use interactions; and
- a ranking panel highlighting high-risk demographic groups.

All plots support hover tooltips and coordinated filtering, allowing users to explore patterns and disparities interactively. The design balances analytical depth with realistic implementation scope while addressing the core research questions on health inequity.

<img src="doc/AppSketch.svg" alt="Dashboard sketch" width="900"/>

------------------------------------------------------------------------

## 🛠 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/inaararajwani11/551Grp2.git
cd 551Grp2

# Install dependencies
pip install -r requirements.txt

# Run the app
python src/app.py
```

Then open http://localhost:8050 in your browser.

------------------------------------------------------------------------

## License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0).

The healthcare survey dataset was obtained from Kaggle and remains subject to its original CC BY-SA 4.0 license.

---

## 🚀 Milestone Roadmap

Milestone 1: Finalize scenario, dataset, target audience, and dashboard sketch.

Milestone 2: Create and deploy a functional prototype dashboard in Python.

Milestone 3: Design a user feedback survey and conduct experience testing.

Milestone 4: Implement feedback and finalize the production-ready dashboard.
