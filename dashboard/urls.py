from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bookings-by-day/', views.bookings_by_day, name='bookings_by_day'),
    path('service-performance/', views.service_performance, name='service_performance'),
    path('most-booked-routes/', views.most_booked_routes, name='most_booked_routes'),
    path('advance-booking-cities/', views.advance_booking_cities, name='advance_booking_cities'),
    path('correlation-analysis/', views.correlation_analysis, name='correlation_analysis'),
    path('device-usage/', views.device_usage, name='device_usage'),
    path('quarterly-trends/', views.quarterly_trends, name='quarterly_trends'),
    path('booking-search-ratio/', views.booking_search_ratio, name='booking_search_ratio'),
]