from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('timings/', views.timings_view, name='timings'),
    path('events/', views.events_view, name='events'),
    path('events/<slug:slug>/', views.event_detail_view, name='event_detail'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('donate/', views.donate_view, name='donate'),
    path('contact/', views.contact_view, name='contact'),
    path('health/', views.health_check_view, name='health_check'),
]
