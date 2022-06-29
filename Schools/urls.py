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
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
    
>>>>>>> c809a56f48d88c241dba499d48092d190fef419c
>>>>>>> b094c157388f3a4b3bff4b7960304089cf37658b
>>>>>>> 14dae33cdcb80f8a14e5a6e043076bd03443d115
    ]