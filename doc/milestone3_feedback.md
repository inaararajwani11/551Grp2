# Milestone 3 - User Feedback Report

## 1. Feedback Questions

We presented the Healthcare Survey Analysis Dashboard to two groups of peers and collected feedback on the following aspects:

### Evaluation Questionnaire

**A. Ease of Navigation**
1. How easy is it to navigate between different sections of the dashboard? (1-5 scale, 5 being the highest)
2. Is the placement and layout of filters intuitive?

**B. Interactivity**
3. Are interactive elements (such as filters and hover tooltips) useful and intuitive? (1-5 scale)
4. Can you easily explore different data combinations?

**C. Performance**
5. How would you rate the loading speed and responsiveness of the dashboard? (1-5 scale)
6. Is there noticeable delay when switching filters?

**D. Visual Appeal**
7. Is the visual design of the charts clear and easy to understand? (1-5 scale)
8. Do the color choices and layout help in understanding the data?

**E. Data Clarity**
9. Do chart titles and labels clearly convey information? (1-5 scale)
10. Can you quickly understand what each chart is trying to show?

**F. Feature Expectations**
11. What features do you expect to see that are currently missing?
12. As a health researcher/policymaker, what additional information do you need?

**G. Open-ended Questions**
13. What do you like most about the dashboard?
14. What do you think needs the most improvement?
15. Any other suggestions or comments?

---

## 2. Received Feedback

### Group A Feedback (Data Visualization Team)

**Participant Background:** 3 MDS students with experience in data visualization and public health data analysis

**Rating Feedback:**
- Ease of Navigation: 4/5
- Interactivity: 3/5
- Performance: 4/5
- Visual Appeal: 3/5
- Data Clarity: 3/5

**Detailed Feedback:**

1. **Navigation and Layout**
   - The left-side filter panel is well-positioned, but feels crowded when there are many filter options
   - Suggest grouping filters or using collapsible sections for better organization

2. **UI Aesthetics**
   - Overall interface design is rather plain and lacks a modern feel
   - Recommend optimizing card design by adding shadows or borders to enhance visual hierarchy
   - Chart spacing could be more consistent, and whitespace handling could be more refined
   - Title and text font hierarchy is not prominent enough

3. **Chart Comprehension**
   - Chart 3 (heatmap) axis labels are not clear enough; it takes careful examination to understand what the axes represent
   - Scatter plot points overlap when there are too many; suggest adding transparency or jitter

4. **Interactive Features**
   - Would like to click on elements in one chart and have other charts highlight related data
   - Missing a "reset all filters" shortcut button

5. **Data Display**
   - The ranking panel is useful, but would like to see specific values rather than just rankings
   - Suggest adding data download functionality for further analysis

6. **Favorite Aspects**
   - The grouped bar chart (Chart 4) showing the relationship between food security and sense of belonging is very intuitive
   - Overall color scheme is professional and easy to read

7. **Most Needs Improvement**
   - Add more explanatory text for charts to explain the research significance of each visualization
   - Legend placement in some charts is not prominent enough
   - UI design needs to be more modern to improve overall aesthetics

---

### Group B Feedback (Health Informatics Team)

**Participant Background:** 2 MDS students, 1 with public health policy background

**Rating Feedback:**
- Ease of Navigation: 4/5
- Interactivity: 4/5
- Performance: 3/5
- Visual Appeal: 3/5
- Data Clarity: 4/5

**Detailed Feedback:**

1. **Performance Issues**
   - Initial loading time is long (approximately 5-7 seconds)
   - Slight delay when updating charts after selecting multiple filters

2. **UI Design and Layout**
   - Overall interface is functional, but visual design is somewhat simple
   - Suggest adding design elements such as gradient backgrounds, icons, etc., to enhance visual appeal
   - Dashboard title and page header could be more prominent
   - Separation between filter panel and chart area could be clearer

3. **Feature Suggestions**
   - Would like to compare data across different provinces or age groups (side-by-side comparison view)
   - Suggest adding time series analysis (if data includes temporal dimension)

4. **Accessibility**
   - Recommend adding alt text descriptions for charts
   - Color contrast is generally good, but suggest checking for color-blind friendliness

5. **User Experience**
   - Filter default values are unclear whether they are "all selected" or "none selected"
   - Suggest displaying the current selected data volume or percentage next to filters

6. **Content Depth**
   - Bubble chart (Chart 5) bubble size meaning is not clear enough; needs clearer legend explanation
   - Would like to see statistical significance indicators (such as p-values or confidence intervals)

7. **Favorite Aspects**
   - Dashboard's overall design is professional and suitable for presenting to policymakers
   - Multi-dimensional filtering functionality is powerful, allowing deep exploration of health disparities across different populations

8. **Most Needs Improvement**
   - Add brief usage guide or tutorial (could be a pop-up tour)
   - Consider adding a "key findings" summary panel to highlight the most important health inequalities
   - Improve UI visual design to make the interface more attractive and modern

---

## 3. Reflection and Improvement Plan

Based on feedback from both groups, we plan to make the following improvements in Milestone 4:

### High Priority Improvements (Must Complete)

1. **Enhance Data Clarity**
   - Add clearer titles and axis labels to all charts
   - Add more detailed legend explanations for Chart 3 (heatmap) and Chart 5 (bubble chart)
   - Display specific values in the ranking panel

2. **Optimize Filter Experience**
   - Add a "reset all filters" button
   - Display current filtered data volume at the top of the filter panel
   - Group filters (demographics, health indicators, socioeconomic factors)

3. **Improve Chart Readability**
   - Add transparency to scatter plot to reduce point overlap
   - Adjust legend placement to ensure visibility in all charts
   - Check and optimize color scheme for color-blind friendliness

4. **Enhance UI Aesthetics**
   - Optimize overall layout to increase visual hierarchy (add card shadows, borders, etc.)
   - Improve title and text font hierarchy design
   - Unify chart spacing and whitespace to enhance overall refinement
   - Optimize visual separation between filter panel and chart area

### Medium Priority Improvements (Complete if Possible)

5. **Performance Optimization**
   - Optimize data loading logic to reduce initial loading time
   - Implement filter debouncing to reduce frequent updates

6. **Enhance User Guidance**
   - Add brief usage instructions at the top of the dashboard
   - Add brief explanatory text for each chart explaining its research significance

7. **Improve Accessibility**
   - Add descriptive text for all charts (can be tooltips or explanatory text)
   - Ensure keyboard navigation support

### Low Priority Improvements (If Time Permits)

8. **Advanced Features**
   - Explore feasibility of adding chart cross-highlighting functionality
   - Consider adding data export functionality (CSV format)
   - Research possibility of adding a "key findings" summary panel
   - Consider adding more visual design elements (such as gradient backgrounds, icons, etc.)

### Suggestions Not Included in This Iteration

- **Side-by-side comparison view**: Requires layout redesign, beyond current milestone scope
- **Time series analysis**: Dataset does not include temporal dimension
- **Statistical significance indicators**: Requires additional statistical analysis, beyond current project scope

---

## Summary

Both groups gave positive overall evaluations of the dashboard, particularly recognizing its professional visual design and powerful multi-dimensional filtering capabilities. Main improvement directions focus on:
1. Enhancing chart label and explanation clarity
2. Optimizing filter user experience
3. Improving performance and loading speed
4. Enhancing user guidance and accessibility
5. Improving UI interface aesthetics and modern feel

These improvements are all achievable and do not require large-scale code refactoring, making them suitable for completion in Milestone 4.

