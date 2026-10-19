import datetime
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from .models import (
    TempleInformation, TempleTiming, Event, Announcement,
    GalleryImage, DonationInformation, ContactMessage
)
from .forms import ContactForm


class ModelTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_temple_information_singleton_and_cache(self):
        """Verify TempleInformation maintains a single record and invalidates cache on save."""
        t1 = TempleInformation.objects.create(
            name="Original Math",
            address="Original Address"
        )
        self.assertEqual(TempleInformation.objects.count(), 1)

        # Set cache
        cache.set('global_temple_info', t1, 3600)

        # Save a new instance - should update the existing record
        t2 = TempleInformation.objects.create(
            name="Updated Math",
            address="Updated Address"
        )
        self.assertEqual(TempleInformation.objects.count(), 1)
        self.assertEqual(TempleInformation.objects.first().name, "Updated Math")
        # Cache must be invalidated
        self.assertIsNone(cache.get('global_temple_info'))

    def test_event_unicode_slug_and_collision(self):
        """Verify event slug generation preserves Unicode (Hindi) and resolves collisions."""
        # Non-ASCII Hindi title
        event1 = Event.objects.create(
            title="श्री जगन्नाथ रथ यात्रा",
            description="Grand annual festival",
            date=timezone.now().date() + datetime.timedelta(days=10),
        )
        self.assertTrue(bool(event1.slug))
        # Ensure it preserved unicode content rather than falling back to 'event'
        self.assertFalse(event1.slug.startswith('event'))

        # Duplicate title should generate incremented slug
        event2 = Event.objects.create(
            title="श्री जगन्नाथ रथ यात्रा",
            description="Second procession",
            date=timezone.now().date() + datetime.timedelta(days=20),
        )
        self.assertTrue(event2.slug.endswith("-1"))
        self.assertNotEqual(event1.slug, event2.slug)

    def test_donation_information_singleton(self):
        """Verify DonationInformation only keeps one row."""
        d1 = DonationInformation.objects.create(
            account_holder_name="Trust 1",
            bank_name="Bank A"
        )
        self.assertEqual(DonationInformation.objects.count(), 1)

        d2 = DonationInformation.objects.create(
            account_holder_name="Trust 2",
            bank_name="Bank B"
        )
        self.assertEqual(DonationInformation.objects.count(), 1)
        self.assertEqual(DonationInformation.objects.first().account_holder_name, "Trust 2")


