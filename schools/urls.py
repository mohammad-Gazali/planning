from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from schools import views

urlpatterns = [    
    path("", views.index, name="home"),
    path("schools", views.schools, name="schools"),
    path("density", views.density, name="density"),
    path("office/<str:office>", views.office, name="office"),
    path("export-excel", views.export_excel, name="export_excel"),
    path("details/<str:s>", views.details, name="details"),
    path("offices-list", views.offices_list, name="offices_list"),
    path("office-details/<str:office_name>/<str:school_gender>", views.office_details, name="office_details"),
    path("filters", views.filters, name="filters"),
    path('projects/<str:project_type>', views.all_projects, name='all_projects'),
    path('projects-types/', views.project_types, name='projects_types'),

    # auth urls
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]