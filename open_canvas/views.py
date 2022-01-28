from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import CanvasSite, CanvasUser


class UserDetailView(DetailView):
    model = CanvasUser
    slug_field = "canvas_id"
    template_name = "canvasuser_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = self.object.courses.all()
        return context


class UserListView(ListView):
    model = CanvasUser
    paginate_by = 100
    template_name = "canvasuser_list.html"


class CourseDetailView(DetailView):
    model = CanvasSite
    template_name = "canvassite_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = self.object.users.all()
        return context


class CourseListView(ListView):
    model = CanvasSite
    paginate_by = 100
    template_name = "canvassite_list.html"
