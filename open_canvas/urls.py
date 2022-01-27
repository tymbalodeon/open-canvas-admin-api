from django.urls import path
from open_canvas.views import view_demo

urlpatterns = [
    path("", view_demo),
]
