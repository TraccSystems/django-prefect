from django.db import models
from django.conf import settings
# Create your models here.

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin


class flowUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None):
        user = self.create_user(
            email,
            password=password,
          
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class flowUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = flowUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
       
        return True

    def has_module_perms(self, app_label):
        
        return True

    @property
    def is_staff(self):
       
        return self.is_admin
    



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image = models.FileField(upload_to='profile/')
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email
    


class dataFlow(models.Model):
    flow_name = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    created_at = models.DateField(auto_now=True)
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.flow_name
    
    class Mata:
        ordering =['created_at']
    

class S3Sourecs(models.Model):
    aws_access_key_id = models.CharField(max_length=200,unique=True)
    aws_region   = models.CharField(max_length=200)
    aws_endpoint_url  = models.CharField(max_length=200)
    aws_secret_access_key   = models.CharField(max_length=200)
    bucket_name  = models.CharField(max_length=200,unique=True)
    file_type   = models.CharField(max_length=200,default='csv')
    created_at = models.DateField(auto_now=True)
    dataflows = models.ForeignKey(dataFlow,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.bucket_name

    class Meta:
        ordering = ['created_at']


class PygonSource(models.Model):
    database_name = models.CharField(max_length=20,unique=True)
    host = models.CharField(max_length=30)
    password = models.CharField(max_length=16,unique=True)
    port = models.CharField(max_length=5,default='5423')
    schema = models.CharField(max_length=20,default='public')
    username = models.CharField(max_length=20,unique=True)
    created_at = models.DateField(auto_now=True)
    dataflows = models.ForeignKey(dataFlow,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.database_name 

    class Meta:
        ordering = ['created_at']

class IntervalScheduleSchedule(models.Model):
    interval_select = [('Minutes','Minutes'),('Hours','Hours'),('Seconds','Seconds')]
    timezone_value  = [('UTC','UTC')]
    value = models.CharField(max_length=20)
    interval = models.CharField(max_length=20,choices=interval_select)
    start_date = models.DateTimeField()
    timezone = models.CharField(max_length=255,choices=timezone_value)
    dataflows = models.ForeignKey(dataFlow,on_delete=models.CASCADE)


    class Meta:
        ordering = ['start_date']



     





