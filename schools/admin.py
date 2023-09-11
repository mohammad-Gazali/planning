from django.contrib import admin
from schools import models

@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    pass