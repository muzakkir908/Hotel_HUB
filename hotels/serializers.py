from rest_framework import serializers
from .models import Hotel, Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'description', 'price_per_night', 
                 'capacity', 'available', 'image']

class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'price_per_night', 'image']

class HotelDetailSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'description', 'price_per_night', 
                 'latitude', 'longitude', 'image', 'created_at', 'rooms']

