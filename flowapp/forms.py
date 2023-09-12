from django.forms import ModelForm
from .models import (Pinecone_connection,
                     Postgress_connections,
                     SingleStoreDB_connections,
                     S3_connections_aws,
                     Flows,
                     Weaviatdb_connection,
                     Snowflake_connection,
                     AzureblobStorage_connection,
                     AzureblobContainer_connection,
                     GoogleDrive_connection,
                     Github_connection,
                     Qdrant_connection,
                     Elasticsearch_connection,
                     Notion_connection,
                     OpenAiEmbedding,
                     
                     
                     )

from django import forms




class S3ConnectionForm(ModelForm):
   
    class Meta:
        model = S3_connections_aws
        fields = ("connection_name","aws_access_key_id","key",
                  "aws_secret_access_key","bucket_name",
                  "file_type")
        
    def __init__(self,*args, **kwargs):
        super(S3ConnectionForm, self).__init__(*args, **kwargs)
        self.fields['key'].widget.attrs.update({'placeholder':'Example : Article/somedata'})


       
   
        
class PostgressConnectionForm(ModelForm):
    class Meta:
        model = Postgress_connections
        fields = ("connection_name","database_name","host","password","port","username")

         
       





class GoogleDriveSourceForm(ModelForm):
    class Meta:
        model = GoogleDrive_connection
        fields = ('connection_name',
                  'gdrive_api_file',
                  'folder_id',
                  'file_types',
                  'recursive',
                  'template',
                  'query',
                  'num_results',
                  'supportsAllDrives'

                  )
    
     



class GitHubSourceForm(ModelForm):
    class Meta:
        model = Github_connection
        fields = ('connection_name',
                  'access_token',
                  'repo',
                  'creator',
                  "include_prs")
        
        
class SnowFlakeSourceForm(ModelForm):
    class Meta:
        model = Snowflake_connection
        fields =  ('connection_name',
                  'query',
                  'user',
                  'password',
                  'account',
                  'warehouse',
                  'role',
                  'database',
                  'schema',
                  )
        
class AzureblobContainerForm(ModelForm):
    class Meta:
        model = AzureblobContainer_connection
        fields = ('connection_name','conn_str','container')
        
        


class AzureblobStorageForm(ModelForm):
    class Meta:
        model =  AzureblobStorage_connection
        fields = ('connection_name','source_name','conn_str','container','blob_name')

         
        widgets = {
            'source_name':forms.widgets.TextInput(attrs={'disabled':'True'}),
  
        }

class NotionSourceForm(ModelForm):
    class Meta:
        model = Notion_connection
        fields = ('connection_name','integration_token','database_id','request_timeout_sec')

         
       


class FlowsForm(forms.ModelForm):   
    class Meta:
        model = Flows
        fields = ("source",'target','schedule_time','time_zone','flow_name','deployment_name',
                  'source_connection_name','target_connection_name')

        widgets = {
            'schedule_time':forms.widgets.DateInput(attrs={'type':'datetime-local'}),
  
        }

        
      



### traget
class PineconeConnectionForm(ModelForm):
    class Meta:
        model = Pinecone_connection
        fields = ("connection_name","api_key","environment","index_name")

         
        




class SingleStoreDBConnectionsForm(ModelForm):
    class Meta:
        model = SingleStoreDB_connections
        fields = ("connection_name","singledb_url","table_name")

       



class QdrantTargetForm(ModelForm):
    class Meta:
        model = Qdrant_connection
        fields = ('connection_name','url','collection_name','api_key','prefer_grpc')

       



class WeaviatTargetForm(ModelForm):
    class Meta:
        model = Weaviatdb_connection
        fields = ('connection_name','url','api_key')

        




class ElasticSearchTargetForm(ModelForm):
    class Meta:
        model = Elasticsearch_connection
        fields = ('connection_name',
                  'es_url',
                  'index_name',
                  'es_user',
                  'es_password'
                  )

class OpenAiEmbeddingForm(ModelForm):
    class Meta:
        model = OpenAiEmbedding
        fields = ("openai_api_key",)