from django.urls import path

from . import views


urlpatterns = [
    path(
        'colleges/',
        views.CollegeListCreateAPIView.as_view(),
        name='api-college-list',
    ),
    path(
        'colleges/<int:pk>/',
        views.CollegeDetailAPIView.as_view(),
        name='api-college-detail',
    ),
    path(
        'programs/',
        views.ProgramListCreateAPIView.as_view(),
        name='api-program-list',
    ),
    path(
        'programs/<int:pk>/',
        views.ProgramDetailAPIView.as_view(),
        name='api-program-detail',
    ),
    path(
        'students/',
        views.StudentListCreateAPIView.as_view(),
        name='api-student-list',
    ),
    path(
        'students/<int:pk>/',
        views.StudentDetailAPIView.as_view(),
        name='api-student-detail',
    ),
]
