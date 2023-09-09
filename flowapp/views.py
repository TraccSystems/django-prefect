from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from .models import UserProfile
from . models import UserProfile
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
    FlowsForm



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
    Elasticsearch_connection
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
def profile(request):
    owner = get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":

        s3form = S3ConnectionForm(request.POST)
        postgresform = PostgressConnectionForm(request.POST)
        pinconeform = PineconeConnectionForm(request.POST)
        singlestoreform = SingleStoreDBConnectionsForm(request.POST)

        if s3form.is_valid():
            instance = s3form.save(commit=False)
            instance.owner = owner
            instance.save()
            HttpResponseRedirect('/flows/profile/')

        elif postgresform.is_valid():
            instance = postgresform.save(commit=False)
            instance.owner = owner
            instance.save()
            HttpResponseRedirect('/flows/profile/')

        elif pinconeform.is_valid():
            instance = pinconeform.save(commit=False)
            instance.owner = owner
            instance.save()
            HttpResponseRedirect('/flows/profile/')
        
        elif singlestoreform.is_valid():
            instance = singlestoreform.save(commit=False)
            instance.owner = owner
            instance.save()
            HttpResponseRedirect('/flows/profile/')
        
    else:
        #forms
        s3form = S3ConnectionForm()
        postgresform = PostgressConnectionForm()
        pinconeform = PineconeConnectionForm()
        singlestoreform = SingleStoreDBConnectionsForm()
        # connections form contexts
    return render(request,'flowapp/profile.html',{
            's3form': s3form,
            "postgresform":postgresform,
            "pinconeform":pinconeform,
            "singlestoreform":singlestoreform,
            "s3connections":S3_connections_aws.objects.filter(owner=owner)[:2],
            "pgres_connection":Postgress_connections.objects.filter(owner=owner)[:2],
            "pincone_connections": Pinecone_connection.objects.filter(owner=owner)[:2],
            "singlestore_connections":SingleStoreDB_connections.objects.filter(owner=owner)[:2],
        })

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
    if request.method =="POST":
        form = FlowsForm(request.POST)
        if form.is_valid():
            schedule_time = form.cleaned_data['schedule_time']
            time_zone = form.cleaned_data['time_zone']
            source = form.cleaned_data['source']
            target = form.cleaned_data['target']

            if source == "S3" and target =="Pinecone":
                 aws_source = S3_connections_aws.objects.filter(source_name=source,owner=owner).first()
                 pinecone_target = Pinecone_connection.objects.filter(target_name=target,owner=owner).first()

                 source_credentials = s3_credentials(
                     aws_access_key=aws_source.aws_access_key_id,
                     aws_secret_access_key=aws_source.aws_secret_access_key,
                     bucket_name=aws_source.bucket_name,
                     prefix=aws_source.key,
                     file_type=aws_source.file_type
                     )
                 target_credentials = pinecone_credentials(openai_api_key='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',
                                                           api_key=pinecone_target.api_key,
                                                           environment=pinecone_target.environment,
                                                           index_name=pinecone_target.index_name
                                                           )
                 
                 #generate flow
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
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
            return HttpResponseRedirect('/flows/profile/integration/')
     else:
         form =  QdrantTargetForm()
    
     return render(request,'flowapp/qdrantTarget.html',{'form':form})
    







