from fastapi import FastAPI, File, Form, UploadFile
import boto3
from botocore.exceptions import NoCredentialsError

app = FastAPI()

@app.get("/")
def homepage():
    return "You Have Reached Home Page of the FastAPI Application"

@app.get("/getvpc")
def get_vpc_list(region: str):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_vpcs()
    vpc_id_list = [vpc['VpcId'] for vpc in response['Vpcs']]
    return vpc_id_list

@app.get("/s3")
def get_s3_buckets(region: str):
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_buckets()
    bucket_list = [bucket['Name'] for bucket in response['Buckets']]
    return bucket_list

def upload_file_to_s3(file_name, bucket_name, object_name=None, location="us-east-1"):
    s3_client = boto3.client('s3')
    try:
        # Check if the bucket exists, if not, create it
        if bucket_name not in [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]:
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': location})

        # If object_name is not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client.upload_file(file_name, bucket_name, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False
    return True

@app.post("/upload/")
async def upload_to_s3(bucket_name: str = Form(...), location: str = Form("us-east-1"), file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    success = upload_file_to_s3(file_location, bucket_name, file.filename, location)
    if success:
        return {"message": "File uploaded successfully"}
    else:
        return {"message": "File upload failed"}
