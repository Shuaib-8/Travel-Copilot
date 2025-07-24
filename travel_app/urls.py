from django.urls import path
from . import views

urlpatterns = [
    path('', views.travel_guidance_view, name='travel-guidance'),
]

