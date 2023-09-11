from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.db.models import Count, Sum
from django.conf import settings
from django.contrib.auth.decorators import login_required
from schools.models import School, OfficeDensity, Project
from schools.helpers import style_fcn, highlight_fcn
from xlwt import Worksheet
import folium
import xlwt
import plotly.express as px
import json
import os


@login_required
def index(request: HttpRequest) -> HttpResponse:
    
    with open(os.path.join(settings.BASE_DIR, "multi/offices.geojson"), encoding="utf8") as gd:
    
        jsondata = json.load(gd)
    
        map = folium.Map(
            location=[24.696,46.691],
            tiles="openstreetmap",
            zoom_start=10,
            control_scale=True
        )

        folium.GeoJson(jsondata).add_to(map)

        map_html = map._repr_html_()

        #connect to sub maps
        # folium.GeoJson(
        #     data=os.path.join(settings.BASE_DIR, 'multi/offices.geojson'),
        #     style_function=style_fcn,
        #     highlight_function=highlight_fcn,
        #     tooltip=folium.features.GeoJsonTooltip(
        #         fields=['name'],
        #         labels=False,
        #         style="background-color: #abdf8245;font-color: #abfd6532;font-size: 30px;color: black",
        #     )
        # ).add_to(map)
    
    return render(request,'pages/index.html', { 'map': map_html })


@login_required
def schools(request: HttpRequest) -> HttpResponse:
    
    school_name = request.GET.get("school_name") or ""

    schools = School.objects.filter(Q(school_name__contains = school_name) | Q(school_nu = school_name))

    schools = School.objects.filter(adminstration="إدارة التعليم بمحافظة الدوادمي")

    for group in request.user.groups.all():
        if group.name == "restricted_group":
            schools = School.objects.filter(Q(school_name__contains = school_name) | Q(school_nu = school_name), adminstration = request.user.first_name)

    paginator = Paginator(schools, 15)
    
    page_number = request.GET.get("page")
    
    page_object = paginator.get_page(page_number)

    page_range = paginator.page_range

    return render(request, "pages/schools.html",{
        "page_object": page_object,
        "school_name": school_name,
        "page_range": page_range,
    })


@login_required
def school_details(request: HttpRequest, school_nu: str) -> HttpResponse:

    school = get_object_or_404(School, school_nu=school_nu)

    map = folium.Map(
        location=[school.latitude, school.longitude],
        zoom_start=14,
        height=350,
    )

    html = f"""
    <div style="
        background-color: #73abe3;
        color: #fff;
        text-align: center;
        padding: 5px 0;
        border-radius: 6px;
    ">
        <h4 style="color:#f2f2f2; padding:0 5px;">{school.school_name}</h4>
    </div>
    """

    folium.Marker([school.latitude, school.longitude],
        tooltip=html,
        icon=folium.Icon(color="red", icon="university", prefix="fa"),
    ).add_to(map)
    
    map = map._repr_html_()

    return render(request,"pages/school_details.html", {
        "school": school,
        "map": map,
    })


@login_required
def offices_list(request: HttpRequest) -> HttpResponse:
    
    schools = School.objects.all().values("office").distinct()

    for group in request.user.groups.all():
        if group.name == "restricted_group":
            schools = School.objects.filter(adminstration=request.user.first_name).values("office").distinct()

    return render(request,"pages/offices_list.html",{
        "schools": schools,
    })


