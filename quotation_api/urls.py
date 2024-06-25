"""quotation_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from departments import views as departamentos_views
from proyects import views as proyectos_views

from proyects.views import get_all_proyects_web

urlpatterns = [
    path('admin/', admin.site.urls),
    path('proyectos/upload_data/', proyectos_views.upload_data_excel, name="departamentos_upload"),
    path('proyectos/get_all_proyects_web/', get_all_proyects_web, name="get_all_proyects_web"),
    path('departamentos/upload_data/', departamentos_views.upload_data_excel, name="departamentos_upload"),
    path('departamentos/update_all_data/', departamentos_views.update_all_data, name="update_all_data"),
    path('departamentos/get_score_crediticio/', departamentos_views.get_score_crediticio, name='get_score_crediticio'),

    path('', include("departments.urls")),
    path('', include("proyects.urls")),
]
