from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('integration/',intergrations,name='integretion'),
    path('create/pipline/',flows,name='create-pipline'),
    path('openai/embedding/',openai_embedding_view,name="openai"),
    path('user/connection/',user_connection,name='connection'),
    path('deployment/',user_flow_deployment,name='deployment'),
    path('flow/',flowpipline,name='flow'),
    path('googledrive/source/',google_drive_source_view,name='googledrive'),
    path('azurecontainter/source/',azure_container_source_view,name='azurecontainer'),
    path('azurestorage/source/',azure_storage_source_view,name='azurestorage'),
    path('github/source/',github_source_view,name='github'),
    path('notion/source/',notion_source_view,name='notion'),
    path('snowflake/source/',snowflake_source_view,name='snowflake'),
    path('aws/source/',asw_source_view,name='aws'),
    path('pinecone/target/', pinecone_target_view,name='pinecone'),
    path('weaviatdb/target/', weaviatdb_target_view,name='weaviatdb'),
    path('singlestoredb/target/', singlestoredb_target_view,name='singlestoredb'),
    path('elasticsearch/target/', elasticsearch_target_view,name='elasticsearch'),
    path('qdrant/target/', qdrant_target_view,name='qdrant'),
    path('login/',auth_views.LoginView.as_view(template_name='flowapp/login.html'),name='login'),
    path('flow/<str:connection_name>/edit',connection_edit,name='connection-edit'),
    path('flow/<str:connection_name>/delete',connection_delete,name='connection-delete'),
]
