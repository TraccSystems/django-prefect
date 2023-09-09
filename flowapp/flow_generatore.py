from prefect import flow,task
from prefect.deployments import Deployment
from prefect_aws.s3 import S3Bucket
from prefect.server.schemas.schedules import CronSchedule
import datetime



def generate_flow(user=None, 
                  source=None, 
                  target=None,
                  source_credentials=dict,
                  target_credentials=dict,
                  time_zone=None,
                  scheduel_time=None,
                  day_or=True
                  ):

    templated_code = {

    "S3": {"function_name": "load_external_document()",
            "code": f"""
os.environ["AWS_ACCESS_KEY_ID"] = "{source_credentials.get('aws_access_key')}"
os.environ["AWS_SECRET_ACCESS_KEY"] = "{source_credentials.get('aws_secret_access_key')}"

    
# load document form s3 space bucket func
def load_external_document(bucket_name=None,prefix=None):

        loader = S3DirectoryLoader(bucket=bucket_name,prefix=prefix)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

documents = load_external_document(
    bucket_name='{source_credentials.get('bucket_name')}',
    prefix='{ source_credentials.get('prefix')}.{source_credentials.get('file_type')}')
            """
              },

    "Github":{
        "function_name":"load_external_document()",
        "code":f"""
def load_external_document(repo=None,access_token=None,creator=None,include_prs=False):

        loader = GitHubIssuesLoader(
        repo=repo,
        acccess_token=access_token,
        creator=creator,
        include_prs=include_prs
        )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

documents = load_external_document(
    repo={source_credentials.get('repo')},
   access_token={source_credentials.get('access_token')},
   creator={source_credentials.get('cretor')},
   include_prs=False)
            
                """
    },

    "Notion":{
        "function_name":"load_external_document()",
        "code":f"""
def load_external_document(integration_token = None,database_id=None,request_timeout_sec=None):

        loader =  NotionDBLoader(
            integration_token = integration_token,
            database_id= database_id,
            request_timeout_sec=request_timeout_sec)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

documents = load_external_document(
    integration_token={source_credentials.get('integration_token')},
    database_id={source_credentials.get('database_id')},
    request_timeout_sec={source_credentials.get('request_timeout_sec')})
            
                """
    },


    
    "Googledrive":{
        "function_name":"load_external_document()",
        "code":f"""
def load_external_document(gdrive_api_file=None,
    folder_id=None,
    recursive=False,
    template=None,
    query=None,
    num_results=None,
    supportsAllDrives=False):

        loader = GoogleDriveLoader(
                        folder_id=folder_id,
                        recursive=recursive,
                        template=template,  
                        query=query,
                        num_results=num_results,            
                        supportsAllDrives=supportsAllDrives
        )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

documents = load_external_document(
   gdrive_api_file={source_credentials.get('gdrive_api_file')},
   folder_id={source_credentials.get('folder_id')},
   recursive={source_credentials.get('recursive')},
   template={source_credentials.get('template')},
   query={source_credentials.get('query')},
   num_results={source_credentials.get('num_result')},
   supportsAllDrives={source_credentials.get('supportsAllDrives')})
            
                """
    },


     "AzureblobStorage":{
        "function_name":"load_external_document()",
        "code":f"""
def load_external_document(conn_str=None,container=None,blob_name=None):

        loader =  AzureBlobStorageFileLoader(
                    conn_str=conn_str,
                    container=container,
                    blob_name=blob_name,
                                )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

documents = load_external_document(
    conn_str={source_credentials.get('conn_str')},
    container={source_credentials.get('container')},
    blob_name={source_credentials.get('blob_name')})
            
                """
    },

    "AzureblobContainer":{
        "function_name":"load_external_document()",
        "code":f"""
def load_external_document(conn_str=None,container=None):

        loader =  AzureBlobStorageContainerLoader(
                    conn_str=conn_str,
                    container=container,
                                )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

documents = load_external_document(
    conn_str={source_credentials.get('conn_str')},
    container={source_credentials.get('container')}
    )
            
                """
    },

    "Snowflake":{
        "function_name":"load_external_document()",
        "code":f"""
def load_external_document(query=None,
                    user=None,
                    password=None,
                    account=None,
                    warehouse=None,
                    role=None,
                    database=None,
                    schema=None,):

        loader = SnowflakeLoader(
                    query=query,
                    user=user,
                    password=password,
                    account=account,
                    warehouse=warehouse,
                    role=role,
                    database=database,
                    schema=schema,
                )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

documents = load_external_document(
                    query={source_credentials.get('query')},
                    user={source_credentials.get('user')},
                    password={source_credentials.get('password')},
                    account={source_credentials.get('account')},
                    warehouse={source_credentials.get('warehouse')},
                    role={source_credentials.get('role')},
                    database={source_credentials.get('database')},
                    schema={source_credentials.get('schema')}
                    )
            
                """
    },



    "postgres": {"function_name": "extract_postgres()",
                "code": """
                """},



    "Pinecone": {"function_name": "pull_data_from_source_to_target()",
                "code": f"""

@flow(name='pull_data_from_source_to_pincone',retries=2,description="pull data from source write to pincone")
def pull_data_from_source_to_target():
    
    embeddings = OpenAIEmbeddings(openai_api_key="{target_credentials.get('openai_api_key')}")

    #embedding document to pinecone..........
    pinecone.init(
        api_key='{target_credentials.get('api_key')}',  
        environment='{target_credentials.get('environment')}',
    )

    index_name='{target_credentials.get('index_name')}'

    if index_name not in pinecone.list_indexes():
    # we create a new index
      pinecone.create_index(
      name=index_name,
      metric='cosine',
      dimension=1536)
    Pinecone.from_documents(documents, embeddings, index_name=index_name)

                """
                },



    "SingleStoreDB": {"function_name": "pull_data_from_source_to_target()",
                    "code": f"""

@flow(name='pull_data_from_source_to_singleStore',retries=2,description="pull data from source write to singleStore")
def pull_data_from_source_to_target():
    embeddings = OpenAIEmbeddings(openai_api_key='{target_credentials.get('openai_api_key','unknown')}')

    #embedding document to SINGLESTOREDB..........
    os.environ["SINGLESTOREDB_URL"] = "{target_credentials.get('SINGLESTOREDB_URL','unknown')}"

    SingleStoreDB.from_documents(documents,embeddings,table_name="{target_credentials.get('table_name','unknow')}")
                   """
                    
                   },

    
    "Elasticsearch": {"function_name": "pull_data_from_source_to_target()",
                    "code": f"""
@flow(name='pull_data_from_source_to_elasticsearch',retries=2,description="pull data from source write to elasticsearch")
def pull_data_from_source_to_target():
    embeddings = OpenAIEmbeddings(openai_api_key='{target_credentials.get('openai_api_key','unknown')}')

    #embedding document to ElasticsearchStore..........
    ElasticsearchStore.from_documents(
        documents, 
        embeddings, 
        es_url="{target_credentials.get('es_url',None)}", 
        index_name="{target_credentials.get('index_name',None)}",
        distance_strategy="COSINE",
        distance_strategy="EUCLIDEAN_DISTANCE",
        distance_strategy="DOT_PRODUCT",
    )
                   """
                    
                   },

    "Qdrant": {"function_name": "pull_data_from_source_to_target()",
                    "code": f"""
@flow(name='pull_data_from_source_to_qdrant',retries=2,description="pull data from source write to qdrant")
def pull_data_from_source_to_target():
    embeddings = OpenAIEmbeddings(openai_api_key='{target_credentials.get('openai_api_key','unknown')}')

    #embedding document to qdrant..........
    Qdrant.from_documents(
            documents,
            embeddings,
            url={target_credentials.get('url')},
            prefer_grpc={target_credentials.get('prefer_grpc')},
            api_key={target_credentials.get('api_key')},
            collection_name={target_credentials.get('collection_name')},
        )
                   """
                    
                   },
        
        
    "Weaviatdb": {"function_name": "pull_data_from_source_to_target()",
                    "code": f"""
@flow(name='pull_data_from_source_to_weaviatdb',retries=2,description="pull data from source write to weaviatdb")
def pull_data_from_source_to_target():
    embeddings = OpenAIEmbeddings(openai_api_key='{target_credentials.get('openai_api_key','unknown')}')
    client = weaviate.Client(url={target_credentials.get('WEAVIATE_URL')}, 
    auth_client_secret=weaviate.AuthApiKey({target_credentials.get('WEAVIATE_API_KEY')}))

    #embedding document to weaviatedb..........
    Weaviate.from_documents(documents, embeddings, client=client, by_text=False)
                   """
                    
                   }
                   
}


    
    base_template_start = """
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
        """

    base_template_end = """
if __name__ == "__main__":
    {target_function}

                        """.format(source_function=templated_code[source]["function_name"],
                                    target_function=templated_code[target]["function_name"])


    source_code = templated_code[source]["code"]

    target_code = templated_code[target]["code"]

    with open("generate_flow.py",'w+') as file:
        file.write(base_template_start)
        file.write(source_code)
        file.write(target_code)
        file.write(base_template_end)
    try:
      from generate_flow import  pull_data_from_source_to_target
    except:
       pass
    
    storage = S3Bucket.load("s3-connection")
    deployment = Deployment.build_from_flow(
    flow = pull_data_from_source_to_target,   
    name="traccflows",
    work_pool_name ="useflow-pool",
    version="1",
    tags=["pincone"],
    storage=storage,
    entrypoint =f"generate_flow.py:{templated_code[target]['function_name'].split('()')[0]}",
    apply=True,
    schedule=(CronSchedule(cron=f"{scheduel_time.minute} {scheduel_time.hour} {scheduel_time.day} {scheduel_time.month} *", timezone=time_zone,day_or=day_or)),
    ignore_file ='.prefectignore',
    description="pull data from sources write to target"
        )  
    
    deployment.apply()

      
    
    
    


