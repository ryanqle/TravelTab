from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('trips/', views.user_trips, name='index'),
    path('trips/create/', views.TripCreate.as_view(), name='trips_create')
]