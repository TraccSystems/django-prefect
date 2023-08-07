from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from .models import UserProfile
from . models import S3Sourecs,PygonSource,IntervalScheduleSchedule,UserProfile,dataFlow
from . forms import S3SourecsForm, PygonSourceForm,IntervalScheduleScheduleForm,dataFlowForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from . digital_ocean_block import PostGresCredential,DigitalOceanCredential
from prefect.deployments import run_deployment
from .flow import (save_progres_credentials,
                   save_asw_credentials,
                   pull_data_from_s3_write_to_postgress,write_data_to_postgress)


def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)


@login_required
def profile(request):
    
    if request.method == "POST":
        user = UserProfile.objects.get(user=request.user)
        form = dataFlowForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = user
            instance.save()
            return HttpResponseRedirect(reverse('flow-edit',args=(instance.flow_name,)))
    else:
         user = UserProfile.objects.get(user=request.user)
         form = dataFlowForm()
         dataflows = dataFlow.objects.filter(profile=user)
    return render(request,'flowapp/profile.html',{'form':form,"dataflows":dataflows})

@login_required
def flow_edit(request,flow_name):
    flow = get_object_or_404(dataFlow,flow_name=flow_name)
    if request.method == "POST":
        s3Form = S3SourecsForm(request.POST)
        postgresfrom =  PygonSourceForm(request.POST)
        if s3Form.is_valid():
            aws_access_key_id = s3Form.cleaned_data['aws_access_key_id']
            aws_region = s3Form.cleaned_data['aws_region']
            aws_endpoint_url = s3Form.cleaned_data['aws_endpoint_url']
            aws_secret_access_key  = s3Form.cleaned_data['aws_secret_access_key']
            bucket_name = s3Form.cleaned_data['bucket_name']
            file_type = s3Form.cleaned_data['file_type']
            
            #save aws credential to prefect db
            save_asw_credentials(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                endpoint_url=aws_endpoint_url,
                region_name=aws_region,
                name=bucket_name.lower())
            

            isinstance = s3Form.save(commit=False)
            isinstance.dataflows = flow
            isinstance.save()
            
        elif postgresfrom.is_valid():
            #save postress credential to prefect db
            database_name = postgresfrom.cleaned_data['database_name']
            host = postgresfrom.cleaned_data['host']
            password = postgresfrom.cleaned_data['password']
            port = postgresfrom.cleaned_data['port']
            username = postgresfrom.cleaned_data['username']
            save_progres_credentials(
                 database_name=database_name.lower(),
                 host=host,password=password,port=port,
                 username=username
            )
           
            isinstance = postgresfrom.save(commit=False)
            isinstance.dataflows = flow
            isinstance.save()
        return HttpResponseRedirect('/flows/profile/')
    else:

        s3Form = S3SourecsForm()
        postgresfrom =  PygonSourceForm()

        flow = get_object_or_404(dataFlow,flow_name=flow_name)

   
    return render(request,'flowapp/flow_edit.html',{'s3Form':s3Form,'postgresfrom':postgresfrom,'flow':flow})

@login_required
def flow_delete(request,flow_name):
    flow = get_object_or_404(dataFlow,flow_name=flow_name)
    flow.delete()
    return HttpResponseRedirect('/flows/profile/')

@login_required
def runflow(request):
     user = UserProfile.objects.filter(user=request.user).first()
     dataflows = dataFlow.objects.get(profile=user)
     s3source_data_credential = S3Sourecs.objects.filter(dataflows=dataflows)
     postgress_data_credential = PygonSource.objects.filter(dataflows=dataflows)
     if s3source_data_credential.exists() and postgress_data_credential.exists():
        result = pull_data_from_s3_write_to_postgress(s3source_data_credential,postgress_data_credential)
        write_data_to_postgress(result)
     elif not s3source_data_credential.exists() and not postgress_data_credential.exists():
         pass
     else:
        result = pull_data_from_s3_write_to_postgress(s3source_data_credential,postgress_data_credential)
        write_data_to_postgress(result)
         
     return HttpResponseRedirect('/flows/profile/')

@login_required
def schedule(request):
    #run_deployment('hello_world/article-deployment',timeout=0)
    return HttpResponseRedirect('/flows/profile/')


