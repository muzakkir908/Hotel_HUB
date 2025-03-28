from django.contrib import admin
from .models import Booking, Review

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'check_in', 'check_out', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'check_in', 'check_out', 'created_at')
    search_fields = ('user__username', 'hotel__name', 'invoice_id')
    list_editable = ('status',)
    readonly_fields = ('invoice_id', 'pdf_generated', 'created_at', 'updated_at')
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'hotel', 'room', 'check_in', 'check_out', 'guests', 'total_price', 'status')
        }),
        ('Additional Information', {
            'fields': ('invoice_id', 'pdf_generated', 'created_at', 'updated_at')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel_id', 'rating', 'sentiment', 'created_at')
    list_filter = ('rating', 'sentiment', 'created_at')
    search_fields = ('user__username', 'comment')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'hotel_id', 'rating', 'comment', 'sentiment')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )