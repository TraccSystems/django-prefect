from prefect import flow,task
import csv
from requests_html import HTMLSession
from datetime import datetime
import boto3
import os
import glob
import datetime
from prefect import flow, task
from prefect.blocks.system import JSON
from prefect_aws.s3 import S3Bucket,s3_download,s3_upload,s3_list_objects
from . digital_ocean_block import DigitalOceanCredential,PostGresCredential
from typing import Optional

region_name='nyc3',
endpoint_url='https://nyc3.digitaloceanspaces.com',
aws_access_key_id='DO003MHYBNBDRQFMYKCV',
aws_secret_access_key='5H60lnPWHgWeSgx7548erltDaoYT9Zt/co9oRJu0ujg',
bucket_name ="scrap_data"

@task(name='pull_data_from_s3_write_to_postgress')
def pull_data_from_s3(credential_name:str):
    data = DigitalOceanCredential.load(name=credential_name)

@task(name='write_data_to_postgress')
def write_data_to_postgress(credential_name: str):
  data = PostGresCredential.load(name=credential_name)


 #pull data from s3 to posgress
@flow(name='pull_data_from_s3_write_to_postgress')
async def pull_data_from_s3_write_to_postgress(s3credential_name,posgres_crendential_name):
    s3data = await DigitalOceanCredential.load(name=s3credential_name)
    postgresdata = await PostGresCredential.load(name=posgres_crendential_name)
    print("writing to destination file......")

    return s3data,postgresdata

@flow(name="write_data_to_pogress")
def write_data_to_postgress(data):
    print("..wrting data")

@flow(name="download_file_from_s3_upload_to_postgres")
def download_file_from_s3_upload_to_postgres():
    digital_credential = DigitalOceanCredential(
        aws_access_key_id='DO003MHYBNBDRQFMYKCV',
        aws_secret_access_key='5H60lnPWHgWeSgx7548erltDaoYT9Zt/co9oRJu0ujg',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        region_name='nyc3'
    )





@flow(name='save_asw_credentials')
def save_asw_credentials(aws_access_key_id, aws_secret_access_key,endpoint_url,region_name,name):
    digital_credential = DigitalOceanCredential(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name
    )
    digital_credential.save(name,overwrite=True)

@flow(name='save_progres_credentials')
def save_progres_credentials(database_name,host,password,
                             port,username):
    postgress_credential = PostGresCredential(
                 database_name=database_name,
                 host=host,password=password,port=port,
                 username=username
            )
    postgress_credential.save(database_name,overwrite=True)
    

    



