"""
URL configuration for the API app.
"""

from django.urls import path
from .api import api

urlpatterns = [
    path('', api.urls),
]
