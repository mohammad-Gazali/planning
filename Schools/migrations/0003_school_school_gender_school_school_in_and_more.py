# Generated by Django 4.0.2 on 2022-02-23 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schools', '0002_alter_school_latitude_alter_school_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='school_gender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='school_in',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='school',
            name='school_stage',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
