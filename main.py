from fastapi import FastAPI
import os
import boto3
from dotenv import load_dotenv, find_dotenv
load_dotenv()

app = FastAPI()
@app.get("/")
def homepage():
    return "You Have Reached Home Page of the FastAPI Application"

@app.get("/getvpc")
def get_vpc_list(region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_vpcs()
    vpc_id_list = []
    for vpc in response['Vpcs']:  # Corrected the key here
        vpc_id_list.append(vpc['VpcId'])
    print(vpc_id_list)
    return vpc_id_list

@app.get("/s3")
def get_s3_buckets(region):
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_buckets()
    bucket_list = []
    for bucket in response['Buckets']:
        bucket_list.append(bucket['Name'])
    print(bucket_list)
    return bucket_list
