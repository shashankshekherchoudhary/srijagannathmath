import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import JsonResponse
from django.db import connection
from django.utils import timezone
from .models import (
    TempleInformation, TempleTiming, Event, Announcement,
    GalleryImage, DonationInformation
)
from .forms import ContactForm

logger = logging.getLogger('core')


def get_temple_info():
    """Helper to get temple information singleton with cache."""
    info = cache.get('global_temple_info')
    if info is None:
        info = TempleInformation.objects.first()
        cache.set('global_temple_info', info, 86400)
    return info


def health_check_view(request):
    """Liveness and readiness probe for container orchestrators and monitoring."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "connected"
    except Exception as exc:
        logger.error(f"Health check database failure: {exc}")
        return JsonResponse(
            {"status": "unhealthy", "database": "unavailable"}, status=503
        )

    return JsonResponse({
        "status": "ok",
        "database": db_status,
        "timestamp": timezone.now().isoformat(),
    })


def home_view(request):
    temple_info = get_temple_info()
    timings = TempleTiming.objects.filter(is_active=True)[:6]
    upcoming_events = Event.objects.filter(
        is_active=True, date__gte=timezone.now().date()
    ).order_by('date')[:3]
    # Sliced to match home template UI grid layouts (3 announcements, 4 gallery items)
    announcements = Announcement.objects.filter(is_active=True)[:3]
    gallery_images = GalleryImage.objects.all()[:4]

    context = {
        'temple_info': temple_info,
        'timings': timings,
        'upcoming_events': upcoming_events,
        'announcements': announcements,
        'gallery_images': gallery_images,
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    temple_info = get_temple_info()
    context = {'temple_info': temple_info}
    return render(request, 'core/about.html', context)


def timings_view(request):
    timings = TempleTiming.objects.filter(is_active=True)
    temple_info = get_temple_info()
    context = {
        'timings': timings,
        'temple_info': temple_info,
    }
    return render(request, 'core/timings.html', context)


def events_view(request):
    today = timezone.now().date()
    upcoming_events_qs = Event.objects.filter(
        is_active=True, date__gte=today
    ).order_by('date')
    past_events_qs = Event.objects.filter(
        is_active=True, date__lt=today
    ).order_by('-date')

    # Paginate upcoming events
    upcoming_paginator = Paginator(upcoming_events_qs, 9)
    upcoming_page = request.GET.get('upcoming_page')
    upcoming_events = upcoming_paginator.get_page(upcoming_page)

    # Paginate past events
    past_paginator = Paginator(past_events_qs, 9)
    past_page = request.GET.get('past_page')
    past_events = past_paginator.get_page(past_page)

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'core/events.html', context)


def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    context = {'event': event}
    return render(request, 'core/event_detail.html', context)


def announcements_view(request):
    announcements_qs = Announcement.objects.filter(is_active=True)
    paginator = Paginator(announcements_qs, 10)
    page = request.GET.get('page')
    announcements = paginator.get_page(page)
    context = {'announcements': announcements}
    return render(request, 'core/announcements.html', context)


def gallery_view(request):
    images_qs = GalleryImage.objects.all()
    paginator = Paginator(images_qs, 12)
    page = request.GET.get('page')
    images = paginator.get_page(page)
    context = {'images': images}
    return render(request, 'core/gallery.html', context)


def donate_view(request):
    donation_info = cache.get('global_donation_info')
    if donation_info is None:
        donation_info = DonationInformation.objects.first()
        cache.set('global_donation_info', donation_info, 86400)
    context = {'donation_info': donation_info}
    return render(request, 'core/donate.html', context)


def contact_view(request):
    temple_info = get_temple_info()

    if request.method == 'POST':
        # Simple IP-based rate limiting via cache (max 5 submissions per 5 minutes)
        ip_addr = request.META.get('REMOTE_ADDR', '127.0.0.1')
        rate_key = f'contact_rate_{ip_addr}'
        submission_count = cache.get(rate_key, 0)
        if submission_count >= 5:
            logger.warning(f"Contact form rate limit reached for IP: {ip_addr}")
            messages.error(request, 'Too many messages sent. Please wait a few minutes before trying again.')
            return render(request, 'core/contact.html', {'form': ContactForm(request.POST), 'temple_info': temple_info})

        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            cache.set(rate_key, submission_count + 1, 300)
            logger.info(f"New contact message received from {contact_msg.email} (ID: {contact_msg.pk})")
            messages.success(request, 'Thank you for your message! We will get back to you soon. 🙏')
            return redirect('contact')
        else:
            logger.info("Contact form submission failed validation.")
    else:
        form = ContactForm()

    context = {
        'form': form,
        'temple_info': temple_info,
    }
    return render(request, 'core/contact.html', context)