@login_required
def office_details(request: HttpRequest, office_name: str) -> HttpResponse:

    schools = School.objects.filter(office=office_name)

    #المتغيرات
    # أعداد المدارس الإجمالي للمكتب
    schools_count = School.objects.filter(office=office_name).aggregate(Count("school_nu"))
    class_count = School.objects.filter(office=office_name).aggregate(Sum("total_class"))
    total_sudents = School.objects.filter(office=office_name).aggregate(Sum("total_student"))

    # أعداد المدارس الإجمالي للمكتب بنين وبنات
    boys_schools = School.objects.filter(school_gender="بنين", office=office_name ).aggregate(Sum("total_student"))
    girls_schools =  School.objects.filter(school_gender="بنات", office=office_name).aggregate(Sum("total_student"))

    # أعداد المدارس الإجمالي للمكتب بنين وبنات
    # تصنيف المدارس
    mustaqel =  School.objects.filter(independence="مستقلة", office=office_name).count()
    mushtarak =  schools_count["school_nu__count"] - mustaqel

    # الشارت
    names = ["مستقلة", "مشتركة"]
    values = [mustaqel, mushtarak]

    fig = px.pie(
        values=values,
        names=names,
        color_discrete_sequence=px.colors.sequential.Blues,
        labels=names,
        hole=0.5,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont_size=20,
        hovertemplate=None,
    )

    # العنوان
    fig.update_layout()

    fig_html = fig.to_html(
        config={
            "displayModeBar": False,
        }
    )

    # الخريطة
    latitude = schools[2].latitude
    longitude = schools[2].longitude
    map = folium.Map(
        location=[latitude, longitude],
        tiles=None,
        zoom_start=12,
        control_scale=True,
    )

    # base map
    base_map = folium.FeatureGroup(name="Basemap", overlay=True, control=False)
    folium.TileLayer(tiles="OpenStreetMap").add_to(base_map)
    base_map.add_to(map)

    for school in schools:
        html = f"""
            <table 
            class="table table-bordered rounded" 
            style="
                background-color:  #385370;
                direction: rtl;
                color: #fff;
                text-align: center;
            ">
                <caption style="background-color: #4B91C5;padding: 2px;">{school.school_name}</caption>
                <tbody>
                    <tr>
                        <td>الرقم الإحصائي</td>
                        <td>{school.school_nu}</td>
                    </tr>
                    <tr>
                        <td>المكتب</td>
                        <td>{school.office}</td>
                    </tr>
                    <tr>
                        <td>المرحلة</td>
                        <td>{school.school_stage}</td>
                    </tr>
                    <tr>
                        <td>جنس المدرسة</td>
                        <td>{school.school_gender}</td>
                    </tr>
                    <tr>
                        <td>عدد الطلاب</td>
                        <td>{school.total_student}</td>
                    </tr>
                    <tr>
                        <td>معدل الكثافة</td>
                            <td>{school.density}</td>
                        </tr>
                        <tr>
                            <td>الحي</td>
                            <td>{school.school_quarter}</td>
                        </tr>
                    </tbody>
            </table>
            """
        
        if type(school.latitude) == float and type(school.longitude) == float:

            if school.school_gender == "بنين":
                folium.Marker(
                    location=[school.latitude, school.longitude],
                    tooltip=html,
                ).add_to(map)

            if school.school_gender == "بنات":
                folium.Marker(
                    location=[school.latitude, school.longitude],
                    tooltip=html,
                    icon=folium.Icon(color= "purple"),
                ).add_to(map)

        if school.density > 35 and school.independence != "مشترك ملحق":
            folium.CircleMarker(
                location=[school.latitude, school.longitude],
                radius=18,
                color="#F87217",
                fill=True,
                fill_color="#F87217",
                fill_opacity=0.5,
            ).add_to(map)

    # add layer control
    folium.LayerControl(collapsed=False).add_to(map)

    map_html = map._repr_html_()

    return render(request, "pages/office_details.html", {
        "map": map_html,
        "office_name": office_name,
        "boys_schools": boys_schools,
        "girls_schools": girls_schools,
        "schools_count": schools_count,
        "fig": fig_html,
        "class_count": class_count,
        "total_sudents": total_sudents,
    })


@login_required
def density(request: HttpRequest) -> HttpResponse:
    
    densities = OfficeDensity.objects.all()

    return render(request, "pages/density.html", {"densities": densities})


@login_required
def export_excel(request: HttpRequest) -> HttpResponse:

    schools = School.objects.filter(school_nu__in=request.session["ids"])

    style = xlwt.easyxf("font: bold 1, color blue;")
    style_data = xlwt.easyxf()

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment;filename=Report.xls"

    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet: Worksheet = workbook.add_sheet("ورقة1")
    worksheet.cols_right_to_left = True

    # Generate worksheet head row data.
    worksheet.write(0, 0, "الرقم الوزاري", style=style)
    worksheet.write(0, 1, "اسم المدرسة", style=style)
    worksheet.write(0, 2, "جنس المدرسة", style=style)
    worksheet.write(0, 3, "المرحلة", style=style)
    worksheet.write(0, 4, "الحي", style=style)
    worksheet.write(0, 5, "مكتب التعليم", style=style)
    worksheet.write(0, 6, "نظام التعليم", style=style)
    worksheet.write(0, 7, "عدد الطلاب ", style=style)
    worksheet.write(0, 8, "عدد الفصول ", style=style)
    worksheet.write(0, 9, "الاستقلالية ", style=style)
    worksheet.write(0, 10, "المدرسة الأساسية ", style=style)
    worksheet.write(0, 11, "خط الطول ", style=style)
    worksheet.write(0, 12, "خط العرض ", style=style)
    worksheet.write(0, 13, "إدارة التعليم ", style=style)

    row = 1

    for school in schools:
        worksheet.write(row, 0, school.school_nu, style=style_data)
        worksheet.write(row, 1, school.school_name, style=style_data)
        worksheet.write(row, 2, school.school_gender, style=style_data)
        worksheet.write(row, 3, school.school_stage, style=style_data)
        worksheet.write(row, 4, school.school_quarter, style=style_data)
        worksheet.write(row, 5, school.office, style=style_data)
        worksheet.write(row, 6, school.school_education_system, style=style_data)
        worksheet.write(row, 7, school.total_student, style=style_data)
        worksheet.write(row, 8, school.total_class, style=style_data)
        worksheet.write(row, 9, school.independence, style=style_data)
        worksheet.write(row, 10, school.main_school, style=style_data)
        worksheet.write(row, 11, school.longitude, style=style_data)
        worksheet.write(row, 12, school.latitude, style=style_data)
        worksheet.write(row, 13, school.adminstration, style=style_data)

        row += 1

    workbook.save(response)

    return response


