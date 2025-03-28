from django.contrib import admin
from .models import Hotel, Room

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    fields = ('name', 'room_type', 'price_per_night', 'capacity', 'available')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'price_per_night', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'address')
    ordering = ('-created_at',)
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'room_type', 'price_per_night', 'capacity', 'available')
    list_filter = ('room_type', 'available', 'hotel')
    search_fields = ('name', 'hotel__name')
    list_editable = ('available', 'price_per_night')