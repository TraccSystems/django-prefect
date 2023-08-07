from typing import Optional
import boto3
from prefect.blocks.core import Block
from pydantic import SecretStr
import psycopg2


## block to save digitalocean data data
class DigitalOceanCredential(Block):
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[SecretStr] = None
    endpoint_url: Optional[str] = None
    region_name: Optional[str] = None
    _description = """
                  block to connect to digitalOcean aws space
            """

    def get_boto3_session(self):
        return boto3.client('s3',
                        region_name = self.region_name,
                        endpoint_url = self.endpoint_url,
                        aws_access_key_id = self.aws_access_key_id,
                        aws_secret_access_key = self.aws_secret_access_key
                        )



## block to save postgress data
class PostGresCredential(Block):
    database_name: Optional[str] = None
    host: Optional[str] = None
    password: Optional[SecretStr] = None
    port: Optional[str] = '5423'
    username: Optional[str] = None
    _description = """
                  block to connect to PostGres database
            """

    def get_postgress_connection(self):
        return psycopg2.connect(database=self.database_name,user=self.username,host=self.host,port=self.port)
