from django.shortcuts import render,redirect
import folium
import json
import os
from django.conf import settings
import random
from folium import plugins


# Create your views here.
def random_html_color():
    r = random.randint(0,256)
    g = random.randint(0,256)
    b = random.randint(0,256)
    return '#%02x%02x%02x' % (r, g, b)
def style_fcn(x):
    return { 'fillColor': random_html_color(),
              'weight' : 1,
            'fillOpacity' : 0.25,
            'color':'#32a852',
            'radious': '20px',

    }
def highlight_fcn(x):
    return { 'fillColor': '#000000' }
# cordinate start





def index(request):
    val = False
    if request.user.groups.filter(name='restricted_group').exists():
        val=True
    if not request.user.is_authenticated:
        return redirect('login')
    gd = open(os.path.join(settings.BASE_DIR, 'multi/offices.geojson'))
    jsondata = json.load(gd)
    m = folium.Map(location=[24.696,46.691]  ,  tiles="openstreetmap" ,zoom_start=10, control_scale=True)
    folium.GeoJson(jsondata).add_to(m)
    #test


    #mini map
    # MiniMap = plugins.MiniMap(toggle_display=True)
    # m.add_child(MiniMap)
    # plugins.Fullscreen(position='topright').add_to(m)

    #base map
    #base_map = folium.map(name='Basemap', overlay=True, control=False)
    # folium.TileLayer(tiles='OpenStreetMap').add_to(base_map)
    #base_map.add_to(m)


    #boys sub group

    # boys = plugins.FeatureGroupSubGroup(base_map,'بنين',overlay=False)

    # m.add_child(boys)


    # #girls sub groups
    # girls = plugins.FeatureGroupSubGroup(m,'بنات',overlay=False)
    # m.add_child(girls)

    # #connect to sub maps
    folium.GeoJson(os.path.join(settings.BASE_DIR, 'multi/offices.geojson'),
    style_function=style_fcn,
    highlight_function=highlight_fcn ,
    tooltip=folium.features.GeoJsonTooltip(
         fields=['name'],
         labels=False,
         style=("background-color: #abdf8245;font-color: #abfd6532;font-size: 30px;color: black"),

      )
    ).add_to(m)
    # folium.GeoJson(os.path.join(settings.BASE_DIR, 'multi/girls.geojson'),
    # style_function=style_fcn,
    # highlight_function=highlight_fcn ,
    # ).add_to(girls)

    #add layer control
    # folium.LayerControl(collapsed=False).add_to(m)


    # subgroups








    #render map
    m = m._repr_html_()
    return render(request,'pages/index.html',{'m':m, 'is_restricted_user':val})






