from ast import alias
from dataclasses import field
from click import style
from django.shortcuts import render
import folium
import json
import os
from django.conf import settings
import random
from folium import GeoJsonTooltip, plugins
from Schools.models import school




# Create your views here.
def random_html_color():
    r = random.randint(0,256)
    g = random.randint(0,256)
    b = random.randint(0,256)
    return '#%02x%02x%02x' % (r, g, b)
def style_fcn(x):
    return { 'fillColor': random_html_color(),
              'weight' : 1,
            'fillOpacity' : 0.5,
            'color':'#0C58A7',
            'radious': '3px',

    }
def highlight_fcn(x):
    return { 'fillColor': '#000000' }
# cordinate start


def index(request):
    gd = open(os.path.join(settings.BASE_DIR, 'multi/offices.geojson'))#  الحصول على كل الاحداثيات
    jsondata = json.load(gd)
    m = folium.Map(location=[24.696934226366672,46.69189453125]  ,  tiles=None ,zoom_start=10, control_scale=True)



    #mini map
    MiniMap = plugins.MiniMap(toggle_display=True)
    m.add_child(MiniMap)
    plugins.Fullscreen(position='topright').add_to(m)

    #base map
    base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
    folium.TileLayer(tiles='OpenStreetMap').add_to(base_map)
    base_map.add_to(m)


    #boys sub group

    boys = plugins.FeatureGroupSubGroup(base_map,'بنين',overlay=False)
    m.add_child(boys)


    #girls sub groups
    girls = plugins.FeatureGroupSubGroup(m,'بنات',overlay=False)
    m.add_child(girls)
    
    #connect to sub maps
    folium.GeoJson(os.path.join(settings.BASE_DIR, 'multi/boys.geojson' ),
    style_function=style_fcn,
    highlight_function=highlight_fcn ,
    tooltip=folium.features.GeoJsonTooltip(
         fields=['name'],
         labels=False,
         style=("background-color: #abdf8245;font-color: #abfd6532;font-size: 30px;color: black"),
         
     )
    
    ).add_to(boys)
    folium.GeoJson(os.path.join(settings.BASE_DIR, 'multi/girls.geojson'),
    style_function=style_fcn,
    highlight_function=highlight_fcn ,
    
    ).add_to(girls)

    markerdata = school.objects.all()

    # for i in markerdata:
    #     if type(i.latitude ) == float :
    #         if type(i.longitude ) == float :
    #             folium.Marker([i.latitude,i.longitude]).add_to(boys)

    
    #add layer control
    folium.LayerControl(collapsed=False).add_to(m)


    # subgroups


    
   

 

    #render map
    m = m._repr_html_()
    m={
        'm':m,
        
        }
    return render(request,'pages/index.html',m)






