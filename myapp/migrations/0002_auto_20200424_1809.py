# Generated by Django 3.0.5 on 2020-04-24 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_info',
            name='company',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='company_info',
            name='units',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='credit_info',
            name='bank',
            field=models.CharField(max_length=30),
        ),
    ]
