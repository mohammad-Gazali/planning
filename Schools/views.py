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
from folium import GeoJsonTooltip, plugins

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

    m = folium.Map(location=[24.696934226366672,46.69189453125]  ,  tiles=None ,zoom_start=12, control_scale=True)
    base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
    folium.TileLayer(tiles='OpenStreetMap').add_to(base_map)
    base_map.add_to(m)
    for i in od:
        if type(i.latitude ) == float :
            if type(i.longitude ) == float :
                folium.Marker([i.latitude,i.longitude]).add_to(m)

    #add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    m = m._repr_html_()
    # الخريطة


    paginator = Paginator(od, 10)
    page_number = request.GET.get('page')
    od = paginator.get_page(page_number)
    return render(request,'schools/office_details.html',{'od':od,'office_name': office_name,'m':m})

def all_projects(request,project_type):
    context = projects.objects.filter(project_type=project_type)
    return render(request,'schools/projects.html',{'context' :context})



def ProjectTypes(request):
    #context = projects.objects.filter(project_type='مشاريع تم تشغيلها خلال العام الدراسي الحالي')
    context = projects.objects.values('project_type').distinct() #.values_list('project_type',flat=True).distinct()
    return render(request,'schools/ProjectsTypes.html',{'context':context})

