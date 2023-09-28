from django.shortcuts import get_object_or_404, render
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

        #connect to sub maps
        folium.GeoJson(
            data=jsondata,
            style_function=style_fcn,
            highlight_function=highlight_fcn,
            tooltip=folium.features.GeoJsonTooltip(
                fields=["name"],
                labels=False,
                style="background-color: #abdf8245;font-color: #abfd6532;font-size: 30px;color: black",
            )
        ).add_to(map)

        map_html = map._repr_html_()
    
    return render(request,"pages/index.html", { "map": map_html })


@login_required
def schools(request: HttpRequest) -> HttpResponse:
    
    school_name = request.GET.get("school_name") or ""

    schools = School.objects.filter(Q(school_name__contains = school_name) | Q(school_nu = school_name)).order_by("school_name")

    for group in request.user.groups.all():
        if group.name == "restricted_group":
            schools = School.objects.filter(Q(school_name__contains = school_name) | Q(school_nu = school_name), adminstration=request.user.first_name).order_by("school_name")

    paginator = Paginator(schools, 15)
    
    page_number = request.GET.get("page")
    
    page_object = paginator.get_page(page_number)

    return render(request, "pages/schools.html",{
        "page_object": page_object,
        "school_name": school_name,
    })


@login_required
def school_details(request: HttpRequest, school_nu: str) -> HttpResponse:

    school = get_object_or_404(School, school_nu=school_nu)

    map = folium.Map(
        location=[school.latitude, school.longitude],
        zoom_start=14,
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
        color_discrete_sequence=px.colors.sequential.Blues_r,
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
def filters(request: HttpRequest) -> HttpResponse:
    
    schools = School.objects.all()

    for group in request.user.groups.all():
        if group.name == "restricted_group":
            schools = School.objects.filter(adminstration=request.user.first_name)

    school_stages = set(school.school_stage for school in schools)
    school_offices = set(school.office for school in schools)
    school_genders = set(school.school_gender for school in schools)
    school_education_systems = set(school.school_education_system for school in schools)
    school_independence = set(school.independence for school in schools)
    school_building_states = set(school.building_state for school in schools)
    school_adminstrations = set(school.adminstration for school in schools)

    school_adminstration = request.POST.getlist("school_adminstration")
    school_gender = request.POST.getlist("school_gender")
    school_office = request.POST.getlist("school_office")
    school_education_system = request.POST.getlist("school_education_system")
    school_stage = request.POST.getlist("school_stage")
    independence = request.POST.getlist("independence")
    school_building_state = request.POST.getlist("school_building_state")

    if school_adminstration != []:
        schools = schools.filter(adminstration__in=school_adminstration)

    if school_gender != []:
        schools= schools.filter(school_gender__in=school_gender)

    if school_office != []:
        schools = schools.filter(office__in=school_office)

    if school_education_system != []:
        schools = schools.filter(school_education_system__in = school_education_system)

    if school_stage != []:
        schools = schools.filter(school_stage__in=school_stage)

    if independence != []:
        schools = schools.filter(independence__in = independence)

    if school_building_state != []:
        schools = schools.filter(building_state__in = school_building_state)


    request.session["ids"] = [school.school_nu for school in schools]

    return render(request,"pages/filters.html", {
        "schools": schools,
        "school_genders": school_genders,
        "school_offices" : school_offices,
        "school_stages" : school_stages,
        "school_education_systems":school_education_systems,
        "school_independence" : school_independence,
        "school_building_states" : school_building_states,
        "school_adminstrations" : school_adminstrations,
    })


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
def density(request: HttpRequest) -> HttpResponse:
    densities = OfficeDensity.objects.all().order_by(request.GET.get("order") or "office_nu")

    return render(request, "pages/density.html", {"densities": densities})


@login_required
def all_projects(request: HttpRequest, project_type: str) -> HttpResponse:

    projects = Project.objects.filter(project_type=project_type)

    # ========== This data can be used for testing this endpoint ==========
    # projects = [
    #     {"project_number": 1, "project_type": project_type, "project_name": "المشروع الأول", "project_gender": "بنين", "project_class_count": 30, "project_capacity": 200, "project_completion_rate": 70, "project_office": "المكتب الأول", "project_location": "https://google.com"},
    #     {"project_number": 2, "project_type": project_type, "project_name": "المشروع الثاني", "project_gender": "بنين", "project_class_count": 20, "project_capacity": 1000, "project_completion_rate": 10, "project_office": "المكتب الأول", "project_location": "https://google.com"},
    #     {"project_number": 3, "project_type": project_type, "project_name": "المشروع الثالث", "project_gender": "بنات", "project_class_count": 100, "project_capacity": 100, "project_completion_rate": 100, "project_office": "المكتب الأول", "project_location": "https://google.com"},
    #     {"project_number": 4, "project_type": project_type, "project_name": "المشروع الرابع", "project_gender": "بنين", "project_class_count": 190, "project_capacity": 200, "project_completion_rate": 92, "project_office": "المكتب الأول", "project_location": "https://google.com"},
    #     {"project_number": 5, "project_type": project_type, "project_name": "المشروع الخامس", "project_gender": "بنات", "project_class_count": 10, "project_capacity": 30, "project_completion_rate": 33, "project_office": "المكتب الأول", "project_location": "https://google.com"},
    # ]

    return render(request, "pages/projects.html", {
        "projects": projects,
        "project_type": project_type,
    })


@login_required
def project_types(request: HttpRequest) -> HttpResponse:
    
    project_types_query = set(project.project_type for project in Project.objects.all())

    # ========== This data can be used for testing this endpoint ==========
    # project_types_query = {"النوع الأول", "النوع الثاني", "النوع الثالث"}

    return render(request, "pages/projects_types.html", {"project_types": project_types_query})