from django.db import models


class School(models.Model):
    school_nu = models.CharField(max_length=30, primary_key=True, default='1')
    school_name = models.CharField(max_length=500, blank=True, null=True)
    school_rule = models.CharField(max_length=500, blank=True, null=True)
    school_stage = models.CharField(max_length=50, blank=True, null=True)
    school_gender = models.CharField(max_length=50, blank=True, null=True)
    total_student= models.IntegerField(null=True,blank=True)
    total_class= models.IntegerField(null=True,blank=True)
    office = models.CharField(max_length=500, blank=True, null=True)
    school_education_system = models.CharField(max_length=50, blank=True, null=True)
    school_quarter = models.CharField(max_length=500, blank=True, null=True)
    school_manager_name = models.CharField(max_length=500, blank=True, null=True)
    school_manager_mobile = models.CharField(max_length=500, blank=True, null=True)
    independence = models.CharField(max_length=500, blank=True, null=True)
    building_state = models.CharField(max_length=500, blank=True, null=True)
    main_school = models.CharField(max_length=500, blank=True, null=True)
    school_in = models.IntegerField(default=1)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    density = models.IntegerField(null=True,blank=True)
    adminstration = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.school_name


class OfficeDensity(models.Model):
    office_nu = models.CharField(max_length=30, primary_key=True, default='1')
    office_name = models.CharField(max_length=500, blank=True, null=True)
    office_density = models.IntegerField(default=0)
    childhold_density = models.IntegerField(default=0)
    primary_density = models.IntegerField(default=0)
    elementry_density= models.IntegerField(default=0)
    secondary_density= models.IntegerField(default=0)

    def __str__(self):
        return self.office_name
    

    
class Project(models.Model):
    project_number = models.IntegerField(null=True, blank=True)
    project_type = models.CharField(max_length=500, blank=True, null=True)
    project_name = models.CharField(max_length=500, blank=True, null=True)
    project_gender = models.CharField(max_length=50, blank=True, null=True)
    project_class_count = models.IntegerField(default=0)
    project_capacity =  models.IntegerField(default=0)
    project_completion_rate =models.DecimalField(max_digits=6, decimal_places=2)
    project_office = models.CharField(max_length=500, blank=True, null=True)
    project_location = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return self.project_name
