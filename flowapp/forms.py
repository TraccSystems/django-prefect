from django.forms import ModelForm
from . models import S3Sourecs,PygonSource,dataFlow,IntervalScheduleSchedule
from .models import PygonSource




class dataFlowForm(ModelForm):
    class Meta:
        model = dataFlow
        fields = ("flow_name","description")


class S3SourecsForm(ModelForm):
    class Meta:
        model = S3Sourecs
        fields = ("aws_access_key_id","aws_region","aws_endpoint_url",
                  "aws_secret_access_key","bucket_name",
                  "file_type")
        
class PygonSourceForm(ModelForm):
    class Meta:
        model = PygonSource
        fields = ("database_name","host","password","port","schema","username")


class IntervalScheduleScheduleForm(ModelForm):
    class Meta:
        model = IntervalScheduleSchedule
        fields = ("value","interval","start_date","timezone")





