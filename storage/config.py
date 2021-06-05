import os
from os import listdir
from os.path import isfile, join
from google.cloud import storage
from config import bucketName, bucketFolder, localFolder

# Google Cloud Storage 
bucketName = os.environ.get('GCP_BUCKET_NAME')
bucketFolder = os.environ.get('GCP_BUCKET_FOLDER_NAME')


storage_client = storage.Client.from_service_account_json('storage-config.json')
bucket = storage_client.get_bucket(bucketName)

# Data
localFolder = os.environ.get('LOCAL_FOLDER')

def upload_files(bucket_name):
    '''File upload to Bucket'''
    files = [f for f in listdir(localFolder) if isfile(join(localFolder, f))]
    for file in files:
        localFile = localFolder + file
        blob = bucket.blob(bucketFolder + file)
        blob.upload_from_filename(localFile)
    return f'Uploaded {files} to "{bucketName}" bucket.'

def list_files(bucketName):
    '''List all files in GCP bucket.'''
    files = bucket.list_blobs(prefix=bucketFolder)
    fileList = [file.name for file in files if '.' in file.name]
    return fileList
