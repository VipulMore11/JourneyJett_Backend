from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'Reviews'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('reviews/', views.review_view, name='review'),
    path('get_reviews/', views.get_reviews, name='get_reviews'),
    # path('chat/', views.chat_with_ai_api, name='chat'),

]
