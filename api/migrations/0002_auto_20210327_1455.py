# Generated by Django 3.0.7 on 2021-03-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='value',
            field=models.IntegerField(),
        ),
    ]
