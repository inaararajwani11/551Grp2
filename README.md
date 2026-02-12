### Healthcare Survey Analysis Dashboard

## 📊 Project Overview

This project aims to analyze and visualize the Healthcare Survey Dataset to uncover insights regarding public health trends, mental health states, and lifestyle factors. Our team is developing an interactive dashboard to make these complex data relationships accessible and actionable for health researchers and policymakers.

# Dataset Source:

Kaggle - Healthcare Survey https://www.kaggle.com/datasets/aradhanahirapara/healthcare-survey

# 👥 Group Members

Xuanrui Qiu (Harry)

Inaara Rajwani

Yin-Wen Tsai (Ella)

Sage Yang (AJ)

# 📝 Important Project Notes

# 🎯 Motivation and Purpose

**Role:** We are a health analytics team within a public health research institute, providing decision-support tools for healthcare administrators and policymakers.

**Target Audience:** Healthcare administrators, policy makers, public health researchers, and clinical managers who need to identify risk factors and design targeted interventions based on population health data.

**Problem Solved:** Healthcare survey data contains complex, multi-dimensional relationships that are difficult to interpret without specialized tools. Our dashboard enables users to interactively explore these relationships, identify at-risk populations, and discover actionable insights for targeted health interventions—without requiring advanced statistical expertise. By making population health patterns visible and explorable, we aim to accelerate evidence-based decision-making and improve resource allocation for vulnerable communities.

# 💾 Description of the Data

Dimensions: The dataset contains 108,252 rows and 50 columns.

Demographics: Key variables include Province, Gender, Age, Edu_level, and Total_income.

Health Indicators: Features include Gen_health_state, Mental_health_state, Stress_level, and Life_satisfaction.

Chronic Conditions: Tracks diagnoses for High_BP, Diabetic, Mood_disorder, and Anxiety_disorder.

Lifestyle & Behavior: Includes Physical_vigorous_act_time, weekly_alcohol, Cannabies_use, and Fruit_veg_con.

# 🔍 Research Questions and Usage Scenarios

***Research Questions***

- How do **physical activity** measures (`Total_physical_act_time`, `Physical_vigorous_act_time`) and **diet** (`Fruit_veg_con`) relate to `Stress_level` and `Mental_health_state` across `Age` and `Total_income` brackets?
- Which **demographic and socioeconomic** factors (`Province`, `Gender`, `Aboriginal_identity`, `Immigrant`, `Edu_level`, `Food_security`, `Insurance_cover`) most strongly predict low `Health_utility_index` or poor `Gen_health_state`?
- Does limited **insurance coverage** or **food insecurity** increase odds of unmanaged chronic conditions (`High_BP`, `Diabetic`, `Mood_disorder`, `Anxiety_disorder`) after controlling for lifestyle factors?
- How do **Work_hours + Work_stress** interact with **substance use** (`Weekly_alcohol`, `Cannabis_use`), and what is their combined effect on `Life_satisfaction`?
- Do provinces with lower **Sense_belonging** show higher prevalence of mood/anxiety disorders, even after adjusting for income and education?
- How do `BMI_18_above` categories pair with `Musculoskeletal_con` and `Cardiovascular_con`, and is regular `Physical_vigorous_act_time` protective?
- Does **Sleep_apnea** co-occur with high `Work_stress` or long `Work_hours`, and how does that affect `Health_utility_index` and `Pain_status`?
- Does **Sense_belonging mediate** the relationship between `Food_security` and `Mental_health_state` for `Immigrant` vs non-Immigrant groups?
- Which factors (`Age`, `Total_income`, `Insurance_cover`, `Family_doctor`) most influence whether chronic conditions are diagnosed vs potentially **under-detected** (high self-reported `Stress_level` but no recorded `High_BP`/`Diabetic`)?

***Usage Scenarios***

- **Policy analysts** map `Province × Food_security × Insurance_cover` to surface communities where high `Stress_level` co-occurs with low access to care, guiding targeted funding.
- **Clinic managers** use “what-if” filters (`Age`, `BMI_18_above`, `Physical_vigorous_act_time`, `Fruit_veg_con`) to flag cohorts at greatest risk for hypertension/diabetes and plan preventive outreach.
- **Mental health leads** segment by `Sense_belonging`, `Work_stress`, and `Weekly_alcohol` to identify workplace populations needing stress-reduction and substance-use interventions.
- **Indigenous health coordinators** compare `Aboriginal_identity` with `Insurance_cover` and `Family_doctor` to find gaps in preventive care and chronic disease follow-up.
- **Public health evaluators** track `Food_security → Mental_health_state → Life_satisfaction` pathways by `Province` to prioritize nutrition and counseling programs.
- **Corporate HR teams** model `Work_hours + Work_stress + Sleep_apnea` patterns to design return-to-work and workload policies that reduce burnout.

# 📱 Description of App & Sketch

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

<img src="Milestone 1/AppSketch.svg" alt="Dashboard sketch" width="900">

# 🚀 Milestone Roadmap

Milestone 1: Finalize scenario, dataset, target audience, and dashboard sketch.

Milestone 2: Create and deploy a functional prototype dashboard in Python.

Milestone 3: Design a user feedback survey and conduct experience testing.

Milestone 4: Implement feedback and finalize the production-ready dashboard.
