from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from .models import UserProfile
from . models import UserProfile
from . flow_generatore import s3_to_pincone_flow,s3_to_singleStore_flow
from . forms import (
                     PostgressConnectionForm,
                     PineconeConnectionForm,
                     SingleStoreDBConnectionsForm,
                     S3ConnectionForm,
                     FlowsForm,
                     FlowsForm_S3_to_Singlestore,
                     FlowsForm_Postgress_to_Pinecone,
                     FlowsForm_Postgress_to_Singlestore
                     )
from . models import (Pinecone_connection,
                      S3_connections_aws,
                      Postgress_connections,
                      SingleStoreDB_connections,
                      Flows
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
    s3 = S3_connections_aws.objects.filter(owner=owner).first()
    pinecone = Pinecone_connection.objects.filter(owner=owner).first()
    singleStore = SingleStoreDB_connections.objects.filter(owner=owner).first()
    if request.method =="POST":
        
        form_postgress_pinecone = FlowsForm_Postgress_to_Pinecone(owner,request.POST)
        form_postgress_singlestore =FlowsForm_Postgress_to_Singlestore(owner,request.POST)
        form = FlowsForm(owner,request.POST)
        form_s3_singlestore = FlowsForm_S3_to_Singlestore(owner,request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            target = form.cleaned_data['target']
            #get connection details
            s3_connections = S3_connections_aws.objects.get(connection_name=source)
            pinecone_connections = Pinecone_connection.objects.get(connection_name=target)
            
            
            ## created and deploy flows to prefect cloud

            s3_to_pincone_flow(owner,
                               s3_connections.aws_access_key_id,
                               s3_connections.aws_secret_access_key,
                               s3_connections.key,
                               s3_connections.bucket_name,
                               s3_connections.file_type,
                               pinecone_connections.index_name,
                               pinecone_connections.environment,
                               pinecone_connections.api_key
                               )

            return HttpResponseRedirect('/flows/flow/')
        
        elif form_s3_singlestore.is_valid():
            source = form.cleaned_data['source']
            target = form.cleaned_data['target']

             #get connection details
            s3_connections = S3_connections_aws.objects.get(connection_name=source)
            singlestore_connections = SingleStoreDB_connections.objects.get(connection_name=target)

             ## created and deploy flows to prefect cloud

            s3_to_singleStore_flow(owner,
                               s3_connections.aws_access_key_id,
                               s3_connections.aws_secret_access_key,
                               s3_connections.key,
                               s3_connections.bucket_name,
                               s3_connections.file_type,
                               singlestore_connections.singledb_url,
                               singlestore_connections.table_name,
                               )


            
            return HttpResponseRedirect('/flows/flow/')
        
        elif form_postgress_pinecone.is_valid():
            source = form.cleaned_data['source']
            target = form.cleaned_data['target']
            return HttpResponseRedirect('/flows/flow/')
        
        elif form_postgress_singlestore.is_valid():
            source = form.cleaned_data['source']
            target = form.cleaned_data['target']
            return HttpResponseRedirect('/flows/flow/')


    else:
        form = FlowsForm(owner=owner)
        form_s3_singlestore = FlowsForm_S3_to_Singlestore(owner=owner)
        form_postgress_pinecone = FlowsForm_Postgress_to_Pinecone(owner=owner)
        form_postgress_singlestore =FlowsForm_Postgress_to_Singlestore(owner=owner)
       
    return render(request,'flowapp/flow.html',{'s3form':form,
                                               'form_s3_singlestore': form_s3_singlestore,
                                               'form_postgress_pinecone': form_postgress_pinecone,
                                               'form_postgress_singlestore':form_postgress_singlestore
                                               })



