from django.forms import ModelForm
from .models import (Pinecone_connection,
                     Postgress_connections,
                     SingleStoreDB_connections,
                     S3_connections_aws,
                     Flows,
                     Flows_s3_to_singlestore,
                     Flows_postgress_to_pinecone,
                     Flows_postgress_to_singlestore
                     )

from django import forms




class S3ConnectionForm(ModelForm):
   
    class Meta:
        model = S3_connections_aws
        fields = ("connection_name","aws_access_key_id","key",
                  "aws_secret_access_key","bucket_name",
                  "file_type","s3_connection_type")
        
    def __init__(self,*args, **kwargs):
        super(S3ConnectionForm, self).__init__(*args, **kwargs)
        self.fields['key'].widget.attrs.update({'placeholder':'Example : Article/somedata'})
       
   
        
class PostgressConnectionForm(ModelForm):
    class Meta:
        model = Postgress_connections
        fields = ("connection_name","database_name","host","password","port","username","post_connection_type")

class PineconeConnectionForm(ModelForm):
    class Meta:
        model = Pinecone_connection
        fields = ("connection_name","api_key","environment","index_name","pincon_connection_types")




class SingleStoreDBConnectionsForm(ModelForm):
    class Meta:
        model = SingleStoreDB_connections
        fields = ("connection_name","single_connection_types","singledb_url","table_name")



class FlowsForm(forms.ModelForm):
    
    class Meta:
        model = Flows
        fields = ("source",'target','scheduel_time','time_zone')

        widgets = {
            'scheduel_time':forms.widgets.DateInput(attrs={'type':'datetime-local'}),
  
        }
    def __init__(self, owner, *args, **kwargs):
        super(FlowsForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = S3_connections_aws.objects.filter(owner=owner)
        self.fields['target'].queryset = Pinecone_connection.objects.filter(owner=owner)
        
       




class FlowsForm_S3_to_Singlestore(forms.ModelForm):
    
    class Meta:
        model = Flows
        fields = ("source",'target')
    def __init__(self, owner, *args, **kwargs):
        super(FlowsForm_S3_to_Singlestore, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = S3_connections_aws.objects.filter(owner=owner)
        self.fields['target'].queryset = SingleStoreDB_connections.objects.filter(owner=owner)




class FlowsForm_Postgress_to_Singlestore(forms.ModelForm):
    
    class Meta:
        model = Flows
        fields = ("source",'target')
    def __init__(self, owner, *args, **kwargs):
        super(FlowsForm_Postgress_to_Singlestore, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = Postgress_connections.objects.filter(owner=owner)
        self.fields['target'].queryset = SingleStoreDB_connections.objects.filter(owner=owner)



class FlowsForm_Postgress_to_Pinecone(forms.ModelForm):
    
    class Meta:
        model = Flows
        fields = ("source",'target')
    def __init__(self, owner, *args, **kwargs):
        super(FlowsForm_Postgress_to_Pinecone, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = Postgress_connections.objects.filter(owner=owner)
        self.fields['target'].queryset = Pinecone_connection.objects.filter(owner=owner)


