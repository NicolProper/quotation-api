from django.contrib import admin
from django.urls import include, path, register_converter



urlpatterns = [
    path('admin/', admin.site.urls),
    path('departamentos/', include('departments.urls')),
    path('proyectos/', include('proyects.urls')),
    path('usuarios/', include('informacion.urls')),
    path('cotizacion/', include('cotizaciones.urls')),
    path('financiamiento/', include('financiamiento.urls')),
    path('proyectos-workshop/', include('project_workshop.urls')),
    path('departamentos-workshop/', include('department_workshop.urls')),
    path('configuraciones/', include('variables.urls')),

]