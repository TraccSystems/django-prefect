from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from .models import UserProfile
from . models import UserProfile
import requests

from . flow_generatore import (
    generate_flow,
    ## source credentials func
    s3_credentials,
    snowflake_credentials,
    notion_credentials,
    azureblobcontainer_credentials,
    azureblobstorage_credentials,
    github_credentials,
    googledrive_credentials,
    ## target credentials func
    pinecone_credentials,
    weaviatdb_credentials,
    singlestoredb_credentials,
    qdrant_credentials,
    elasticsearch_credentials
    


    )
from . forms import (
    S3ConnectionForm,
    AzureblobContainerForm,
    AzureblobStorageForm,
    PineconeConnectionForm,
    PostgressConnectionForm,
    SingleStoreDBConnectionsForm,
    NotionSourceForm,
    SnowFlakeSourceForm,
    ElasticSearchTargetForm,
    QdrantTargetForm,
    WeaviatTargetForm,
    GitHubSourceForm,
    GoogleDriveSourceForm,
    FlowsForm,
    OpenAiEmbeddingForm



)
from . models import (
    ## source
    S3_connections_aws,
    S3_connections_digital_ocean,
    Snowflake_connection,
    AzureblobStorage_connection,
    AzureblobContainer_connection,
    Notion_connection,
    Postgress_connections,
    Github_connection,
    GoogleDrive_connection,
    ##target,
    Pinecone_connection,
    Qdrant_connection,
    SingleStoreDB_connections,
    Weaviatdb_connection,
    Elasticsearch_connection,
    OpenAiEmbedding,
)
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.



def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)


@login_required
def intergrations(request):

    return render(request,'flowapp/intergrations.html')

#@login_required
def connection_edit(request,connection_name):
   
    return render(request,'flowapp/flow_edit.html',{})

@login_required
def connection_delete(request,connection_name):
   
    return HttpResponseRedirect('/flows/profile/')