source_credentials = {
    "aws_access_key": "AKIARDTV5PYP5NLI7BJ4",
    "aws_secret_access_key": "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",
    "bucket_name":"developer-news-porter",
    "prefix":"articles/owolabi_accessKeys",
    "file_type":"csv"
    # Add other credential values as needed
}

target_credentials ={
    'openai_api_key':'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',
    'api_key':'788fc40b-a4bd-40b6-b4c5-6d02ae274428',
    'environment':"us-west4-gcp-free",
    "index_name":"scrap-data"

}

### source functions


def s3_credentials(aws_access_key=None,aws_secret_access_key=None,bucket_name=None,prefix=None,file_type=None):
   source_credentials = {
    "aws_access_key": aws_access_key,
    "aws_secret_access_key":aws_secret_access_key,
    "bucket_name":bucket_name,
    "prefix":prefix,
    "file_type":file_type
   
    }
   return source_credentials



def googledrive_credentials(gdrive_api_file=None,folder_id=None,recursive=None,template=None,query=None,num_results=None,supportsAllDrives=None):
   source_credentials = {
    "gdrive_api_file": gdrive_api_file,
    "folder_id":folder_id,
    "recursive":recursive,
    "template":template,
    "query":query,
    "num_results":num_results,
    "supportsAllDrives":supportsAllDrives 
    }
   return source_credentials


