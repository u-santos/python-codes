import boto3
from datetime import datetime, timedelta

s3 = boto3.client('s3')
bucket_name = "lqd"
prefix = 'account/100192'

response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
objects = response.get('Contents', [])

total_files = len(objects)

print(total_files)

all_files_old = True

for obj in objects:
    object_key = obj['Key']
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    last_access_date = response['LastModified']

    diff = datetime.now() - last_access_date.replace(tzinfo=None)

    if diff.days <= 1095:
        all_files_old = False 
        break

if all_files_old:
    print("Todos os arquivos têm a última modificação há mais de 3 anos.")
else:
    print("Alguns arquivos têm a última modificação há menos de 3 anos.")