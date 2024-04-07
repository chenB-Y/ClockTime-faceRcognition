import os
from boto3.session import Session
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()
session = Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

s3 = session.resource('s3')
bucket_name = 'chenfirstbucket'
bucket = s3.Bucket(bucket_name)
directory = './db/'

def importUsers():
    for s3_file in bucket.objects.all():
        object_key = s3_file.key
        local_file_path = f'{directory}{object_key}'
        if '.txt' in object_key:
            continue
        else:
            if not os.path.exists(local_file_path):
                print("Trying to download:", object_key)
                try:
                    # adding the user photo to the local file
                    bucket.download_file(object_key, local_file_path)
                    print("Download successful.")
                except ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        print(f"The object {object_key} does not exist in the bucket.")
                    else:
                        print(f"An error occurred: {e}")
            else:
                print(f"File already exists: {local_file_path}")


def uploadUsers(name):
    file_path = f"{directory}{name}.jpg"
    print(file_path)
    object_key = f'{name}.jpg'
    print(object_key)
    try:
        s3.meta.client.upload_file(file_path, bucket_name, object_key)
        print(f"File uploaded successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

def downloadAttendanceSheet():
    bucket.download_file('Attendance.txt','./log.txt')

def uploadAttendanceSheet():
    file_path = './log.txt'
    object_key = f'Attendance.txt'
    try:
        s3.meta.client.upload_file(file_path, bucket_name, object_key)
        print(f"File uploaded successfully")
    except Exception as e:
        print(f"An error occurred: {e}")