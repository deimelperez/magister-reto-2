# Generated by Django 3.2 on 2021-05-01 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readPdfs', '0004_auto_20210501_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='exclusion',
        ),
        migrations.AddField(
            model_name='teacher',
            name='exclusion',
            field=models.ManyToManyField(blank=True, to='readPdfs.Exclusion'),
        ),
    ]
