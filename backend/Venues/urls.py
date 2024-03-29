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
    path('get_saved_places/', views.get_saved_places, name='get_saved_places'),
    path('get_best_places/', views.get_best_places, name='get_best_places'),
    path('create_event/', views.create_event, name='create_event'),
    path('get_event/', views.get_all_events, name='get_event'),
    path('done_place/', views.done_place, name='done_event'),
    path('get_done_place/', views.get_done_place, name='get_done_event'),
    # path('code/', views.execute_code,name='code'),
]
