import requests
import zipfile
import datetime
from google.cloud import storage
from google.oauth2 import service_account
import os
import sys

def download_file(url):
    """ Download a file from a URL and return the path to the local file. """
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def unzip_file(zip_path, extract_to):
    """Unzip a zip file."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {zip_path} to {extract_to}")


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """ Uploads a file to the Google Cloud Storage bucket. """
    # Set up Google Cloud credentials
    credentials = service_account.Credentials.from_service_account_file(
        'service-account-file.json'
    )
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def get_file_type_url(current_time, file_type):
    """ Generate the URL based on the current time and file type. """
    link = f"http://data.gdeltproject.org/gdeltv2/{current_time}.{file_type}.CSV.zip"

    if file_type == 'gkg':
        return link.lower()

    return link

def main(time_stamp, file_type):
    url = get_file_type_url(time_stamp, file_type)
    local_file = download_file(url)
    destination_name = f"{file_type}_{time_stamp}.csv"
    unzip_file(local_file, destination_name)
    upload_to_gcs("gdelt_raw_data_bucket", 'export_20240415190000.csv/20240415190000.export.CSV', destination_name)
    os.remove(local_file)  # Clean up the local file after upload

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <time_stamp> <type>")
        sys.exit(1)

    time_stamp = sys.argv[1]  # e.g., '20240415190000'
    file_type = sys.argv[2]   # e.g., 'export'
    main(time_stamp, file_type)
