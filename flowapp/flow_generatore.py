from prefect import flow,task
from prefect.deployments import Deployment
from prefect_aws.s3 import S3Bucket



def s3_to_pincone_flow(user=None,aws_access_key=None,aws_secrete_access=None,aws_endpoint_url=None,
                       bucket_name=None,aws_region=None,pincone_index_name=None,pinecone_environment=None,pinecone_api_key=None):
    
    templates = f"""
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

    def __init__(self, bucket: str, key: str, space_key:str,space_secrete:str):\n
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
        region_name='{aws_region}',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        aws_access_key_id=self.space_key,
        aws_secret_access_key=self.space_secrete
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{{temp_dir}}/{{self.key}}"
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
        return docs \n
    
# load document form s3 space bucket func
def load_external_document(space_key=None,space_secret=None):

        current_date = datetime.today().strftime("%A-%d-%B-%Y")

        folder_name ='latestArticles' 
        prefix = f"{{folder_name}}_" + current_date  # to load latest article from s3 with current date
        loader = S3DirectoryLoader_space('{bucket_name}',space_key,space_secret, prefix=prefix)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        print(len(documents))
        return texts

@flow(name='pull_data_from_s3_write_to_pincone',retries=2,description="pull data from s3 write to pincone")
def pull_data_from_s3_write_to_pincone():
        documents = load_external_document('{aws_access_key}','{aws_secrete_access}')
        embeddings = OpenAIEmbeddings()
    
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




def s3_to_singleStore_flow(user=None,aws_access_key=None,aws_secrete_access=None,aws_endpoint_url=None,
                       bucket_name=None,aws_region=None,singledb_url=None,table_name=None):
    
    templates = f"""
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
from langchain.vectorstores import SingleStoreDB
import pinecone 
from prefect import flow, task 
from prefect.deployments import Deployment
from prefect.filesystems import S3
    

## base document load for s3 bucket class
class S3FileLoader_space(BaseLoader):
##Loading logic for loading documents from s3

    def __init__(self, bucket: str, key: str, space_key:str,space_secrete:str):\n
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
        region_name='{aws_region}',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        aws_access_key_id=self.space_key,
        aws_secret_access_key=self.space_secrete
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{{temp_dir}}/{{self.key}}"
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
        prefix = f"{{folder_name}}_" + current_date  # to load latest article from s3 with current date
        loader = S3DirectoryLoader_space('{bucket_name}',space_key,space_secret, prefix=prefix)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        print(len(documents))
        return texts

@flow(name='pull_data_from_s3_write_to_singleStore',retries=2,description="pull data from s3 write to singleStore")
def pull_data_from_s3_write_to_singleStore():
        documents = load_external_document('{aws_access_key}','{aws_secrete_access}')
        embeddings = OpenAIEmbeddings()
    
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
    












