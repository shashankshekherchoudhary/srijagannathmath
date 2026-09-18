from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone

class TempleInformation(models.Model):
    name = models.CharField(max_length=200, default='Sri Jagannath Math')
    address = models.TextField(default='Tetri-Dandari, Begusarai, Bihar, India')
    about_text = models.TextField(blank=True, help_text='Short introduction about the Math')
    history = models.TextField(blank=True, help_text='Detailed history of the Math')
    mission = models.TextField(blank=True, help_text='Mission and values')
    spiritual_significance = models.TextField(blank=True, help_text='Spiritual significance of the Math')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    map_embed_url = models.TextField(blank=True, help_text='Google Maps embed URL (iframe src)')
    
    class Meta:
        verbose_name = 'Temple Information'
        verbose_name_plural = 'Temple Information'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Singleton pattern - only allow one record
        if not self.pk and TempleInformation.objects.exists():
            existing = TempleInformation.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.map_embed_url:
            url = self.map_embed_url.strip()
            allowed_prefixes = (
                'https://www.google.com/maps/embed',
                'https://maps.google.com/maps',
                'https://www.google.co.in/maps',
            )
            if not url.startswith(allowed_prefixes):
                raise ValidationError({
                    'map_embed_url': 'Only Google Maps embed URLs are allowed for security.'
                })


class TempleTiming(models.Model):
    activity_name = models.CharField(max_length=100)
    time = models.CharField(max_length=100, help_text='e.g., 5:00 AM - 6:00 AM')
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    class Meta:
        ordering = ['display_order']
        verbose_name = 'Temple Timing'
        verbose_name_plural = 'Temple Timings'
    
    def __str__(self):
        return f'{self.activity_name} - {self.time}'


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    date = models.DateField(db_index=True)
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, default='Sri Jagannath Math')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = 'event'
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField(default=timezone.now, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
    
    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        return self.title


class DonationInformation(models.Model):
    account_holder_name = models.CharField(max_length=200, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True, verbose_name='IFSC Code')
    branch_name = models.CharField(max_length=200, blank=True)
    upi_id = models.CharField(max_length=100, blank=True, verbose_name='UPI ID')
    qr_code = models.ImageField(upload_to='donation/', blank=True, null=True, verbose_name='QR Code')
    
    class Meta:
        verbose_name = 'Donation Information'
        verbose_name_plural = 'Donation Information'
    
    def __str__(self):
        return 'Donation Information'
    
    def save(self, *args, **kwargs):
        if not self.pk and DonationInformation.objects.exists():
            existing = DonationInformation.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f'{self.name} - {self.created_at.strftime("%d %b %Y")}'
