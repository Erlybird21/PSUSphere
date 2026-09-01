from django.contrib import admin
from django.urls import path, include
from studentorg import views
from studentorg.views import HomePageView, OrganizationList

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', views.HomePageView.as_view(), name='home'),
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', views.OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<int:pk>', views.OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<int:pk>/delete', views.OrganizationDeleteView.as_view(), name='organization-delete'),
    path('orgmember_list', views.OrgMemberList.as_view(), name='orgmember-list'),
    path('orgmember_list/add', views.OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember_list/<int:pk>', views.OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember_list/<int:pk>/delete', views.OrgMemberDeleteView.as_view(), name='orgmember-delete'),
    path('student_list', views.StudentList.as_view(), name='student-list'),
    path('student_list/add', views.StudentCreateView.as_view(), name='student-add'),
    path('student_list/<int:pk>', views.StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<int:pk>/delete', views.StudentDeleteView.as_view(), name='student-delete'),
    path('college_list', views.CollegeList.as_view(), name='college-list'),
    path('college_list/add', views.CollegeCreateView.as_view(), name='college-add'),
    path('college_list/<int:pk>', views.CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/<int:pk>/delete', views.CollegeDeleteView.as_view(), name='college-delete'),
    path('program_list', views.ProgramList.as_view(), name='program-list'),
    path('program_list/add', views.ProgramCreateView.as_view(), name='program-add'),
    path('program_list/<int:pk>', views.ProgramUpdateView.as_view(), name='program-update'),
    path('program_list/<int:pk>/delete', views.ProgramDeleteView.as_view(), name='program-delete'),
]
