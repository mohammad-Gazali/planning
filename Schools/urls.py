from django.urls import path
from django.views import View
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('details/<str:s>',views.details,name='detail'),
    path('offices_list',views.offices_list,name='offices_list'),
    path('office_details/<str:office_name>/<str:school_gender>/',views.office_details,name='office_details'),
    path('filters/',views.filters,name='filters'),
    path('ExportExcel',views.ExportExcel,name='ExportExcel'),
    path('office/<str:office>',views.office,name='office'),
    path('density/',views.density,name='density')

    ]