@login_required
def flows(request):
    ## get owner details......................
    owner = get_object_or_404(UserProfile,user=request.user)
    openai_api_key_embedding = OpenAiEmbedding.objects.filter(owner=owner).first()
    if request.method =="POST":
        form = FlowsForm(request.POST)
        if form.is_valid():
            schedule_time = form.cleaned_data['schedule_time']
            time_zone = form.cleaned_data['time_zone']
            source = form.cleaned_data['source']
            target = form.cleaned_data['target']
            source_connection_name = form.cleaned_data['source_connection_name']
            target_connection_name = form.cleaned_data['target_connection_name']

            #check if source is S3 and target is  targets
            if source == "S3" and target =="Pinecone":
                 aws_source = S3_connections_aws.objects.filter(connection_name=source_connection_name,owner=owner).first()
                 pinecone_target = Pinecone_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()

                 source_credentials = s3_credentials(
                     aws_access_key=aws_source.aws_access_key_id,
                     aws_secret_access_key=aws_source.aws_secret_access_key,
                     bucket_name=aws_source.bucket_name,
                     prefix=aws_source.key,
                     file_type=aws_source.file_type
                     )
                 target_credentials = pinecone_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           api_key=pinecone_target.api_key,
                                                           environment=pinecone_target.environment,
                                                           index_name=pinecone_target.index_name
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "S3" and target == "SingleStoreBb":
                 aws_source = S3_connections_aws.objects.filter(connection_name=source_connection_name,owner=owner).first()
                 singlestore_target = SingleStoreDB_connections.objects.filter(connection_name=target_connection_name,owner=owner).first()

                 source_credentials = s3_credentials(
                     aws_access_key=aws_source.aws_access_key_id,
                     aws_secret_access_key=aws_source.aws_secret_access_key,
                     bucket_name=aws_source.bucket_name,
                     prefix=aws_source.key,
                     file_type=aws_source.file_type
                     )
                 target_credentials = singlestoredb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           singlestoredb_url=singlestore_target.singledb_url,
                                                           table_name=singlestore_target.table_name,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            elif source == "S3" and target == "Elasticsearch":
                 aws_source = S3_connections_aws.objects.filter(connection_name=source_connection_name,owner=owner).first()
                 elasticsearch_target = Elasticsearch_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()

                 source_credentials = s3_credentials(
                     aws_access_key=aws_source.aws_access_key_id,
                     aws_secret_access_key=aws_source.aws_secret_access_key,
                     bucket_name=aws_source.bucket_name,
                     prefix=aws_source.key,
                     file_type=aws_source.file_type
                     )
                 target_credentials = elasticsearch_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          es_url=elasticsearch_target.es_url,
                                                          index_name=elasticsearch_target.index_name,
                                                          es_user=elasticsearch_target.es_user,
                                                          es_password=elasticsearch_target.es_password
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "S3" and target == "Weaviatdb":
                 aws_source = S3_connections_aws.objects.filter(connection_name=source_connection_name,owner=owner).first()
                 weaviate_target = Weaviatdb_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()

                 source_credentials = s3_credentials(
                     aws_access_key=aws_source.aws_access_key_id,
                     aws_secret_access_key=aws_source.aws_secret_access_key,
                     bucket_name=aws_source.bucket_name,
                     prefix=aws_source.key,
                     file_type=aws_source.file_type
                     )
                 target_credentials = weaviatdb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                            weaviate_url=weaviate_target.url,
                                                          weaviate_api_key=weaviate_target.api_key,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            
            
            elif source == "S3" and target == "Qdrant":
                 aws_source = S3_connections_aws.objects.filter(connection_name=source_connection_name,owner=owner).first()
                 qdrant_target = Qdrant_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()

                 source_credentials = s3_credentials(
                     aws_access_key=aws_source.aws_access_key_id,
                     aws_secret_access_key=aws_source.aws_secret_access_key,
                     bucket_name=aws_source.bucket_name,
                     prefix=aws_source.key,
                     file_type=aws_source.file_type
                     )
                 target_credentials = qdrant_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          url=qdrant_target.url,
                                                          collection_name=qdrant_target.collection_name,
                                                          api_key=qdrant_target.api_key,
                                                          prefer_grpc=qdrant_target.prefer_grpc
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 

             #check if source is googledrive and target is  targets


            if source == "Googledrive" and target =="Pinecone":
                 pinecone_target = Pinecone_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 googledrive_source = GoogleDrive_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = googledrive_credentials(
                     gdrive_api_file=googledrive_source.gdrive_api_file,
                     folder_id=googledrive_source.folder_id,
                     recursive=googledrive_source.recursive,
                     template=googledrive_source.template,
                     query=googledrive_source.query,
                     num_results=googledrive_source.num_results,
                     supportsAllDrives=googledrive_source.supportsAllDrives
                     )
                 target_credentials = pinecone_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           api_key=pinecone_target.api_key,
                                                           environment=pinecone_target.environment,
                                                           index_name=pinecone_target.index_name
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "Googledrive" and target == "SingleStoreBb":
                 singlestore_target = SingleStoreDB_connections.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 googledrive_source = GoogleDrive_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 
                 source_credentials = googledrive_credentials(
                     gdrive_api_file=googledrive_source.gdrive_api_file,
                     folder_id=googledrive_source.folder_id,
                     recursive=googledrive_source.recursive,
                     template=googledrive_source.template,
                     query=googledrive_source.query,
                     num_results=googledrive_source.num_results,
                     supportsAllDrives=googledrive_source.supportsAllDrives
                     )
                 target_credentials = singlestoredb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           singlestoredb_url=singlestore_target.singledb_url,
                                                           table_name=singlestore_target.table_name,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            elif source == "Googledrive" and target == "Elasticsearch":
                 elasticsearch_target = Elasticsearch_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 googledrive_source = GoogleDrive_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 
                 source_credentials = googledrive_credentials(
                     gdrive_api_file=googledrive_source.gdrive_api_file,
                     folder_id=googledrive_source.folder_id,
                     recursive=googledrive_source.recursive,
                     template=googledrive_source.template,
                     query=googledrive_source.query,
                     num_results=googledrive_source.num_results,
                     supportsAllDrives=googledrive_source.supportsAllDrives
                     )
                 target_credentials = elasticsearch_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          es_url=elasticsearch_target.es_url,
                                                          index_name=elasticsearch_target.index_name,
                                                          es_user=elasticsearch_target.es_user,
                                                          es_password=elasticsearch_target.es_password
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "Googledrive" and target == "Weaviatdb":
                 weaviate_target = Weaviatdb_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 googledrive_source = GoogleDrive_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                
                 source_credentials = googledrive_credentials(
                     gdrive_api_file=googledrive_source.gdrive_api_file,
                     folder_id=googledrive_source.folder_id,
                     recursive=googledrive_source.recursive,
                     template=googledrive_source.template,
                     query=googledrive_source.query,
                     num_results=googledrive_source.num_results,
                     supportsAllDrives=googledrive_source.supportsAllDrives
                     )
                 target_credentials = weaviatdb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                            weaviate_url=weaviate_target.url,
                                                          weaviate_api_key=weaviate_target.api_key,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            
            
            elif source == "Googledrive" and target == "Qdrant":
                 qdrant_target = Qdrant_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 googledrive_source = GoogleDrive_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 
                 source_credentials = googledrive_credentials(
                     gdrive_api_file=googledrive_source.gdrive_api_file,
                     folder_id=googledrive_source.folder_id,
                     recursive=googledrive_source.recursive,
                     template=googledrive_source.template,
                     query=googledrive_source.query,
                     num_results=googledrive_source.num_results,
                     supportsAllDrives=googledrive_source.supportsAllDrives
                     )
                 target_credentials = qdrant_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          url=qdrant_target.url,
                                                          collection_name=qdrant_target.collection_name,
                                                          api_key=qdrant_target.api_key,
                                                          prefer_grpc=qdrant_target.prefer_grpc
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            

            #check if source is github and target is  targets


            if source == "Github" and target =="Pinecone":
                 pinecone_target = Pinecone_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 github_source = Github_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = github_credentials(
                     repo=github_source.repo,
                     creator=github_source.creator,
                     access_token=github_source.access_token,
                     include_prs=github_source.include_prs
                     
                     )
                 target_credentials = pinecone_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           api_key=pinecone_target.api_key,
                                                           environment=pinecone_target.environment,
                                                           index_name=pinecone_target.index_name
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "Github" and target == "SingleStoreBb":
                 singlestore_target = SingleStoreDB_connections.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 github_source = Github_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = github_credentials(
                     repo=github_source.repo,
                     creator=github_source.creator,
                     access_token=github_source.access_token,
                     include_prs=github_source.include_prs
                     
                     )
                 target_credentials = singlestoredb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           singlestoredb_url=singlestore_target.singledb_url,
                                                           table_name=singlestore_target.table_name,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            elif source == "Github" and target == "Elasticsearch":
                 elasticsearch_target = Elasticsearch_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 github_source = Github_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = github_credentials(
                     repo=github_source.repo,
                     creator=github_source.creator,
                     access_token=github_source.access_token,
                     include_prs=github_source.include_prs
                     
                     )
                 target_credentials = elasticsearch_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          es_url=elasticsearch_target.es_url,
                                                          index_name=elasticsearch_target.index_name,
                                                          es_user=elasticsearch_target.es_user,
                                                          es_password=elasticsearch_target.es_password
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "Github" and target == "Weaviatdb":
                 weaviate_target = Weaviatdb_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 github_source = Github_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = github_credentials(
                     repo=github_source.repo,
                     creator=github_source.creator,
                     access_token=github_source.access_token,
                     include_prs=github_source.include_prs
                     
                     )
                 target_credentials = weaviatdb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                            weaviate_url=weaviate_target.url,
                                                          weaviate_api_key=weaviate_target.api_key,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            
            
            elif source == "Github" and target == "Qdrant":
                 qdrant_target = Qdrant_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 github_source = Github_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = github_credentials(
                     repo=github_source.repo,
                     creator=github_source.creator,
                     access_token=github_source.access_token,
                     include_prs=github_source.include_prs
                     
                     )
                 target_credentials = qdrant_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          url=qdrant_target.url,
                                                          collection_name=qdrant_target.collection_name,
                                                          api_key=qdrant_target.api_key,
                                                          prefer_grpc=qdrant_target.prefer_grpc
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            

             #check if source is snowflake and target is  targets


            if source == "Snowflake" and target =="Pinecone":
                 pinecone_target = Pinecone_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 snowflake_source = Snowflake_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = snowflake_credentials(
                     query=snowflake_source.query,
                     user=snowflake_source.user,
                     password=snowflake_source.password,
                     account=snowflake_source.account,
                     warehouse=snowflake_source.warehouse,
                     role=snowflake_source.role,
                     database=snowflake_source.database,
                     schema=snowflake_source.schema
                     
                     
                     
                     )
                 target_credentials = pinecone_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           api_key=pinecone_target.api_key,
                                                           environment=pinecone_target.environment,
                                                           index_name=pinecone_target.index_name
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "Snowflake" and target == "SingleStoreBb":
                 singlestore_target = SingleStoreDB_connections.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 snowflake_source = Snowflake_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = snowflake_credentials(
                     query=snowflake_source.query,
                     user=snowflake_source.user,
                     password=snowflake_source.password,
                     account=snowflake_source.account,
                     warehouse=snowflake_source.warehouse,
                     role=snowflake_source.role,
                     database=snowflake_source.database,
                     schema=snowflake_source.schema
                     
                     
                     
                     )
                 target_credentials = singlestoredb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           singlestoredb_url=singlestore_target.singledb_url,
                                                           table_name=singlestore_target.table_name,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            elif source == "Snowflake" and target == "Elasticsearch":
                 elasticsearch_target = Elasticsearch_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 snowflake_source = Snowflake_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = snowflake_credentials(
                     query=snowflake_source.query,
                     user=snowflake_source.user,
                     password=snowflake_source.password,
                     account=snowflake_source.account,
                     warehouse=snowflake_source.warehouse,
                     role=snowflake_source.role,
                     database=snowflake_source.database,
                     schema=snowflake_source.schema
                     
                     
                     
                     )
                 target_credentials = elasticsearch_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          es_url=elasticsearch_target.es_url,
                                                          index_name=elasticsearch_target.index_name,
                                                          es_user=elasticsearch_target.es_user,
                                                          es_password=elasticsearch_target.es_password
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "Snowflake" and target == "Weaviatdb":
                 weaviate_target = Weaviatdb_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 snowflake_source = Snowflake_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = snowflake_credentials(
                     query=snowflake_source.query,
                     user=snowflake_source.user,
                     password=snowflake_source.password,
                     account=snowflake_source.account,
                     warehouse=snowflake_source.warehouse,
                     role=snowflake_source.role,
                     database=snowflake_source.database,
                     schema=snowflake_source.schema
                     
                     
                     
                     )
                 target_credentials = weaviatdb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                            weaviate_url=weaviate_target.url,
                                                          weaviate_api_key=weaviate_target.api_key,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            
            
            elif source == "Snowflake" and target == "Qdrant":
                 qdrant_target = Qdrant_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 snowflake_source = Snowflake_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = snowflake_credentials(
                     query=snowflake_source.query,
                     user=snowflake_source.user,
                     password=snowflake_source.password,
                     account=snowflake_source.account,
                     warehouse=snowflake_source.warehouse,
                     role=snowflake_source.role,
                     database=snowflake_source.database,
                     schema=snowflake_source.schema
                     
                     
                     
                     )
                 target_credentials = qdrant_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          url=qdrant_target.url,
                                                          collection_name=qdrant_target.collection_name,
                                                          api_key=qdrant_target.api_key,
                                                          prefer_grpc=qdrant_target.prefer_grpc
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 

            

             #check if source is notion and target is  targets


            if source == "Notion" and target =="Pinecone":
                 pinecone_target = Pinecone_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 notion_source = Notion_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = notion_credentials(
                    integration_token=notion_source.integration_token,
                    database_id=notion_source.database_id,
                    request_timeout_sec=notion_source.request_timeout_sec
                     
                     
                     )
                 target_credentials = pinecone_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           api_key=pinecone_target.api_key,
                                                           environment=pinecone_target.environment,
                                                           index_name=pinecone_target.index_name
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "Notion" and target == "SingleStoreBb":
                 singlestore_target = SingleStoreDB_connections.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 notion_source = Notion_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = notion_credentials(
                    integration_token=notion_source.integration_token,
                    database_id=notion_source.database_id,
                    request_timeout_sec=notion_source.request_timeout_sec
                     
                     
                     )
                 target_credentials = singlestoredb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           singlestoredb_url=singlestore_target.singledb_url,
                                                           table_name=singlestore_target.table_name,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            elif source == "Notion" and target == "Elasticsearch":
                 elasticsearch_target = Elasticsearch_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 notion_source = Notion_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = notion_credentials(
                    integration_token=notion_source.integration_token,
                    database_id=notion_source.database_id,
                    request_timeout_sec=notion_source.request_timeout_sec
                     
                     
                     )
                 target_credentials = elasticsearch_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          es_url=elasticsearch_target.es_url,
                                                          index_name=elasticsearch_target.index_name,
                                                          es_user=elasticsearch_target.es_user,
                                                          es_password=elasticsearch_target.es_password
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "Notion" and target == "Weaviatdb":
                 weaviate_target = Weaviatdb_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 notion_source = Notion_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = notion_credentials(
                    integration_token=notion_source.integration_token,
                    database_id=notion_source.database_id,
                    request_timeout_sec=notion_source.request_timeout_sec
                     
                     
                     )
                 target_credentials = weaviatdb_credentials(openai_api_key='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',
                                                            weaviate_url=weaviate_target.url,
                                                          weaviate_api_key=weaviate_target.api_key,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            
            
            elif source == "Notion" and target == "Qdrant":
                 qdrant_target = Qdrant_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 notion_source = Notion_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = notion_credentials(
                    integration_token=notion_source.integration_token,
                    database_id=notion_source.database_id,
                    request_timeout_sec=notion_source.request_timeout_sec
                     
                     
                     )
                 target_credentials = qdrant_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          url=qdrant_target.url,
                                                          collection_name=qdrant_target.collection_name,
                                                          api_key=qdrant_target.api_key,
                                                          prefer_grpc=qdrant_target.prefer_grpc
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 



            

            
             #check if source is AzureblobStorage and target is  targets


            if source == "AzureblobStorage" and target =="Pinecone":
                 pinecone_target = Pinecone_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 azureblobstorage_source = AzureblobStorage_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = azureblobstorage_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                   blob_name=azureblobstorage_source.blob_name
                     
                     
                     )
                 target_credentials = pinecone_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           api_key=pinecone_target.api_key,
                                                           environment=pinecone_target.environment,
                                                           index_name=pinecone_target.index_name
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "AzureblobStorage" and target == "SingleStoreBb":
                 singlestore_target = SingleStoreDB_connections.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 azureblobstorage_source = AzureblobStorage_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = azureblobstorage_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                   blob_name=azureblobstorage_source.blob_name
                     
                     
                     )
                 target_credentials = singlestoredb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           singlestoredb_url=singlestore_target.singledb_url,
                                                           table_name=singlestore_target.table_name,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            elif source == "AzureblobStorage" and target == "Elasticsearch":
                 elasticsearch_target = Elasticsearch_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 azureblobstorage_source = AzureblobStorage_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = azureblobstorage_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                   blob_name=azureblobstorage_source.blob_name
                     
                     
                     )
                 target_credentials = elasticsearch_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          es_url=elasticsearch_target.es_url,
                                                          index_name=elasticsearch_target.index_name,
                                                          es_user=elasticsearch_target.es_user,
                                                          es_password=elasticsearch_target.es_password
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "AzureblobStorage" and target == "Weaviatdb":
                 weaviate_target = Weaviatdb_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 azureblobstorage_source = AzureblobStorage_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = azureblobstorage_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                   blob_name=azureblobstorage_source.blob_name
                     
                     
                     )
                 target_credentials = weaviatdb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                            weaviate_url=weaviate_target.url,
                                                          weaviate_api_key=weaviate_target.api_key,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            
            
            elif source == "AzureblobStorage" and target == "Qdrant":
                 qdrant_target = Qdrant_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 azureblobstorage_source = AzureblobStorage_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = azureblobstorage_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                   blob_name=azureblobstorage_source.blob_name
                     
                     
                     )
                 target_credentials = qdrant_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          url=qdrant_target.url,
                                                          collection_name=qdrant_target.collection_name,
                                                          api_key=qdrant_target.api_key,
                                                          prefer_grpc=qdrant_target.prefer_grpc
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 

            

            
             #check if source is AzureblobContainer and target is  targets


            if source == "AzureblobContainer" and target =="Pinecone":
                 pinecone_target = Pinecone_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 azureblobcontainer_source = AzureblobContainer_connection.objects.filter(connection_name=source_connection_name,owner=owner).first()

                 source_credentials = azureblobcontainer_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                     
                     )
                 target_credentials = pinecone_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           api_key=pinecone_target.api_key,
                                                           environment=pinecone_target.environment,
                                                           index_name=pinecone_target.index_name
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "AzureblobContainer" and target == "SingleStoreBb":
                 singlestore_target = SingleStoreDB_connections.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 source_credentials = azureblobcontainer_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                     
                     )
                 target_credentials = singlestoredb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                           singlestoredb_url=singlestore_target.singledb_url,
                                                           table_name=singlestore_target.table_name,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            elif source == "AzureblobContainer" and target == "Elasticsearch":
                 elasticsearch_target = Elasticsearch_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 source_credentials = azureblobcontainer_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                     
                     )
                 target_credentials = elasticsearch_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          es_url=elasticsearch_target.es_url,
                                                          index_name=elasticsearch_target.index_name,
                                                          es_user=elasticsearch_target.es_user,
                                                          es_password=elasticsearch_target.es_password
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
            
            elif source == "AzureblobContainer" and target == "Weaviatdb":
                 weaviate_target = Weaviatdb_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 source_credentials = azureblobcontainer_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                     
                     )
                 target_credentials = weaviatdb_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                            weaviate_url=weaviate_target.url,
                                                          weaviate_api_key=weaviate_target.api_key,
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                 
            
            
            
            elif source == "AzureblobContainer" and target == "Qdrant":
                 qdrant_target = Qdrant_connection.objects.filter(connection_name=target_connection_name,owner=owner).first()
                 source_credentials = azureblobcontainer_credentials(
                   conn_str=azureblobstorage_source.conn_str,
                   container=azureblobstorage_source.container,
                     
                     )
                 target_credentials = qdrant_credentials(openai_api_key=openai_api_key_embedding.openai_api_key,
                                                          url=qdrant_target.url,
                                                          collection_name=qdrant_target.collection_name,
                                                          api_key=qdrant_target.api_key,
                                                          prefer_grpc=qdrant_target.prefer_grpc
                                                           )
                 
                 
                 #generate flow /////
                 generate_flow(user=owner,
                               source=source,
                               target=target,
                               source_credentials=source_credentials,
                               target_credentials=target_credentials,
                               scheduel_time=schedule_time,
                               time_zone=time_zone
                               )
                
            
            ## created and deploy flows to prefect cloud
           
            return HttpResponseRedirect('/flows/pipline/')
        
        


    else:
        form = FlowsForm()
       
    return render(request,'flowapp/flow.html',{'form':form})




 ## source view
