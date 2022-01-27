from django.shortcuts import render
from .models import CanvasUser, CanvasSite


def view_demo(request):
    users = CanvasUser.objects.all()
    sites = CanvasSite.objects.all()
    return render(request, "demo.html", {"users": users, "sites": sites})
