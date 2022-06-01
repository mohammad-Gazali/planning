# Generated by Django 4.0.2 on 2022-02-23 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schools', '0003_school_school_gender_school_school_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='school',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
    ]
