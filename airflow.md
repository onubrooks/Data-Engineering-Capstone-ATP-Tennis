# Tennis ETL DAG

## Overview

The Airflow DAG orchestrates the extraction, transformation, and loading of tennis data from raw sources to a PostgreSQL database and Google BigQuery. It also performs data cleaning and uploads parquet files to Google Cloud Storage.

<img width="1201" alt="Airflow DAG" src="https://github.com/onubrooks/Data-Engineering-Capstone-ATP-Tennis/assets/26160845/116be332-bc0a-40eb-9c21-dfbe1ac37854">


## Dependencies

- Airflow
- Postgres
- Google Cloud Storage
- Google BigQuery
- dbt Cloud

## Configuration

1. Set environment variables for database connection details:

   ```python
   export PG_HOST=<postgres_host>
   export PG_USER=<postgres_user>
   export PG_PASSWORD=<postgres_password>
   export PG_PORT=<postgres_port>
   export PG_DATABASE=<postgres_database>
   ```

2. Set environment variables for Google Cloud resources:

   ```python
   export GCP_PROJECT_ID=<project_id>
   export GCP_GCS_BUCKET=<gcs_bucket>
   ```

3. Set environment variable for dbt Cloud job ID:

   ```python
   export DBT_JOB_ID=<dbt_job_id>
   ```

## DAG Tasks

1. **Extract files:** Downloads raw data files from the specified URL to the `downloads` directory using the BashOperator and the `wget` utility.

2. **Transform to parquet:** Converts downloaded CSV files to parquet format for efficient data processing.

3. **Drop and create tennis database:** Drops and recreates the `atp_tennis_2000_2022` database in PostgreSQL.

4. **Clean and load:** Loads the transformed parquet files into the `atp_tennis_2000_2022` database, performing data cleaning and normalization.

5. **Upload to GCS:** Uploads the transformed parquet files to the specified Google Cloud Storage bucket.

6. **Create table players:** Creates a BigQuery table `atp_tennis_data.atp_players` from the corresponding parquet files in GCS.

7. **Create table matches:** Creates a BigQuery table `atp_tennis_data.atp_matches` from the corresponding parquet files in GCS.

8. **Create table rankings:** Creates a BigQuery table `atp_tennis_data.atp_rankings` from the corresponding parquet files in GCS.

9. **Run dbt job:** Runs the specified dbt Cloud job to perform additional transformations or data quality checks (requires a paid dbt Cloud account or the 2 week free trial to use the API).

10. **Delete files:** Removes the downloaded raw data files from the `downloads` directory to conserve storage space.

## Schedule

This DAG is currently configured to run once manually. You can modify the `schedule_interval` parameter in the DAG definition to schedule it for regular execution.

## Monitoring

The DAG can be monitored in the Airflow web UI. You can also set up email alerts to be notified of DAG failures or successes.
