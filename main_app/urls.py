from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('trips/', views.user_trips, name='index'),
    path('trips/create/', views.TripCreate.as_view(), name='trip_create'),
    path('trips/<int:pk>/', views.TripDetail.as_view(), name='trip_detail'),
    path('trips/<int:pk>/update/', views.TripUpdate.as_view(), name='trip_update'),
    path('trips/<int:pk>/delete/', views.TripDelete.as_view(), name='trip_delete'),
    path('trips/<int:pk>/transaction/create', views.TransactionCreate.as_view(), name='transaction_create'),
    path('trips/<int:pk>/member/create', views.MemberCreate.as_view(), name='member_create')
]