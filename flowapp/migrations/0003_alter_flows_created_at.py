# Generated by Django 4.2.4 on 2023-09-02 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowapp', '0002_alter_pinecone_connection_pincon_connection_types_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flows',
            name='created_at',
            field=models.DateField(),
        ),
    ]