from django.urls import path

from .views import CourseDetailView, CourseListView, UserDetailView, UserListView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("user/<slug>", UserDetailView.as_view(), name="user-detail"),
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("course/<int:pk>", CourseDetailView.as_view(), name="course-detail"),
]
