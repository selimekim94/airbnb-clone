from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (Room, RoomType, Amenity, Facility, HouseRule, Photo)


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """
    list_display = ('name', 'used_by')

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'country', 'city', 'address', 'price', 'room_type')
        }),
        ('Times', {
            'fields': ('check_in', 'check_out', 'instant_book')
        }),
        ('Spaces', {
            'fields': ('guests', 'beds', 'bedrooms', 'baths')
        }),
        ('More about the spaces', {
            # 'classes': ('collapse',),
            'fields': ('amenities', 'facilities', 'house_rules')
        }),
        ('Last Details', {
            'fields': ('host',)
        }),
    )

    inlines = (PhotoInline,)

    list_display = (
        'name',
        'country',
        'city',
        'price',
        'guests',
        'beds',
        'bedrooms',
        'baths',
        'check_in',
        'check_out',
        'instant_book',
        'count_amenities',
        'total_ratings'
    )

    list_filter = (
        'instant_book',
        'host__super_host',
        'room_type',
        'amenities',
        'facilities',
        'house_rules',
        'city',
        'country'
    )

    raw_id_fields = ('host',)

    search_fields = ('=city', '^host__username')

    filter_horizontal = ('amenities', 'facilities', 'house_rules')  # many to many relationship

    def count_amenities(self, obj):
        return obj.amenities.count()


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """
    list_display = ('__str__', 'get_thumbnail')

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}">')

    get_thumbnail.short_description = 'Thumbnail'
