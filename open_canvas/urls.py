from django.urls import path

from open_canvas.views import view_courses, view_users

urlpatterns = [path("users/", view_users), path("courses/", view_courses)]
