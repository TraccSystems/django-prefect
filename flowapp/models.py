from django.db import models
from django.conf import settings
import pytz
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
    
    

class S3_connections_digital_ocean(models.Model):
    connection_name = models.CharField(max_length=255)
    CONNECTION = [('Source','Source'),('Target','Target')]
    aws_access_key_id = models.CharField(max_length=200,unique=True)
    aws_region = models.CharField(max_length=200)
    aws_endpoint_url  = models.CharField(max_length=200)
    aws_secret_access_key  = models.CharField(max_length=200)
    bucket_name  = models.CharField(max_length=200,unique=True)
    file_type  = models.CharField(max_length=200,default='csv')
    s3_connection_type = models.CharField(max_length=10,choices=CONNECTION)
    created_at = models.DateField(auto_now=True)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.connection_name

    class Meta:
        ordering = ['created_at']



class S3_connections_aws(models.Model):
    connection_name = models.CharField(max_length=255)
    CONNECTION = [('Source','Source')]
    aws_access_key_id = models.CharField(max_length=200,unique=True)
    key = models.CharField(max_length=200)
    aws_secret_access_key  = models.CharField(max_length=200)
    bucket_name  = models.CharField(max_length=200,unique=True)
    file_type  = models.CharField(max_length=200,default='csv')
    s3_connection_type = models.CharField(max_length=10,choices=CONNECTION)
    created_at = models.DateField(auto_now=True)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.connection_name

    class Meta:
        ordering = ['created_at']


class Postgress_connections(models.Model):
    connection_name = models.CharField(max_length=255)
    CONNECTION = [('Source','Source')]
    database_name = models.CharField(max_length=20,unique=True)
    host = models.CharField(max_length=30)
    password = models.CharField(max_length=16,unique=True)
    port = models.CharField(max_length=5,default='5423')
    username = models.CharField(max_length=20,unique=True)
    post_connection_type = models.CharField(max_length=10,choices=CONNECTION)
    created_at = models.DateField(auto_now=True)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.connection_name


    class Meta:
        ordering = ['created_at']



class Pinecone_connection(models.Model):
    connection_name = models.CharField(max_length=255)
    CONNECTION = [('Target','Target')]
    api_key = models.CharField(max_length=255,unique=True)
    environment = models.CharField(max_length=255)
    index_name = models.CharField(max_length=255)
    pincon_connection_types = models.CharField(max_length=10,choices=CONNECTION)
    created_at = models.DateField(auto_now=True)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.connection_name
    

    class Meta:
        ordering = ['created_at']


class SingleStoreDB_connections(models.Model):
    connection_name = models.CharField(max_length=255)
    CONNECTION = [('Target','Target')]
    single_connection_types = models.CharField(max_length=10,choices=CONNECTION)
    table_name = models.CharField(max_length=255,default='scrap_data')
    created_at = models.DateField(auto_now=True)
    singledb_url = models.CharField(max_length=255)
    created_at = models.DateField(auto_now=True)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    
    def __str__(self) -> str:
        return self.connection_name 
    
    class Meta:
        ordering = ['created_at']



class Flows(models.Model):
    all_timezones = pytz.all_timezones
    time_zone_choices = [(tz, tz) for tz in all_timezones]
    time_zone_choices.sort(key=lambda x: x[0])
    source = models.ForeignKey(S3_connections_aws,on_delete=models.CASCADE)
    target = models.ForeignKey(Pinecone_connection,on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    scheduel_time = models.DateTimeField()
    time_zone = models.CharField(max_length=255,choices=time_zone_choices)

    def __str__(self) -> str:
        return self.target

    class Meta:
        ordering = ['scheduel_time']



class Flows_s3_to_singlestore(models.Model):
    source = models.ForeignKey(S3_connections_aws,on_delete=models.CASCADE)
    target = models.ForeignKey(SingleStoreDB_connections,on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.target

    class Meta:
        ordering = ['created_at']



class Flows_postgress_to_pinecone(models.Model):
    source = models.ForeignKey(Postgress_connections,on_delete=models.CASCADE)
    target = models.ForeignKey(Pinecone_connection,on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.target

    class Meta:
        ordering = ['created_at']



class Flows_postgress_to_singlestore(models.Model):
    source = models.ForeignKey(Postgress_connections,on_delete=models.CASCADE)
    target = models.ForeignKey(SingleStoreDB_connections,on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.target

    class Meta:
        ordering = ['created_at']




