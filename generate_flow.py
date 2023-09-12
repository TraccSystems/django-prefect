
from datetime import datetime
import boto3
import os
import boto3 
import os 
from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.text_splitter import CharacterTextSplitter 
## source loader
from langchain.document_loaders import S3FileLoader,S3DirectoryLoader
from langchain.document_loaders import AzureBlobStorageContainerLoader
from langchain.document_loaders import AzureBlobStorageFileLoader
from langchain.document_loaders import GitHubIssuesLoader
from langchain.document_loaders import GoogleDriveLoader
from langchain.document_loaders import NotionDBLoader
from langchain.document_loaders import SnowflakeLoader
from langchain.document_loaders import NotionDBLoader
from langchain.document_loaders.unstructured import UnstructuredFileLoader 
import tempfile 
### target
from langchain.vectorstores import Pinecone 
from langchain.vectorstores import Qdrant
from langchain.vectorstores import SingleStoreDB
from langchain.vectorstores import Weaviate
from langchain.vectorstores.elasticsearch import ElasticsearchStore
import pinecone
import weaviate 
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.filesystems import S3
        
os.environ["AWS_ACCESS_KEY_ID"] = "AKIARDTV5PYP5NLI7BJ4"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"

    
# load document form s3 space bucket func
def load_external_document(bucket_name=None,prefix=None):

        loader = S3DirectoryLoader(bucket=bucket_name,prefix=prefix)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

documents = load_external_document(
    bucket_name='developer-news-porter',
    prefix='articles/owolabi_accessKeys.csv')
            

@flow(name='owolabidevelop84@gmail.com_pull_data_from_source_to_target',retries=2,description="pull data from source write to pincone")
def pull_data_from_source_to_target():
    
    embeddings = OpenAIEmbeddings(openai_api_key="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")

    #embedding document to pinecone..........
    pinecone.init(
        api_key='788fc40b-a4bd-40b6-b4c5-6d02ae274428',  
        environment='us-west4-gcp-free',
    )

    index_name='scrap-data'

    if index_name not in pinecone.list_indexes():
    # we create a new index
      pinecone.create_index(
      name=index_name,
      metric='cosine',
      dimension=1536)
    Pinecone.from_documents(documents, embeddings, index_name=index_name)

                
if __name__ == "__main__":
    pull_data_from_source_to_target()

                        