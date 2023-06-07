import time
import boto3
import logging
import requests
import datetime

class MaxRetriesExceeded(Exception):
    pass

def request_headers():
    return {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

def request_payload(object_summary, request_id):
    return {
        "aws_request_id": request_id,
        "csv_file": object_summary
    }

def csv_processor_request(request_headers, request_payload, csv_processor_endpoint):
    max_retries = 4
    retry_delay = 2
    attempt = 0
    
    while attempt < max_retries:
        try:
            response = requests.post(csv_processor_endpoint, headers=request_headers, json=request_payload)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            attempt += 1
            if attempt < max_retries:
                logging.info(f'Retrying in {retry_delay**attempt} seconds...')
                time.sleep(retry_delay**attempt)
            else:
                raise MaxRetriesExceeded("Maximum number of retries exceeded")
    return None

def get_s3_resource(region_name, aws_access_key_id, aws_secret_access_key):
    s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key )
    return s3

def get_s3_objects_to_process(s3, bucket_name, bucket_url, months_to_process, days_to_process):
    objects_to_process = {month: [] for month in months_to_process}
    
    for month, days in days_to_process.items():
        for day in days:
            prefix = f'prod/2023/{month}/{day}/'
            bucket = s3.Bucket(bucket_name)
            for object_summary in bucket.objects.filter(Prefix=prefix):
                objects_to_process[month].append(f'{bucket_url}/{object_summary.key}')
    
    return objects_to_process

def main():
    aws_access_key_id = '' 
    aws_secret_access_key = ''
    region_name=''
    s3 = get_s3_resource(region_name, aws_access_key_id, aws_secret_access_key)
    bucket_name = ''
    bucket_url = f's3://{bucket_name}'
    csv_processor_endpoint = 'http://'

    months_to_process = [6]
    days_to_process = {
        6: [6]
    }

    objects_to_process = get_s3_objects_to_process(s3, bucket_name, bucket_url, months_to_process, days_to_process)
    
    request_id = 0
    count = 0
    for month, objects in objects_to_process.items():
        for objects_to_process in objects:
            request_id += 1
            headers = request_headers()
            payload = request_payload(objects_to_process, request_id)
            
            print(f'Request {request_id}: {payload}')
            response = csv_processor_request(headers, payload, csv_processor_endpoint)
            if response:
                print(f'Response {request_id}: {response.status_code}')
                print(f'Response {request_id}: {response.text}\n')
            else:
                print(f'No response {request_id}\n')

            count += 1
            if (count >= 10):
                count = 0
                time.sleep(120)
    
if __name__ == '__main__':
    main()
