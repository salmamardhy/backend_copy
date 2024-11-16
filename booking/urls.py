# booking/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('event/<str:event_id>/', views.event, name='booking_event'),
    path('booking/<str:event_id>/', views.booking_without_referral, name='booking_index'),
    path('booking/<str:event_id>/<str:referral_id>/', views.booking_with_referral, name='booking_with_referral'),
    # path('update_booking_status/', views.update_booking_status, name='update_booking_status'),
]