@login_required
def filters(request: HttpRequest) -> HttpResponse:
    
    school_stage = School.objects.values('school_stage').distinct()
    s_office = School.objects.values('office').distinct()
    s_gender = School.objects.values('school_gender').distinct()
    e_s = School.objects.values('school_education_system').distinct()
    s_independence = School.objects.values('independence').distinct()
    s_building_state = School.objects.values('building_state').distinct()
    adminstration = School.objects.values('adminstration').distinct()

    for group in request.user.groups.all():
        if group.name == 'restricted_group':
            school_stage = School.objects.filter(adminstration = request.user.first_name).values('school_stage').distinct()
            s_office = School.objects.filter(adminstration = request.user.first_name).values('office').distinct()
            s_gender = School.objects.filter(adminstration = request.user.first_name).values('school_gender').distinct()
            e_s = School.objects.filter(adminstration = request.user.first_name).values('school_education_system').distinct()
            s_independence = School.objects.filter(adminstration = request.user.first_name).values('independence').distinct()
            s_building_state = School.objects.filter(adminstration = request.user.first_name).values('building_state').distinct()
            adminstration = School.objects.filter(adminstration = request.user.first_name).values('adminstration').distinct()  
    
    qs = School.objects.all()

    stage = request.POST.getlist('stage')
    office = request.POST.getlist('office')
    gender = request.POST.getlist('gender')
    ef_s = request.POST.getlist('e_system')
    independence = request.POST.getlist('independence')
    building_state = request.POST.getlist('building_state')
    s_adminstration = request.POST.getlist('school_adminstration')

    if stage != '' and stage is not None:
        qs = qs.filter(school_stage__in=stage)
    else:
        qs = qs.values_list("school_stage")

    if office != '' and office is not None:
        qs = qs.filter(office__in=office)

    if gender != '' and gender is not None:
        qs= qs.filter(school_gender__in=gender)

    if ef_s != '' and ef_s is not None:
        qs = qs.filter(school_education_system__in = ef_s)

    if independence != '' and independence is not None:
        qs = qs.filter(independence__in = independence)

    if building_state != '' and building_state is not None:
        qs = qs.filter(building_state__in = building_state)

    if s_adminstration != '' and s_adminstration is not None:
        qs = qs.filter(adminstration__in = s_adminstration)

    request.session['ids'] = [school.school_nu for school in qs]

    context = {
        's_gender':s_gender,
        's_office' : s_office,
        'school_stage' : school_stage,
        'e_system':e_s,
        'queryset' : qs,
        's_independence' : s_independence,
        's_building_state' : s_building_state,
        'adminstration' : s_adminstration
    }

    request.session['ids'] = [school.school_nu for school in qs]

    context = {
        's_gender':s_gender,
        's_office' : s_office,
        'school_stage' : school_stage,
        'e_system':e_s,
        'queryset' : qs,
        's_independence' : s_independence,
        's_building_state' : s_building_state,
        'adminstration' : adminstration,
    }

    return render(request,'pages/filters.html', context)


@login_required
def all_projects(request: HttpRequest, project_type) -> HttpResponse:

    context = Project.objects.filter(project_type=project_type)

    return render(request, 'pages/projects.html', {'context' :context})


@login_required
def project_types(request: HttpRequest) -> HttpResponse:
    
    context = Project.objects.values('project_type').distinct()

    return render(request, 'pages/projects_types.html', {'context':context})