def google_drive_source_view(request):
    owner = get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":
        form = GoogleDriveSourceForm(request.POST)
        print(request.POST)
        if form.is_valid():

            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
    else:
         form = GoogleDriveSourceForm()
    return render(request,'flowapp/googledrivesource.html',{'form':form})




def azure_container_source_view(request):
    owner = get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":

        form = AzureblobContainerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
    else:
         
         form = AzureblobContainerForm()
    return render(request,'flowapp/Azurecontainer.html',{'form':form})

def azure_storage_source_view(request):
    owner = get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":
        form =AzureblobStorageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
    else:
         form = AzureblobStorageForm()
    return render(request,'flowapp/AzureStorage.html',{'form':form})


def github_source_view(request):
    owner = get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":
        form = GitHubSourceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
    else:
         form = GitHubSourceForm()
    return render(request,'flowapp/githubsource.html',{'form':form})




def notion_source_view(request):
    owner = get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":
        form = NotionSourceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
    else:
         form = NotionSourceForm()
    return render(request,'flowapp/notionsource.html',{'form':form})


def snowflake_source_view(request):
   owner = get_object_or_404(UserProfile,user=request.user)
   if request.method == "POST":
        form = SnowFlakeSourceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
   else:
         form = SnowFlakeSourceForm()
   return render(request,'flowapp/snowflakesource.html',{'form':form})


