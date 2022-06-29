from django.urls import path
from django.views import View
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('details/<str:s>',views.details,name='detail'),
    path('offices_list',views.offices_list,name='offices_list'),
    path('office_details/<str:office_name>',views.office_details,name='office_details'),
    path('projects/<str:project_type>',views.all_projects,name='all_projects'),
    path('ProjectsTypes/',views.ProjectTypes,name='ProjectsTypes'),

    ]