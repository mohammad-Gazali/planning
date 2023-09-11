from django.http import HttpRequest

def schools_processor(request: HttpRequest):
    return {
        "is_restricted_user": bool(request.user.groups.filter(name='restricted_group')),
    }
