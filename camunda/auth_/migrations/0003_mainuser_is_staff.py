# Generated by Django 3.1.1 on 2020-09-10 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0002_mainuser_camunda_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
