# Generated by Django 4.0.4 on 2022-05-31 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Schools', '0014_school_total_class_school_total_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school_note',
            name='created_user',
        ),
        migrations.DeleteModel(
            name='note',
        ),
        migrations.DeleteModel(
            name='school_note',
        ),
    ]
