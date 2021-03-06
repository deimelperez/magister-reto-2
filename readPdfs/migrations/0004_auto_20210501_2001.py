# Generated by Django 3.2 on 2021-05-01 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('readPdfs', '0003_auto_20210501_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access',
            name='code',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='access',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='readPdfs.access'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='corp',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='readPdfs.corp'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='dat',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='readPdfs.dat'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='exclusion',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='readPdfs.exclusion'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='specialty',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='readPdfs.specialty'),
        ),
    ]
