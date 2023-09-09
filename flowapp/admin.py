from django.contrib import admin

from . models import *

# Register your models here.
admin.site.register(S3_connections_aws)
admin.site.register(S3_connections_digital_ocean)
admin.site.register(Postgress_connections)
admin.site.register(GoogleDrive_connection)
admin.site.register(Github_connection)
admin.site.register(Snowflake_connection)
admin.site.register(AzureblobContainer_connection)
admin.site.register(AzureblobStorage_connection)
admin.site.register(Pinecone_connection)
admin.site.register(SingleStoreDB_connections)
admin.site.register(Qdrant_connection)
admin.site.register(Weaviatdb_connection)
admin.site.register(Elasticsearch_connection)
admin.site.register(Flows)

