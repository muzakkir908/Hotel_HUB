from rest_framework import serializers
from .models import Booking, Review
from hotels.serializers import HotelListSerializer, RoomSerializer

class BookingSerializer(serializers.ModelSerializer):
    hotel_details = HotelListSerializer(source='hotel', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'hotel', 'hotel_details', 'room', 'room_details', 
                  'check_in', 'check_out', 'guests', 'total_price', 
                  'status', 'invoice_id', 'pdf_generated', 'created_at']
        read_only_fields = ['invoice_id', 'pdf_generated', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'hotel_id', 'rating', 'comment', 
                 'sentiment', 'created_at', 'verified']
        read_only_fields = ['user_name', 'sentiment', 'created_at', 'verified']
