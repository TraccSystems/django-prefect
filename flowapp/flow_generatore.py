from prefect import flow,task
from prefect.deployments import Deployment
from prefect_aws.s3 import S3Bucket



def s3_to_pincone_flow(user=None,aws_access_key=None,aws_secrete_access=None,key=None,
                       bucket_name=None,file_type=None,pincone_index_name=None,pinecone_environment=None,pinecone_api_key=None):
    
    templates = f"""
from datetime import datetime
import boto3
import os
import boto3 
import os 
from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.text_splitter import CharacterTextSplitter 
from langchain.document_loaders import S3FileLoader,S3DirectoryLoader
from langchain.document_loaders.unstructured import UnstructuredFileLoader 
import tempfile 
from langchain.vectorstores import Pinecone 
import pinecone 
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.filesystems import S3
    
os.environ["AWS_ACCESS_KEY_ID"] = "{aws_access_key}"
os.environ["AWS_SECRET_ACCESS_KEY"] = "{aws_secrete_access}"

    
# load document form s3 space bucket func
def load_external_document(bucket_name=None,prefix=None):

        loader = S3DirectoryLoader(bucket=bucket_name,prefix=prefix)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        
        return texts

@flow(name='pull_data_from_s3_write_to_pincone',retries=2,description="pull data from s3 write to pincone")
def pull_data_from_s3_write_to_pincone():
        documents = load_external_document(bucket_name='{bucket_name}',prefix='{key}.{file_type}')
        embeddings = OpenAIEmbeddings(openai_api_key="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")
    
        #embedding document to pinecone..........
        pinecone.init(
            api_key='{pinecone_api_key}',  # find at app.pinecone.io
            environment='{pinecone_environment}',  # next to api key in console
        )

        index_name='{pincone_index_name}'
        Pinecone.from_documents(documents, embeddings, index_name=index_name)
    
    
    


    
if __name__ == "__main__":
    pull_data_from_s3_write_to_pincone()

            """

    with open("pinecone_user_flow.py",'w') as file:
        file.write(templates)
    
    try:
     from pinecone_user_flow import pull_data_from_s3_write_to_pincone
    except:
        pass
   

    storage = S3Bucket.load("s3-connection")
    deployment = Deployment.build_from_flow(
    flow=pull_data_from_s3_write_to_pincone,    
    name="pull_data_from_s3_write_to_pincone",
    work_pool_name ="useflow-pool",
    version="1",
    tags=["pincone"],
    storage=storage,
    entrypoint ="pinecone_user_flow.py:pull_data_from_s3_write_to_pincone",
    apply=True,
    ignore_file ='.prefectignore',
    description="pull data from s3 write to pincone"
        )  
    deployment.apply()




def s3_to_singleStore_flow(user=None,aws_access_key=None,aws_secrete_access=None,
                       bucket_name=None,file_type=None,singledb_url=None,table_name=None):
    
    templates = f"""


import os
import boto3 
from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.text_splitter import CharacterTextSplitter 
from langchain.document_loaders import S3FileLoader,S3DirectoryLoader
from langchain.document_loaders.unstructured import UnstructuredFileLoader 
from langchain.vectorstores import SingleStoreDB
from prefect import flow, task 
from prefect.deployments import Deployment
from prefect.filesystems import S3

os.environ["AWS_ACCESS_KEY_ID"] = "{aws_access_key}"
os.environ["AWS_SECRET_ACCESS_KEY"] = "{aws_secrete_access}"
    


# load document form s3 space bucket func
def load_external_document(bucket_name=None,prefix=None):

        loader = S3DirectoryLoader(bucket=bucket_name,prefix=prefix)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        
        return texts

@flow(name='pull_data_from_s3_write_to_singleStore',retries=2,description="pull data from s3 write to singleStore")
def pull_data_from_s3_write_to_singleStore():
        documents = load_external_document(bucket_name='{bucket_name}',prefix=f'{aws_secrete_access}.{file_type}')
        embeddings = OpenAIEmbeddings(openai_api_key='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')
    
        #embedding document to SINGLESTOREDB..........
        os.environ["SINGLESTOREDB_URL"] = "{singledb_url}"

        docsearch = SingleStoreDB.from_documents(
            documents,
            embeddings,
            table_name="{table_name}",  # use table with a custom name
        )


    
    


    
if __name__ == "__main__":
   pull_data_from_s3_write_to_singleStore()
            """

    with open("singleStore_user_flow.py",'w') as file:
        file.write(templates)
    try:
     from singleStore_user_flow import pull_data_from_s3_write_to_singleStore
    except:
        pass
    
  #/ flow deployment and upload to s3
    storage = S3Bucket.load("s3-connection")
    deployment = Deployment.build_from_flow(
    flow=pull_data_from_s3_write_to_singleStore,    
    name="pull_data_from_s3_write_to_singleStore",
    work_pool_name ="useflow-pool",
    version="1",
    tags=["singleStore"],
    storage=storage,
    entrypoint ="singleStore_user_flow.py:pull_data_from_s3_write_to_singleStore",
    apply=True,
    ignore_file ='.prefectignore',
    description="pull data from s3 write to singleStore"
        )  
    deployment.apply()
    












