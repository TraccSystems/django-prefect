# Generated by Django 4.2.4 on 2023-08-24 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flowapp', '0005_remove_postgress_connections_schema'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('S3', 'S3')], max_length=255)),
                ('target', models.CharField(choices=[('Pincone', 'Pincone'), ('Postgress', 'Postgress'), ('SingleStore', 'SingleStore')], max_length=255)),
                ('created_at', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowapp.userprofile')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
