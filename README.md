# GDELT Global Events Analysis Project

## Project Overview

This data engineering project utilizes the GDELT 2.0 Event Database to provide comprehensive insights into international relations dynamics and to identify historically active periods, seasons, and dates. The objective is to analyze a vast repository of global event data to uncover patterns and trends in political and social behaviors across different timelines and geographies.

## Problem Statement

### Insights into International Relations Dynamics
The complexity of global interactions and events poses a challenge in understanding the changing dynamics of international relations. This project aims to decode these interactions by analyzing data on diplomatic exchanges, conflicts, and cooperation reported in the GDELT database. By processing and visualizing this data, we seek to provide actionable insights that can help policymakers, researchers, and the public understand current trends and historical changes in international relations.

### Identification of Active Historical Periods, Seasons, and Dates
Another critical aspect of this project is to identify key periods and dates that have historically been significant in terms of global events. This involves analyzing data to pinpoint seasons and specific dates when major events (like conflicts, treaties, or international summits) have occurred more frequently. These insights can assist historians, educators, and analysts in focusing their efforts on these significant times for further study or commemoration.

## Objectives
- **Data Analysis**: Leverage advanced data processing techniques to extract meaningful patterns and trends from the GDELT 2.0 Event Database.
- **Visualization**: Develop interactive visual tools to represent the data clearly and compellingly, making it accessible to a wide audience.
- **Trend Identification**: Use statistical and machine learning methods to identify significant periods of activity and notable trends in international relations.

## Technologies Used
- **Cloud Services**: Google Cloud Platform (GCP)
- **Data Processing**: Apache Spark
- **Infrastructure as Code**: Terraform
- **Workflow Orchestration**: Apache Airflow
- **Visualization Tools**: Data Looker Studio

## Data Pipeline Overview
1. **Data Extraction**: Retrieve GDELT event data from the site into a cloud storage bucket. Use Terraform to set up the infrastructure.
2. **Data Processing**: Transform raw data into warehouse using Apache Spark.
3. **Data Mart preparation**: Prepare data mart for visualization using Spark.
4. **Data Mart visualization**: Setup visualization in Looker Studio.
5. **Data Pipeline Orchestration**: Automate the pipeline using Cloud Composer.
6. **Documentation**: Add documentation to the project repository.
