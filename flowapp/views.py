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
                     )
from . models import (Pinecone_connection,
                      S3_connections,
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
        print(Postgress_connections.objects.filter(owner=owner))
    return render(request,'flowapp/profile.html',{
            's3form': s3form,
            "postgresform":postgresform,
            "pinconeform":pinconeform,
            "singlestoreform":singlestoreform,
            "s3connections":S3_connections.objects.filter(owner=owner)[:2],
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


def flows(request):
    ## get owner details......................
    owner = get_object_or_404(UserProfile,user=request.user)
    s3 = S3_connections.objects.filter(owner=owner).first()
    pinecone = Pinecone_connection.objects.filter(owner=owner).first()
    singleStore = SingleStoreDB_connections.objects.filter(owner=owner).first()
    if request.method =="POST":
        form = FlowsForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            target = form.cleaned_data['target']
            if source == "S3" and target == "Pinecone":
                # generate and upload flow function to s3 then deploy on prefect cloud
                s3_to_pincone_flow(
                    request.user,
                    s3.aws_access_key_id,
                    s3.aws_secret_access_key,
                    s3.aws_endpoint_url,
                    s3.bucket_name,
                    s3.aws_region,
                    pinecone.index_name,pinecone.environment,pinecone.api_key)
            elif source =="S3" and target == "SingleStore":
                s3_to_singleStore_flow(
                    request.user,
                    s3.aws_access_key_id,
                    s3.aws_secret_access_key,
                    s3.aws_endpoint_url,
                    s3.bucket_name,
                    s3.aws_region,
                    singleStore.singledb_url,
                    singleStore.table_name
                )
            return HttpResponseRedirect('/flows/flow/')
    else:
        form = FlowsForm()
    return render(request,'flowapp/flow.html',{'form':form})



