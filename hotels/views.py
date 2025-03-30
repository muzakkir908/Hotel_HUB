from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room
from bookings.models import Review
from django.db.models import Avg

def home(request):
    """Home page with featured hotels"""
    print("HOME VIEW CALLED")
    featured_hotels = Hotel.objects.all()[:6]
    return render(request, 'home.html', {
        'featured_hotels': featured_hotels
    })

def hotel_list(request):
    """List all hotels with optional location search"""
    hotels = Hotel.objects.all()
    location = request.GET.get('location', '')
    
    if location:
        hotels = hotels.filter(address__icontains=location)
        
    return render(request, 'hotels/list.html', {
        'hotels': hotels,
        'location_search': location
    })

def hotel_detail(request, hotel_id):
    """Show details for a specific hotel"""
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel, available=True)
    
    # Get reviews for this hotel from our database
    reviews = Review.objects.filter(hotel_id=hotel_id)
    
    # Handle sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'newest':
        reviews = reviews.order_by('-created_at')
    elif sort == 'highest':
        reviews = reviews.order_by('-rating')
    elif sort == 'lowest':
        reviews = reviews.order_by('rating')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, 'hotels/detail.html', {
        'hotel': hotel,
        'rooms': rooms,
        'reviews': reviews,
        'avg_rating': avg_rating
    })