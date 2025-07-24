from django.urls import path
from . import views

urlpatterns = [
    path('', views.TravelGuidanceView.as_view(), name='travel-guidance'),
]

