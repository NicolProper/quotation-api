# custom_storage.py

from storages.backends.s3boto3 import S3Boto3Storage

class AnotherBucketS3Boto3Storage(S3Boto3Storage):
    bucket_name = 'properworkshop'  # Cambia esto por el nombre de tu otro bucket
