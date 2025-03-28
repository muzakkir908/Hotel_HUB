from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Hotel, Room
from .serializers import HotelListSerializer, HotelDetailSerializer, RoomSerializer

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing hotels"""
    queryset = Hotel.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HotelDetailSerializer
        return HotelListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured hotels (first 6)"""
        hotels = self.get_queryset()[:6]  
        serializer = HotelListSerializer(hotels, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def rooms(self, request, pk=None):
        """Get all rooms for a specific hotel"""
        hotel = self.get_object()
        rooms = Room.objects.filter(hotel=hotel, available=True)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
        
class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing rooms"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        queryset = Room.objects.filter(available=True)
        hotel_id = self.request.query_params.get('hotel', None)
        
        if hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)
                
        return queryset
