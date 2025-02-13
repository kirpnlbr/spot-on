"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from api import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/initialize/<str:lot_name>/', views.initialize_parking_lot, name='initialize_parking_lot'),
    path('api/park/', views.park_vehicle, name='park_vehicle'),  # lot_name in POST data
    path('api/remove/', views.remove_vehicle, name='remove_vehicle'),  # lot_name in POST data
    path('api/status/<str:lot_name>/', views.get_status, name='get_status'),
    path("api/parking_grid/<str:lot_name>/", views.get_parking_grid, name="get_parking_grid"),
    path('api/parking_lots/', views.get_parking_lots, name='get_parking_lots'),
    path('api/simulation/start/<str:lot_name>/', views.start_simulation, name='start_simulation'),
    path('api/simulation/status/<str:lot_name>/', views.is_simulation_running_view, name='is_simulation_running'),
    path('api/simulation/stop/<str:lot_name>/', views.stop_simulation, name='stop_simulation'),
    
]
