# Architecture for ATP Tennis Data

## Introduction

This document describes the data engineering architecture and data flow for a project that analyzes historical ATP tennis world tour data from 2000 to 2022. The project aims to explore various aspects of the data, such as player performance, match outcomes, and tournament trends. The architecture is designed to be scalable, performant, and maintainable.

### Architecture Overview

The architecture consists of the following components:

1. **Data Sources:** he ATP Tennis Rankings, Results, and Stats repository on GitHub: This repository contains a comprehensive collection of ATP match results, player rankings, and biographical information. The data is provided in CSV format and spans from 1968 to the present. However, for this project, the focus is on a 20-year period between 2000 and 2019, using men's singles data on the ATP tour only (excluding doubles and ATP futures/challenger series).

2. **Data Ingestion:** The data ingestion pipeline is responsible for loading data from the data sources into a staging area. The pipeline uses a shell script and the bash airflow operator to load the data from the GitHub repository. The staging area is a temporary location where data is stored before it is processed. The staging area is used to ensure that the data is not corrupted or lost during the data processing pipeline.

3. **Data Transformation:** The data transformation pipeline is responsible for cleaning, transforming, and loading data into the data warehouse. The pipeline uses Apache Beam to load the data from the staging area into a parquet format. The parquet format is a columnar data format that is optimized for performance.

4. **Data Warehousing:** The data warehouse is used to store and analyze the transformed data. The data warehouse is implemented using Google BigQuery. BigQuery is a fully managed, serverless data warehouse that is scalable and performant.

5. **Data Modeling:** The data modeling stage uses dbt to create and manage data transformations in SQL. DBT helps to ensure that the data is transformed in a consistent and maintainable way.

### Data Flow

The data flow for the project is as follows:

1. Data is loaded from the GitHub repository into a staging area.
2. Data is loaded from the staging area into a parquet format.
3. The parquet data is loaded into a PostgreSQL database.
4. The parquet data is transformed and loaded into BigQuery.
5. Data is modeled in BigQuery using dbt.

The data modelling is designed to support a variety of analytical queries, such as:

1. Player performance analysis: Queries that analyze player performance, such as win-loss records, ranking history, and advanced match statistics.

2. Match outcome prediction: Queries that predict the outcome of matches based on historical data.

3. Tournament analysis: Queries that analyze tournament data, such as attendance trends, sponsorship revenue, and overall success.

### Architecture Diagram

The following diagram shows the architecture of the data pipeline:

![Architecture](https://github.com/onubrooks/Data-Engineering-Capstone-ATP-Tennis/assets/26160845/ecab89b5-6a36-4510-8eba-c8774b2dd5da)


### Conclusion

The data engineering architecture and data flow for the ATP Tennis Data project is designed to be scalable, performant, and maintainable. The architecture uses a variety of technologies, including Apache Beam, Google BigQuery, and dbt, to ensure that the data is processed and analyzed efficiently.
