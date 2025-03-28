"""
URL configuration for hotel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from hotels.views import home, hotel_list, hotel_detail
from hotels.api_views import HotelViewSet, RoomViewSet
from bookings.views import booking_list, create_booking, booking_confirmation, generate_booking_pdf, submit_review
from bookings.api_views import BookingViewSet, ReviewViewSet
from hotel_project.health_check import health_check

# Create a router for REST API endpoints
router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('health/', health_check, name='health_check'),  # Health check endpoint
    path('hotels/', hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/', hotel_detail, name='hotel_detail'),
    path('submit-review/<int:hotel_id>/', submit_review, name='submit_review'),
    path('bookings/', booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('bookings/<int:booking_id>/pdf/', generate_booking_pdf, name='generate_booking_pdf'),
    path('book-hotel/<int:hotel_id>/', create_booking, name='create_booking'),
    path('book-hotel/<int:hotel_id>/room/<int:room_id>/', create_booking, name='create_booking_with_room'),
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/hotels/featured/', HotelViewSet.as_view({'get': 'featured'}), name='api-featured-hotels'),
    path('api/hotels/<int:pk>/rooms/', HotelViewSet.as_view({'get': 'rooms'}), name='api-hotel-rooms'),
    path('api/reviews/hotel/', ReviewViewSet.as_view({'get': 'hotel_reviews'}), name='api-hotel-reviews'),
    
    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)