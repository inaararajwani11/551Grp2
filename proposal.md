# **Group 2 Proposal**

#### Group Member: Xuanrui Qiu (Harry), Inaara Rajwani, Yin-Wen Tsai (Ella), Sage Yang

This project aims to analyze and visualize the Healthcare Survey Dataset to uncover insights regarding public health trends, mental health states, and lifestyle factors. Our team is developing an interactive dashboard to make these complex data relationships accessible and actionable for health researchers and policymakers.

------------------------------------------------------------------------

## Motivation and Purpose

**Role:** We are a health analytics team within a public health research institute, providing decision-support tools for healthcare administrators and policymakers.

**Target Audience:** Healthcare administrators, policy makers, public health researchers, and clinical managers who need to identify risk factors and design targeted interventions based on population health data.

**Problem Solved:** Healthcare survey data contains complex, multi-dimensional relationships that are difficult to interpret without specialized tools. Our dashboard enables users to interactively explore these relationships, identify at-risk populations, and discover actionable insights for targeted health interventions—without requiring advanced statistical expertise. By making population health patterns visible and explorable, we aim to accelerate evidence-based decision-making and improve resource allocation for vulnerable communities.

------------------------------------------------------------------------

## Description of the Data

**Data source:** Kaggle - Healthcare Survey <https://www.kaggle.com/datasets/aradhanahirapara/healthcare-survey>

We will visualize a Canadian healthcare survey dataset with 108,252 observations and 50 variables, where each row represents one respondent. The dataset includes:

(1) demographic and socioeconomic attributes (e.g., age group, sex/gender, geography, education/income-related indicators),

(2) health status and chronic-condition indicators, and

(3) lifestyle and behavioral factors (e.g., smoking and physical activity). Many fields are stored as numeric codes and include special response values (e.g., “valid skip”, “don’t know”, “refused”, “not stated”).

We will use the accompanying codebook to map coded values to human-readable categories and to convert non-substantive codes into NA/“Unknown” before building the visualizations.

Given the large number of columns, we will focus on a smaller set of variables that supports our dashboard’s main goal: **exploring how key health outcomes vary across population groups and behaviors.** Our planned visualizations will emphasize differences in outcome distributions across age/sex/region and their association with lifestyle factors (especially smoking and physical activity). We will also derive a small number of new variables to simplify interpretation, such as standardized “Unknown/NA” categories, grouped activity levels derived from activity frequency/time fields, and summary indicators (e.g., a count or composite index of selected health risk factors/conditions) where appropriate.

------------------------------------------------------------------------

## Research Questions and Usage Scenarios

***Research Questions ( 6 total)***

- How do `Total_physical_act_time` and `Fruit_veg_con` relate to `Stress_level` and `Mental_health_state` across `Age`, `Gender`, and `Province`?
- Which `Age × Province × Gender` segments show the highest prevalence of key chronic conditions (`High_BP`, `Diabetic`, `Mood_disorder`, `Anxiety_disorder`), and how do their `Stress_level` profiles differ?
- Does higher physical activity moderate the negative association between elevated `Stress_level` and `Life_satisfaction`?
- How do `BMI_18_above` categories pair with chronic conditions and `Stress_level`, and is regular `Physical_vigorous_act_time` protective within each BMI group?
- Which provinces or age groups combine low physical activity with poor `Mental_health_state` and lower `Life_satisfaction`, indicating priority regions for intervention?
- Among income brackets, how do physical activity and diet together predict `Stress_level` and `Mental_health_state`, and do patterns differ by `Gender`?

***Usage Scenarios (supported by current filters/plots)***

- **Policy analysts** filter by `Province`, `Age`, and `Gender` to spot areas where low activity and high stress coincide with poorer mental health and chronic conditions.
- **Clinic managers** use the activity and diet filters to flag cohorts with higher hypertension/diabetes prevalence and plan preventive outreach.
- **Mental health leads** contrast stress vs life satisfaction in the bubble/scatter views to target stress-reduction programs for high-stress segments.
- **Population health teams** compare BMI categories with chronic conditions to prioritize physical-activity interventions where risk is highest.