def asw_source_view(request):
   owner = get_object_or_404(UserProfile,user=request.user)
   if request.method == "POST":
        print(request.POST)
        form = S3ConnectionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
   else:
         form = S3ConnectionForm()
   return render(request,'flowapp/s3source.html',{'form':form})




## target views


def pinecone_target_view(request):

    owner = get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":
        form = PineconeConnectionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
    else:
         form =  PineconeConnectionForm()
    
    return render(request,'flowapp/pineconetarget.html',{'form':form})


def weaviatdb_target_view(request):
     
     owner = get_object_or_404(UserProfile,user=request.user)
     if request.method == "POST":
        form = WeaviatTargetForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/profile/integration/')
     else:
         form =  WeaviatTargetForm()
    
     return render(request,'flowapp/weaviateTarget.html',{'form':form})


def singlestoredb_target_view(request):
   
   owner = get_object_or_404(UserProfile,user=request.user)
   if request.method == "POST":
        form = SingleStoreDBConnectionsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
   else:
         form =  SingleStoreDBConnectionsForm()
    
   return render(request,'flowapp/singlestoreTarget.html',{'form':form})


def elasticsearch_target_view(request):
     
     owner = get_object_or_404(UserProfile,user=request.user)
     if request.method == "POST":
        form = ElasticSearchTargetForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
     else:
         form =  ElasticSearchTargetForm()
    
     return render(request,'flowapp/elasticsearchTarget.html',{'form':form})



def qdrant_target_view(request):
     owner = get_object_or_404(UserProfile,user=request.user)
     if request.method == "POST":
        form = QdrantTargetForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
     else:
         form =  QdrantTargetForm()
    
     return render(request,'flowapp/qdrantTarget.html',{'form':form})
    



def openai_embedding_view(request):
     owner = get_object_or_404(UserProfile,user=request.user)
     if request.method == "POST":
        form = OpenAiEmbeddingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = owner
            instance.save()
            return HttpResponseRedirect('/flows/integration/')
     else:
         form =  OpenAiEmbeddingForm()
    
     return render(request,'flowapp/openaiembedding.html',{'form':form})





def user_connection(request):
    return render(request,"flowapp/connections.html")

def user_flow_deployment(request):
  
    return render(request,'flowapp/deployments.html')


def flowpipline(request):
    return render(request,"flowapp/flowpipline.html")
