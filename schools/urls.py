from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from schools import views

urlpatterns = [    
    path("", views.index, name="home"),
    path("schools", views.schools, name="schools"),
    path("school-details/<str:school_nu>", views.school_details, name="school_details"),
    path("offices-list", views.offices_list, name="offices_list"),
    path("office-details/<str:office_name>", views.office_details, name="office_details"),
    path("density", views.density, name="density"),
    path("export-excel", views.export_excel, name="export_excel"),
    path("filters", views.filters, name="filters"),
    path("projects/<str:project_type>", views.all_projects, name="all_projects"),
    path("projects-types", views.project_types, name="projects_types"),

    # auth urls
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]