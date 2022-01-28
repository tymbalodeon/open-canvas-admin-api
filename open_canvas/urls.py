from django.urls import path

from open_canvas.views import (
    UserListView,
    CourseListView,
    UserDetailView,
    CourseDetailView,
)

urlpatterns = [
    path("users/", UserListView.as_view()),
    path("user/<slug>", UserDetailView.as_view(), name="user-detail"),
    path("courses/", CourseListView.as_view()),
    path("course/<int:pk>", CourseDetailView.as_view(), name="course-detail"),
]
