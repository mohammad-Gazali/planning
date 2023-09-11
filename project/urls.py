from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # project apps urls
    path("", include("schools.urls")),
]
