from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.



class school(models.Model):
    school_nu = models.CharField(max_length=30, primary_key=True,default='1')
    school_name = models.CharField(max_length=500, blank=True, null=True)
    school_rule = models.CharField(max_length=500, blank=True, null=True)
    school_stage = models.CharField(max_length=50, blank=True, null=True)
    school_gender = models.CharField(max_length=50, blank=True, null=True)
    total_student= models.IntegerField(null=True,blank=True)
    total_class= models.IntegerField(null=True,blank=True)
    office = models.CharField(max_length=500, blank=True, null=True)
    school_education_system = models.CharField(max_length=50, blank=True, null=True)
    school_Quarter = models.CharField(max_length=500, blank=True, null=True)
    school_manager_name = models.CharField(max_length=500, blank=True, null=True)
    school_manager_mobile = models.CharField(max_length=500, blank=True, null=True)
    independence = models.CharField(max_length=500, blank=True, null=True)
    BuildingState = models.CharField(max_length=500, blank=True, null=True)
    MainSchool = models.CharField(max_length=500, blank=True, null=True)
    school_in = models.IntegerField(default=1)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    density = models.IntegerField(null=True,blank=True)
    adminstration = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.school_name


class office_density(models.Model):
    office_nu = models.CharField(max_length=30, primary_key=True,default='1')
    office_name = models.CharField(max_length=500, blank=True, null=True)
    office_density = models.IntegerField(default=0)
    childHold_density = models.IntegerField(default=0)
    primary_density = models.IntegerField(default=0)
    elementry_density= models.IntegerField(default=0)
    secondary_density= models.IntegerField(default=0)


    def __str__(self):
        return self.office_name







