from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Course, CanvasUser


class UserDetailView(DetailView):
    model = CanvasUser
    context_object_name = "user"
    slug_field = "canvas_id"
    template_name = "canvasuser_detail.html"


class UserListView(ListView):
    model = CanvasUser
    context_object_name = "users"
    paginate_by = 100
    template_name = "canvasuser_list.html"


class CourseDetailView(DetailView):
    model = Course
    context_object_name = "site"
    template_name = "canvassite_detail.html"


class CourseListView(ListView):
    model = Course
    context_object_name = "sites"
    paginate_by = 100
    template_name = "canvassite_list.html"
