from django.shortcuts import render
from .models import CanvasUser, CanvasSite


def view_users(request):
    users = CanvasUser.objects.all()
    users = [
        {
            "user": user,
            "full_name": user.get_full_name(),
            "sortable_name": user.get_sortable_name(),
            "courses": user.courses.all(),
        }
        for user in users
    ]
    return render(request, "users.html", {"users": users})


def view_courses(request):
    sites = CanvasSite.objects.all()
    sites = [{"site": site, "users": site.users.all()} for site in sites]
    return render(request, "courses.html", {"sites": sites})
