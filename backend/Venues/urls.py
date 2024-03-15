from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'Venues'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('places/', views.places_view,name='places'),
    path('get_places/', views.get_places_view,name='get_places'), 
    path('get_destinations/',views.get_destination_view,name='get_destinations'),
    path('recommendations/', views.personalize_recommendations,name='recommendations'),
    path('saved_places/', views.saved_places,name='saved_places'),
    # path('code/', views.execute_code,name='code'),
]
