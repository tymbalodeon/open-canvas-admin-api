from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import CanvasUser, Course


class UserDetailView(DetailView):
    model = CanvasUser
    context_object_name = "user"
    slug_field = "canvas_id"
    template_name = "user_detail.html"


class UserListView(ListView):
    model = CanvasUser
    context_object_name = "users"
    paginate_by = 100
    template_name = "user_list.html"


class CourseDetailView(DetailView):
    model = Course
    template_name = "course_detail.html"


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    paginate_by = 100
    template_name = "course_list.html"
