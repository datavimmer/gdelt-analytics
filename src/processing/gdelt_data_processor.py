
import os
import sys
import zipfile
from pyspark.sql import SparkSession
from google.cloud import storage
from google.cloud.bigquery import Client, LoadJobConfig
from google.cloud.bigquery import SchemaField, WriteDisposition
from google.oauth2 import service_account

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)
    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def unzip_file(zip_path, extract_to):
    """Unzip a zip file."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {zip_path} to {extract_to}")

def create_spark_session():
    """Create and return a Spark session."""
    return SparkSession.builder \
        .appName("GDELT to BigQuery") \
        .getOrCreate()

def read_csv_to_df(spark, file_path):
    """Read CSV file into PySpark DataFrame."""
    return spark.read.csv(file_path, header=True, inferSchema=True)

def write_df_to_bigquery(df, dataset_table_name):
    """Write PySpark DataFrame to BigQuery."""
    bigquery_client = Client()
    job_config = LoadJobConfig(
        write_disposition=WriteDisposition.WRITE_APPEND,
        autodetect=True  # Use for the first time to automatically detect schema
    )
    df.write.format('bigquery') \
        .option('table', dataset_table_name) \
        .option('temporaryGcsBucket', 'gdelt_spark_data_bucket') \
        .mode('append') \
        .save()
    print(f"Data written to BigQuery table {dataset_table_name}")

def main(file_type):
    bucket_name = 'gdelt_raw_data_bucket'
    source_blob_name = f"{file_type}_{sys.argv[1]}.zip"
    destination_file_name = source_blob_name
    extract_to = "unzipped_data"

    download_blob(bucket_name, source_blob_name, destination_file_name)
    unzip_file(destination_file_name, extract_to)

    spark = create_spark_session()
    csv_file_path = os.path.join(extract_to, f"{source_blob_name[:-4]}.CSV")  # Assuming CSV after unzipping
    df = read_csv_to_df(spark, csv_file_path)

    bigquery_table = f"gdelt_dwh.{file_type}_info"
    write_df_to_bigquery(df, bigquery_table)

    # Clean up local files
    os.remove(destination_file_name)
    for root, dirs, files in os.walk(extract_to, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        os.rmdir(root)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <time_stamp> <type>")
        sys.exit(1)
    main(sys.argv[2])
