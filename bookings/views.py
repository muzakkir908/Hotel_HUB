import base64
import uuid
import requests
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from .models import Booking, Review
from hotels.models import Hotel, Room
from .review_api import ReviewAPI


@login_required
def booking_list(request):
    """Show user's bookings"""
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/list.html', {'bookings': bookings})

@login_required
def create_booking(request, hotel_id, room_id=None):
    """Create a new booking"""
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = get_object_or_404(Room, id=room_id) if room_id else None
    
    if request.method == 'POST':
        # Process the booking form
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests = int(request.POST.get('guests', 1))
        
        # Calculate total price
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        nights = (check_out_date - check_in_date).days
        
        price_per_night = room.price_per_night if room else hotel.price_per_night
        total_price = price_per_night * nights
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            hotel=hotel,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            guests=guests,
            total_price=total_price,
            status='confirmed'
        )
        
        messages.success(request, 'Your booking has been confirmed!')
        return redirect('booking_confirmation', booking_id=booking.id)
    
    return render(request, 'bookings/form.html', {
        'hotel': hotel,
        'room': room
    })

@login_required
def booking_confirmation(request, booking_id):
    """Show booking confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    return render(request, 'bookings/confirmation.html', {
        'booking': booking
    })

@login_required
def generate_booking_pdf(request, booking_id):
    """Generate PDF for booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if it's an email request with custom email dialog
    if request.method == 'POST' and 'email' in request.POST:
        email_address = request.POST.get('email_address', request.user.email)
        
        # Prepare data for PDF Generator API
        pdf_data = {
            "dynamicData": {
                "heading": "Booking Confirmation",
                "sections": ["Details", "Summary"],
                "Details": {
                    "Booking ID": booking.id,
                    "Hotel": booking.hotel.name,
                    "Room": f"{booking.room.name} ({booking.room.get_room_type_display()})" if booking.room else "Standard Room",
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
            "email": email_address
        }
        
        try:
            # Call the PDF Generator API
            response = requests.post(
                "https://r9jwjvpgca.execute-api.us-east-1.amazonaws.com/dev/api/utils/pdf/generatePdf",
                json=pdf_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Update booking with invoice ID if not already set
                if not booking.invoice_id:
                    booking.invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
                    booking.pdf_generated = True
                    booking.save()
                
                messages.success(request, f'PDF has been sent to {email_address}')
            else:
                messages.error(request, f'Error generating PDF: {response.text}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            
        return redirect('booking_confirmation', booking_id=booking.id)
            
    # Standard GET method handling for direct download or showing email form
    elif request.method == 'GET':
        if request.GET.get('download') == 'true':
            # Handle direct download
            pdf_data = {
                "dynamicData": {
                    "heading": "Booking Confirmation",
                    "sections": ["Details", "Summary"],
                    "Details": {
                        "Booking ID": booking.id,
                        "Hotel": booking.hotel.name,
                        "Room": f"{booking.room.name} ({booking.room.get_room_type_display()})" if booking.room else "Standard Room",
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
                }
            }
            
            try:
                # Call the PDF Generator API
                response = requests.post(
                    "https://r9jwjvpgca.execute-api.us-east-1.amazonaws.com/dev/api/utils/pdf/generatePdf",
                    json=pdf_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Update booking with invoice ID
                    if not booking.invoice_id:
                        booking.invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
                        booking.pdf_generated = True
                        booking.save()
                    
                    # Decode base64 PDF data
                    pdf_file = result.get('data', {}).get('file')
                    if pdf_file:
                        pdf_bytes = base64.b64decode(pdf_file)
                        
                        # Create response with PDF content
                        response = HttpResponse(pdf_bytes, content_type='application/pdf')
                        response['Content-Disposition'] = f'attachment; filename="booking_{booking_id}.pdf"'
                        return response
                else:
                    messages.error(request, f'Error generating PDF: {response.text}')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                
            return redirect('booking_confirmation', booking_id=booking.id)
            
        elif request.GET.get('email') == 'true':
            # Show email form instead of sending directly
            return render(request, 'bookings/email_pdf_form.html', {
                'booking': booking,
                'default_email': request.user.email
            })
    
    # Default fallback
    return redirect('booking_confirmation', booking_id=booking.id)

def submit_review(request, hotel_id):
    """Handle review submission"""
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to submit a review.')
        return redirect('hotel_detail', hotel_id=hotel_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if not rating or not comment:
            messages.error(request, 'Both rating and comment are required.')
            return redirect('hotel_detail', hotel_id=hotel_id)
        
        # Check if user already has a review for this hotel
        existing_review = Review.objects.filter(hotel_id=hotel_id, user=request.user).first()
        
        if existing_review:
            # Update existing review
            existing_review.rating = int(rating)
            existing_review.comment = comment
            existing_review.sentiment = existing_review.get_sentiment()
            existing_review.save()
            messages.success(request, 'Your review has been updated successfully!')
        else:
            # Create new review with basic sentiment
            new_review = Review(
                hotel_id=hotel_id,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            new_review.sentiment = new_review.get_sentiment()
            new_review.save()
            messages.success(request, 'Your review has been submitted successfully!')
        
    return redirect('hotel_detail', hotel_id=hotel_id)