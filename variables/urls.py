

from django.urls import path
from . import views


urlpatterns = [
    path('create_variable/', views.create_variable, name='create_variable'),
]
