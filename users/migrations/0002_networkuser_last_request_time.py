# Generated by Django 4.2.5 on 2023-09-17 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkuser',
            name='last_request_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
