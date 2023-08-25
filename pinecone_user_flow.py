
from datetime import datetime
import boto3
import os
import boto3 
import os 
from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.text_splitter import CharacterTextSplitter 
from typing import List 
from langchain.docstore.document import Document 
from langchain.document_loaders.base import BaseLoader 
from langchain.document_loaders.unstructured import UnstructuredFileLoader 
import tempfile 
from langchain.vectorstores import Pinecone 
import pinecone 
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.filesystems import S3
    

## base document load for s3 bucket class
class S3FileLoader_space(BaseLoader):
##Loading logic for loading documents from s3

    def __init__(self, bucket: str, key: str, space_key:str,space_secrete:str):

        ##Initialize with bucket and key name
        self.bucket = bucket
        self.key = key
        self.space_key = space_key
        self.space_secrete = space_secrete

    def load(self) -> List[Document]:
        ##Load documents
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "Could not import `boto3` python package. "
                "Please install it with `pip install boto3`."
            )
        s3 = boto3.client("s3",
        region_name='ytryrt',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        aws_access_key_id=self.space_key,
        aws_secret_access_key=self.space_secrete
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/{self.key}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            s3.download_file(self.bucket, self.key, file_path)
            loader = UnstructuredFileLoader(file_path)
            return loader.load()

class S3DirectoryLoader_space(BaseLoader):
    ##Loading logic for loading documents from s3
    def __init__(self, bucket: str,space_key:str,space_secrete:str, prefix: str = "",):
        ##Initialize with bucket and key name.
        self.bucket = bucket
        self.prefix = prefix
        self.space_key = space_key
        self.space_secrete = space_secrete

    def load(self) -> List[Document]:
        ##Load documents
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "Could not import boto3 python package. "
                "Please install it with `pip install boto3`."
            )
        s3 = boto3.resource("s3",
        region_name='nyc3',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        aws_access_key_id=self.space_key,
        aws_secret_access_key=self.space_secrete
        )
        bucket = s3.Bucket(self.bucket)
        docs = []
        for obj in bucket.objects.filter(Prefix=self.prefix):
            loader = S3FileLoader_space(self.bucket, obj.key,self.space_key,self.space_secrete)
            docs.extend(loader.load())
        return docs 

    
# load document form s3 space bucket func
def load_external_document(space_key=None,space_secret=None):

        current_date = datetime.today().strftime("%A-%d-%B-%Y")

        folder_name ='latestArticles' 
        prefix = f"{folder_name}_" + current_date  # to load latest article from s3 with current date
        loader = S3DirectoryLoader_space('ytryt',space_key,space_secret, prefix=prefix)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        print(len(documents))
        return texts

@flow(name='pull_data_from_s3_write_to_pincone',retries=2,description="pull data from s3 write to pincone")
def pull_data_from_s3_write_to_pincone():
        documents = load_external_document('trt','yrty')
        embeddings = OpenAIEmbeddings()
    
        #embedding document to pinecone..........
        pinecone.init(
            api_key='1232435',  # find at app.pinecone.io
            environment='456464',  # next to api key in console
        )

        index_name='436457'
        Pinecone.from_documents(documents, embeddings, index_name=index_name)
    
    
    


    
if __name__ == "__main__":
    pull_data_from_s3_write_to_pincone()

            