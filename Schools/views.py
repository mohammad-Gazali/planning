from multiprocessing import context
from pickle import FALSE
import re
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
import folium
import Schools
from .models import school
from .models import projects
from django.contrib.auth.models import User
from django.db.models import Q

app_name= Schools



def index(request):
    sn = request.GET.get('schoolname')
    if not sn:
        sn=''
    schools = school.objects.filter(Q(school_name__contains = sn) | Q(school_nu = sn) )
    paginator = Paginator(schools, 10)
    page_number = request.GET.get('page')
    s = paginator.get_page(page_number)
    return render(request,'schools/index.html',{'s':s,'sn':sn})
    # return render(request,'Schools/index.html' )

def details(request,s):
    d = get_object_or_404(school,school_nu = s)

    

    map = folium.Map([d.latitude, d.longitude] ,
     zoom_start=14,
     height=350,

     )
 
    
    html = f"""
    
    <div >
            <h6 style="color:blue;">  {d.school_name}</h6>
            <h6 style="color:blue;">  {d.school_stage}</h6>
            </div>
    """ 
    folium.Marker([d.latitude, d.longitude],
        tooltip=html,
        #popup=popup,
        icon=folium.Icon(color="red", icon='university', prefix='fa'),
        ).add_to(map)
    map=map._repr_html_()



    context={
        'd':d,
        'map' : map
    }

    return render(request,'schools/details.html',context)





def offices_list(request):
    b = school.objects.filter(school_gender__exact="بنين").values('office').distinct()
    g = school.objects.filter(school_gender__exact="بنات").values('office').distinct()
    return render(request,'schools/offices_list.html',{'b':b,'g':g})


def office_details(request,office_name):
    od = school.objects.filter(office = office_name ) 
    paginator = Paginator(od, 10)
    page_number = request.GET.get('page')
    od = paginator.get_page(page_number)
    return render(request,'schools/office_details.html',{'od':od,'office_name': office_name})

def all_projects(request):
    context = projects.objects.all()
    return render(request,'schools/projects.html',{'context' :context})


