from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'Authentication'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/',views.profile_view,name='user_profile'),
    path('update_profile/', views.update_profile_view,name='update_user_profile'),
]
