# **Group 2 Proposal**

#### Group Member: Xuanrui Qiu (Harry), Inaara Rajwani, Yin-Wen Tsai (Ella), Sage Yang

This project aims to analyze and visualize the Healthcare Survey Dataset to uncover insights regarding public health trends, mental health states, and lifestyle factors. Our team is developing an interactive dashboard to make these complex data relationships accessible and actionable for health researchers and policymakers.

------------------------------------------------------------------------

## 🎯 Motivation and Purpose

**Role:** We are a health analytics team within a public health research institute, providing decision-support tools for healthcare administrators and policymakers.

**Target Audience:** Healthcare administrators, policy makers, public health researchers, and clinical managers who need to identify risk factors and design targeted interventions based on population health data.

**Problem Solved:** Healthcare survey data contains complex, multi-dimensional relationships that are difficult to interpret without specialized tools. Our dashboard enables users to interactively explore these relationships, identify at-risk populations, and discover actionable insights for targeted health interventions—without requiring advanced statistical expertise. By making population health patterns visible and explorable, we aim to accelerate evidence-based decision-making and improve resource allocation for vulnerable communities.

------------------------------------------------------------------------

## 💾 Description of the Data

**Data source:** Kaggle - Healthcare Survey <https://www.kaggle.com/datasets/aradhanahirapara/healthcare-survey>

We will visualize a Canadian healthcare survey dataset with 108,252 observations and 50 variables, where each row represents one respondent. The dataset includes:

(1) demographic and socioeconomic attributes (e.g., age group, sex/gender, geography, education/income-related indicators),

(2) health status and chronic-condition indicators, and

(3) lifestyle and behavioral factors (e.g., smoking and physical activity). Many fields are stored as numeric codes and include special response values (e.g., “valid skip”, “don’t know”, “refused”, “not stated”).

We will use the accompanying codebook to map coded values to human-readable categories and to convert non-substantive codes into NA/“Unknown” before building the visualizations.

Given the large number of columns, we will focus on a smaller set of variables that supports our dashboard’s main goal: **exploring how key health outcomes vary across population groups and behaviors.** Our planned visualizations will emphasize differences in outcome distributions across age/sex/region and their association with lifestyle factors (especially smoking and physical activity). We will also derive a small number of new variables to simplify interpretation, such as standardized “Unknown/NA” categories, grouped activity levels derived from activity frequency/time fields, and summary indicators (e.g., a count or composite index of selected health risk factors/conditions) where appropriate.

------------------------------------------------------------------------

## 🔍 Research Questions and Usage Scenarios

***Research Questions***

-   How do **physical activity** measures (`Total_physical_act_time`, `Physical_vigorous_act_time`) and **diet** (`Fruit_veg_con`) relate to `Stress_level` and `Mental_health_state` across `Age` and `Total_income` brackets?
-   Which **demographic and socioeconomic** factors (`Province`, `Gender`, `Aboriginal_identity`, `Immigrant`, `Edu_level`, `Food_security`, `Insurance_cover`) most strongly predict low `Health_utility_index` or poor `Gen_health_state`?
-   Does limited **insurance coverage** or **food insecurity** increase odds of unmanaged chronic conditions (`High_BP`, `Diabetic`, `Mood_disorder`, `Anxiety_disorder`) after controlling for lifestyle factors?
-   How do **Work_hours + Work_stress** interact with **substance use** (`Weekly_alcohol`, `Cannabis_use`), and what is their combined effect on `Life_satisfaction`?
-   Do provinces with lower **Sense_belonging** show higher prevalence of mood/anxiety disorders, even after adjusting for income and education?
-   How do `BMI_18_above` categories pair with `Musculoskeletal_con` and `Cardiovascular_con`, and is regular `Physical_vigorous_act_time` protective?
-   Does **Sleep_apnea** co-occur with high `Work_stress` or long `Work_hours`, and how does that affect `Health_utility_index` and `Pain_status`?
-   Does **Sense_belonging mediate** the relationship between `Food_security` and `Mental_health_state` for `Immigrant` vs non-Immigrant groups?
-   Which factors (`Age`, `Total_income`, `Insurance_cover`, `Family_doctor`) most influence whether chronic conditions are diagnosed vs potentially **under-detected** (high self-reported `Stress_level` but no recorded `High_BP`/`Diabetic`)?

***Usage Scenarios***

-   **Policy analysts** map `Province × Food_security × Insurance_cover` to surface communities where high `Stress_level` co-occurs with low access to care, guiding targeted funding.
-   **Clinic managers** use “what-if” filters (`Age`, `BMI_18_above`, `Physical_vigorous_act_time`, `Fruit_veg_con`) to flag cohorts at greatest risk for hypertension/diabetes and plan preventive outreach.
-   **Mental health leads** segment by `Sense_belonging`, `Work_stress`, and `Weekly_alcohol` to identify workplace populations needing stress-reduction and substance-use interventions.
-   **Indigenous health coordinators** compare `Aboriginal_identity` with `Insurance_cover` and `Family_doctor` to find gaps in preventive care and chronic disease follow-up.
-   **Public health evaluators** track `Food_security → Mental_health_state → Life_satisfaction` pathways by `Province` to prioritize nutrition and counseling programs.
-   **Corporate HR teams** model `Work_hours + Work_stress + Sleep_apnea` patterns to design return-to-work and workload policies that reduce burnout.