def notion_credentials(integration_token=None,database_id=None,request_timeout_sec=None):
   source_credentials = {
    "integration_token":integration_token,
    "database_id":database_id,
    "request_timeout_sec":request_timeout_sec,
    }
   return source_credentials


def github_credentials(repo=None,access_token=None,creator=None,include_prs=False):
   source_credentials = {
    "repo":repo,
    "access_token":access_token,
    "creator":creator,
    "include_prs":include_prs,
    }
   return source_credentials



def azureblobstorage_credentials(conn_str=None,container=None,blob_name=None):
   source_credentials = {
    "conn_str":conn_str,
    "container":container,
    "blob_name":blob_name,
    }
   return source_credentials


def azureblobcontainer_credentials(conn_str=None,container=None):
   source_credentials = {
    "conn_str":conn_str,
    "container":container,
    }
   return source_credentials


def snowflake_credentials(query=None,user=None,password=None,account=None,warehouse=None,role=None,database=None,schema=None):
   source_credentials = {
    "query":query,
    "user":user,
    "password":password,
    "account":account,
    "warehouse":warehouse,
    "role":role,
    "database":database,
    "schema":schema

    }
   return source_credentials
   
   
   



###### target function .......
def pinecone_credentials(openai_api_key=None,api_key=None,environment=None,index_name=None):
   target_credentials ={
    'openai_api_key':openai_api_key,
    'api_key':api_key,
    'environment':environment,
    "index_name":index_name
    }
   return target_credentials



def qdrant_credentials(openai_api_key=None,api_key=None,url=None,collection_name=None,prefer_grpc=None):
   target_credentials ={
    'openai_api_key':openai_api_key,
    'api_key':api_key,
    'url':url,
    "collection_name":collection_name,
    "prefer_grpc":prefer_grpc
    }
   return target_credentials


def weaviatdb_credentials(openai_api_key=None,weaviate_url=None,weaviate_api_key=None):
   target_credentials = {
    'openai_api_key':openai_api_key,
    'WEAVIATE_API_KEY':weaviate_api_key,
    'WEAVIATE_URL':weaviate_url,
    }
   return target_credentials



def elasticsearch_credentials(openai_api_key=None,es_url=None,index_name=None):
   target_credentials = {
    'openai_api_key':openai_api_key,
    'es_url':es_url,
    'index_name':index_name,
    }
   return target_credentials


def singlestoredb_credentials(openai_api_key=None,singlestoredb_url=None,table_name=None):
   target_credentials = {
    'openai_api_key':openai_api_key,
    'SINGLESTOREDB_URL':singlestoredb_url,
    'table_name':table_name,
    }
   return target_credentials