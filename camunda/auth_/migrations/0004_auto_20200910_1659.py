# Generated by Django 3.1.1 on 2020-09-10 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0003_mainuser_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainuser',
            name='fio',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ФИО сотрудника'),
        ),
    ]
