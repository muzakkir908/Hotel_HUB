import uuid
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from .models import Booking, Review
from .serializers import BookingSerializer, ReviewSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """API endpoint for managing bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        """
        Generates a PDF confirmation for a booking using external PDF generator API
        """
        booking = self.get_object()
        
        # Prepare data for PDF generator API
        pdf_data = {
            "dynamicData": {
                "heading": "Booking Confirmation",
                "sections": ["Details", "Summary"],
                "Details": {
                    "Booking ID": booking.id,
                    "Hotel": booking.hotel.name,
                    "Room": f"{booking.room.name} ({booking.room.get_room_type_display()})",
                    "Check-In": booking.check_in.strftime("%Y-%m-%d"),
                    "Check-Out": booking.check_out.strftime("%Y-%m-%d"),
                    "Guests": booking.guests,
                    "Total Price": f"${booking.total_price}",
                    "Status": booking.get_status_display()
                },
                "Summary": {
                    "Transaction ID": f"TXN{booking.id}",
                    "Payment Method": "Credit Card",
                    "Booking Source": "Website",
                    "Additional Notes": "Thank you for your reservation!"
                }
            },
            # If email is provided, it will be sent to that address
            "email": request.data.get('email', '')
        }
        
        try:
            # Call the PDF Generator API
            pdf_api_url = "https://r9jwjvpgca.execute-api.us-east-1.amazonaws.com/dev/api/utils/pdf/generatePdf"
            response = requests.post(
                pdf_api_url,
                json=pdf_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                pdf_result = response.json()
                
                # Update booking with PDF data
                booking.invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
                booking.pdf_generated = True
                booking.save()
                
                return Response({
                    'success': True,
                    'message': 'PDF generated successfully',
                    'booking_id': booking.id,
                    'invoice_id': booking.invoice_id,
                    'pdf_data': pdf_result.get('data', {})
                })
            else:
                return Response({
                    'success': False,
                    'message': f'Error from PDF service: {response.text}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating PDF: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewViewSet(viewsets.ModelViewSet):
    """API endpoint for managing reviews"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['get'])
    def hotel_reviews(self, request):
        """Get reviews for a specific hotel"""
        hotel_id = request.query_params.get('hotel_id')
        if not hotel_id:
            return Response({"error": "hotel_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        reviews = Review.objects.filter(hotel_id=hotel_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
