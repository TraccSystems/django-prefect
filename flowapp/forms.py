from django.forms import ModelForm
from .models import (Pinecone_connection,
                     Postgress_connections,
                     SingleStoreDB_connections,
                     S3_connections,
                     Flows
                     )

from django import forms




class S3ConnectionForm(ModelForm):
    class Meta:
        model = S3_connections
        fields = ("aws_access_key_id","aws_region","aws_endpoint_url",
                  "aws_secret_access_key","bucket_name",
                  "file_type","s3_connection_type")
        
class PostgressConnectionForm(ModelForm):
    class Meta:
        model = Postgress_connections
        fields = ("database_name","host","password","port","username","post_connection_type")

class PineconeConnectionForm(ModelForm):
    class Meta:
        model = Pinecone_connection
        fields = ("api_key","environment","index_name","pincon_connection_types")




class SingleStoreDBConnectionsForm(ModelForm):
    class Meta:
        model = SingleStoreDB_connections
        fields = ("single_connection_types","singledb_url","table_name")



class FlowsForm(forms.ModelForm):
    
    class Meta:
        model = Flows
        fields = ("source",'target')




