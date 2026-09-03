from django.contrib import admin
from django.utils.html import format_html
from .models import (
    TempleInformation, TempleTiming, Event, Announcement,
    GalleryImage, DonationInformation, ContactMessage
)

admin.site.site_header = 'Sri Jagannath Math Administration'
admin.site.site_title = 'Sri Jagannath Math Admin'
admin.site.index_title = 'Manage Website Content'


@admin.register(TempleInformation)
class TempleInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    
    def has_add_permission(self, request):
        # Only allow one record
        if TempleInformation.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TempleTiming)
class TempleTimingAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'time', 'display_order', 'is_active')
    list_editable = ('time', 'display_order', 'is_active')
    ordering = ('display_order',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'is_active', 'image_preview')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-date',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;max-width:80px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_active')
    list_filter = ('is_active', 'published_date')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'uploaded_at')
    search_fields = ('title', 'description')
    ordering = ('-uploaded_at',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;max-width:80px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(DonationInformation)
class DonationInformationAdmin(admin.ModelAdmin):
    list_display = ('account_holder_name', 'bank_name', 'upi_id', 'qr_preview')
    
    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" style="max-height:60px;" />', obj.qr_code.url)
        return '-'
    qr_preview.short_description = 'QR Code'
    
    def has_add_permission(self, request):
        if DonationInformation.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        # Allow viewing but fields are readonly
        return True
