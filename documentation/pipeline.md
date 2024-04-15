# GDELT Data Processing Pipeline

## Overview

This document describes the GDELT Data Processing Pipeline built using Apache Airflow. The Global Database of Events, Language, and Tone (GDELT) is an open, big data platform of global human society for open research, which monitors the world's news media from nearly every corner of every country in print, broadcast, and web formats, in over 100 languages.

## Purpose

The purpose of this pipeline is to automate the daily extraction, processing, and storage of GDELT data. By structuring and analyzing this data, organizations can derive insights into global behavior, helping in decision-making processes for business, security, or research objectives.

## Pipeline Schedule

The pipeline is scheduled to run daily at 01:00 AM UTC. This schedule ensures that each day's data is processed in a timely manner, allowing for up-to-date analyses and reports.

## Tasks and Workflow

### Task List

1. **Start**: Initiates the DAG.
2. **Extract Tasks**:
   - **extract_exports**: Extracts "export" data using `gdelt_extractor.py`.
   - **extract_mentions**: Extracts "mentions" data using `gdelt_extractor.py`.
   - **extract_gkg**: Extracts "gkg" (Global Knowledge Graph) data using `gdelt_extractor.py`.
3. **Raw Data Collected**: Marker task indicating completion of data extraction.
4. **Process Tasks**:
   - **process_exports**: Processes "export" data using `gdelt_processor.py`.
   - **process_mentions**: Processes "mentions" data using `gdelt_processor.py`.
   - **process_gkg**: Processes "gkg" data using `gdelt_processor.py`.
5. **Create Datamart**: Runs SQL operations to update a data mart with processed data.
6. **Finish**: Completes the DAG.

### Task Dependencies

![Task Flow Diagram](path_to_diagram.png)  <!-- Generate a task flow diagram using Airflow's UI and replace path_to_diagram.png with the actual path -->

## Business Value

By automating the processing of GDELT data, this pipeline provides timely insights into global events, which can be invaluable for:
- Predicting economic shifts.
- Understanding geopolitical developments.
- Monitoring global media trends.
- Enhancing situational awareness for decision-makers.

## Insights Derived

From the processed GDELT data, various insights can be extracted:
- **Trend Analysis**: Identifying long-term changes in the occurrence of different types of global events.
- **Sentiment Analysis**: Assessing the tone and sentiment of global news coverage.
- **Network Analysis**: Understanding the relationships and influences among different actors or entities mentioned in the news.
- **Event Detection**: Spotting significant events as they are reported across the globe.

## Requirements

Ensure that Apache Airflow is set up correctly with access to necessary scripts and SQL files. The Python scripts `gdelt_extractor.py` and `gdelt_processor.py` should be correctly referenced in the DAG, and the SQL file `update_datamart.sql` should be available for the SQL task.

## Conclusion

The GDELT Data Processing Pipeline leverages Apache Airflow to provide robust, automated processing of global data, facilitating advanced analytics and insights into worldwide events and trends.
