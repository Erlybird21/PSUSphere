from django.contrib import admin
from django.urls import path
from studentorg import views
from studentorg.views import HomePageView, OrganizationList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', views.OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<int:pk>', views.OrganizationUpdateView.as_view(), name='organization-update'),
]