class FormTests(TestCase):
    def test_contact_form_valid_data(self):
        """Test standard valid contact form input."""
        data = {
            'name': 'Ramesh Kumar',
            'email': 'ramesh@example.com',
            'phone': '9876543210',
            'message': 'Jai Jagannath. Please share details regarding the upcoming aarti.',
            'website': '',  # Honeypot empty
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_contact_form_phone_formats(self):
        """Test contact form handles standard international phone formatting."""
        valid_phones = [
            '+91 98765 43210',
            '+91 (123) 456-7890',
            '123-456-7890',
            '+1.555.123.4567',
        ]
        for phone in valid_phones:
            data = {
                'name': 'Devotee',
                'email': 'devotee@example.com',
                'phone': phone,
                'message': 'Test phone formatting.',
                'website': '',
            }
            form = ContactForm(data=data)
            self.assertTrue(form.is_valid(), f"Phone '{phone}' should be valid, but got: {form.errors}")

    def test_contact_form_phone_too_short_or_long(self):
        """Test rejection of invalid phone numbers."""
        invalid_phones = [
            '12345',  # Too short (<10 digits)
            '+91 123456789012345678901',  # Exceeds 20 chars
            'abc-def-ghij',  # No digits
        ]
        for phone in invalid_phones:
            data = {
                'name': 'Devotee',
                'email': 'devotee@example.com',
                'phone': phone,
                'message': 'Test invalid phone.',
                'website': '',
            }
            form = ContactForm(data=data)
            self.assertFalse(form.is_valid(), f"Phone '{phone}' should be rejected as invalid.")

    def test_contact_form_honeypot_blocking(self):
        """Test that automated bot filling the honeypot field is rejected."""
        data = {
            'name': 'Spam Bot',
            'email': 'bot@spammer.com',
            'phone': '9876543210',
            'message': 'Visit my pharmacy website.',
            'website': 'https://spam-link.com',  # Honeypot filled by bot
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)
        self.assertEqual(form.errors['website'][0], 'Bot detected.')

    def test_contact_form_message_too_long(self):
        """Test rejection of overly long contact form messages (>5000 chars)."""
        data = {
            'name': 'Devotee',
            'email': 'devotee@example.com',
            'phone': '9876543210',
            'message': 'A' * 5001,
            'website': '',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
        self.assertIn('5000', form.errors['message'][0])


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()
        self.temple = TempleInformation.objects.create(
            name="Sri Jagannath Math",
            address="Tetri-Dandari, Begusarai, Bihar",
            phone="+91-99999-99999",
            email="info@jagannathmath.org",
        )
        self.timing = TempleTiming.objects.create(
            activity_name="Mangala Aarti",
            time="5:30 AM",
            display_order=1,
            is_active=True,
        )
        self.event = Event.objects.create(
            title="Upcoming Yatra",
            description="Holy yatra festival",
            date=timezone.now().date() + datetime.timedelta(days=15),
            is_active=True,
        )
        self.announcement = Announcement.objects.create(
            title="Temple Notice",
            content="Temple premises sanitized daily.",
            is_active=True,
        )

    def test_health_check_endpoint(self):
        """Verify the health check endpoint returns 200 and json status ok."""
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'ok')
        self.assertEqual(data.get('database'), 'connected')

    def test_all_public_get_views(self):
        """Verify all public informational views return HTTP 200."""
        routes = [
            'home', 'about', 'timings', 'events',
            'announcements', 'gallery', 'donate', 'contact'
        ]
        for route in routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200, f"Route '{route}' failed with status {response.status_code}")

    def test_event_detail_view(self):
        """Verify event detail retrieves the event and 404s on missing slug."""
        response = self.client.get(reverse('event_detail', kwargs={'slug': self.event.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)

        # Missing slug should return 404
        response_404 = self.client.get(reverse('event_detail', kwargs={'slug': 'non-existent-slug'}))
        self.assertEqual(response_404.status_code, 404)

    def test_contact_post_success(self):
        """Verify successful contact submission redirects and saves message."""
        payload = {
            'name': 'Ananya Roy',
            'email': 'ananya@example.com',
            'phone': '9876543210',
            'message': 'Seeking blessings for upcoming exams.',
            'website': '',
        }
        response = self.client.post(reverse('contact'), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contact'))
        self.assertTrue(ContactMessage.objects.filter(email='ananya@example.com').exists())

    def test_contact_rate_limiting(self):
        """Verify excessive contact POST submissions trigger rate limit warning."""
        payload = {
            'name': 'Devotee',
            'email': 'devotee@example.com',
            'phone': '9876543210',
            'message': 'Message payload.',
            'website': '',
        }
        # First 5 submissions succeed
        for _ in range(5):
            self.client.post(reverse('contact'), data=payload)

        # 6th submission triggers rate limiting
        response = self.client.post(reverse('contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Too many messages sent')

    def test_custom_404_view(self):
        """Verify requesting a non-existent URL returns 404 status and custom template."""
        response = self.client.get('/non-existent-page-url-xyz/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Page Not Found', status_code=404)

    @patch('core.views.connection.cursor')
    def test_health_check_database_failure(self, mock_cursor):
        """Verify health check returns 503 without exposing exception details when DB fails."""
        mock_cursor.side_effect = Exception("Simulated DB connection failure")
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertEqual(data.get('status'), 'unhealthy')
        self.assertEqual(data.get('database'), 'unavailable')
        # Ensure internal exception details are NOT leaked in response
        self.assertNotIn("Simulated DB connection failure", response.content.decode())
