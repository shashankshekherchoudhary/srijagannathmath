"""
Seed script to populate the database with placeholder data.
Run with: python3.13.exe manage.py shell < seed_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from core.models import (
    TempleInformation, TempleTiming, Event, Announcement,
    GalleryImage, DonationInformation
)

# ── Temple Information ──
temple, _ = TempleInformation.objects.get_or_create(
    pk=1,
    defaults={
        'name': 'Sri Jagannath Math',
        'address': 'Tetri-Dandari, Begusarai, Bihar, India',
        'about_text': (
            'Sri Jagannath Math is a revered spiritual institution located in '
            'Tetri-Dandari, Begusarai, Bihar. The Math serves as a centre for '
            'spiritual learning, devotion, and community service, dedicated to '
            'Lord Jagannath and the timeless values of Sanatan Dharma.'
        ),
        'history': (
            'Sri Jagannath Math has a rich spiritual heritage rooted in the '
            'traditions of Jagannath culture. Established with the vision of '
            'spreading the divine teachings of Lord Jagannath, the Math has '
            'been a beacon of devotion and community service in the Begusarai '
            'region of Bihar.\n\n'
            'The Math continues to uphold the sacred traditions of worship, '
            'learning, and service that have been passed down through '
            'generations. It stands as a testament to the enduring spiritual '
            'legacy of Jagannath culture in Eastern India.\n\n'
            '[This section can be updated with the actual historical details '
            'of the Math through the Admin panel.]'
        ),
        'spiritual_significance': (
            'Sri Jagannath Math holds deep spiritual significance as a place '
            'where devotees can connect with the divine presence of Lord '
            'Jagannath. The Math follows the sacred traditions of Jagannath '
            'worship and provides a serene environment for meditation, prayer, '
            'and spiritual growth.\n\n'
            'The daily rituals, aarti ceremonies, and festivals celebrated at '
            'the Math create an atmosphere of devotion and peace that draws '
            'seekers from across the region.\n\n'
            '[This section can be updated with specific spiritual details '
            'through the Admin panel.]'
        ),
        'mission': (
            'Our mission is to preserve and promote the sacred traditions of '
            'Jagannath culture, provide spiritual guidance to devotees, and '
            'serve the community through charitable activities.\n\n'
            '• Promote spiritual education and awareness\n'
            '• Conduct daily worship and sacred rituals\n'
            '• Organise festivals and cultural programmes\n'
            '• Serve the underprivileged through community outreach\n'
            '• Preserve the heritage and traditions of Sanatan Dharma\n\n'
            '[This section can be updated through the Admin panel.]'
        ),
        'phone': '+91-XXXXX-XXXXX',
        'email': 'info@jagannathmath.org',
        'map_embed_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d57456.89!2d86.12!3d25.41!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sBegusarai!5e0!3m2!1sen!2sin!4v1234567890',
    }
)
print(f"✅ Temple Information: {temple}")

# ── Temple Timings ──
timings_data = [
    ('Temple Opening', '5:00 AM', 1),
    ('Mangala Aarti', '5:30 AM - 6:00 AM', 2),
    ('Morning Darshan', '6:00 AM - 11:00 AM', 3),
    ('Bhog (Prasad)', '12:00 PM - 12:30 PM', 4),
    ('Afternoon Rest', '12:30 PM - 4:00 PM', 5),
    ('Evening Darshan', '4:00 PM - 7:00 PM', 6),
    ('Sandhya Aarti', '7:00 PM - 7:30 PM', 7),
    ('Shayan Aarti', '8:30 PM - 9:00 PM', 8),
    ('Temple Closing', '9:00 PM', 9),
]
for name, time, order in timings_data:
    TempleTiming.objects.get_or_create(
        activity_name=name,
        defaults={'time': time, 'display_order': order, 'is_active': True}
    )
print(f"✅ Temple Timings: {len(timings_data)} entries")

# ── Events ──
today = timezone.now().date()
events_data = [
    {
        'title': 'Rath Yatra Mahotsav',
        'description': (
            'The grand annual Rath Yatra celebration at Sri Jagannath Math. '
            'Join us for the sacred chariot procession of Lord Jagannath, '
            'Lord Balabhadra, and Devi Subhadra. The celebration includes '
            'kirtans, bhajans, prasad distribution, and cultural programmes.'
        ),
        'date': today + timedelta(days=30),
        'time': '7:00',
        'location': 'Sri Jagannath Math, Tetri-Dandari',
    },
    {
        'title': 'Janmashtami Celebrations',
        'description': (
            'Celebrate the divine birth of Lord Krishna with midnight aarti, '
            'bhajans, kirtan, and prasad distribution. Special decorations '
            'and cultural programmes throughout the day.'
        ),
        'date': today + timedelta(days=60),
        'time': '18:00',
        'location': 'Sri Jagannath Math, Tetri-Dandari',
    },
    {
        'title': 'Spiritual Discourse Series',
        'description': (
            'A series of spiritual discourses on the Bhagavad Gita by '
            'distinguished scholars and saints. Open to all devotees and '
            'seekers of spiritual knowledge.'
        ),
        'date': today + timedelta(days=15),
        'time': '10:00',
        'location': 'Sri Jagannath Math, Tetri-Dandari',
    },
    {
        'title': 'Community Seva Day',
        'description': (
            'Join us for a day of community service including food '
            'distribution, cleanliness drive, and health awareness camp '
            'organised by the Math.'
        ),
        'date': today + timedelta(days=7),
        'time': '8:00',
        'location': 'Tetri-Dandari, Begusarai',
    },
]
for e in events_data:
    Event.objects.get_or_create(
        title=e['title'],
        defaults={
            'description': e['description'],
            'date': e['date'],
            'time': e['time'],
            'location': e['location'],
            'is_active': True,
        }
    )
print(f"✅ Events: {len(events_data)} entries")

# ── Announcements ──
announcements_data = [
    {
        'title': 'Daily Aarti Timings Updated',
        'content': (
            'Dear devotees, please note that the daily aarti timings have '
            'been updated for the current season. Kindly check the Timings '
            'page for the latest schedule. Jai Jagannath! 🙏'
        ),
    },
    {
        'title': 'Prasad Distribution Every Sunday',
        'content': (
            'Sri Jagannath Math announces free prasad distribution every '
            'Sunday after the morning aarti. All devotees and visitors are '
            'welcome to partake in the sacred prasad of Lord Jagannath.'
        ),
    },
    {
        'title': 'Volunteers Needed for Upcoming Festival',
        'content': (
            'We are looking for dedicated volunteers to help with the '
            'upcoming festival celebrations. If you wish to serve Lord '
            'Jagannath through seva, please contact the Math office.'
        ),
    },
    {
        'title': 'New Donation Facility Available',
        'content': (
            'Devotees can now contribute to the Math through UPI and '
            'bank transfer. Visit the Donate page for details. Your '
            'generous contributions help sustain the spiritual and '
            'community activities of the Math.'
        ),
    },
    {
        'title': 'Welcome to Our New Website',
        'content': (
            'We are delighted to launch the official website of Sri '
            'Jagannath Math. Stay connected with us for updates on events, '
            'festivals, and announcements. Jai Jagannath! 🙏'
        ),
    },
]
for a in announcements_data:
    Announcement.objects.get_or_create(
        title=a['title'],
        defaults={'content': a['content'], 'is_active': True}
    )
print(f"✅ Announcements: {len(announcements_data)} entries")

# ── Donation Information ──
donation, _ = DonationInformation.objects.get_or_create(
    pk=1,
    defaults={
        'account_holder_name': 'Sri Jagannath Math Trust',
        'bank_name': '[Bank Name - Update in Admin]',
        'account_number': 'XXXXXXXXXXXX',
        'ifsc_code': 'XXXX0000000',
        'branch_name': '[Branch Name - Update in Admin]',
        'upi_id': 'jagannathmath@upi',
    }
)
print(f"✅ Donation Information: {donation}")

print("\n🎉 All seed data loaded successfully!")
print("📝 Update placeholder content through Django Admin at /admin/")
print("🔑 Admin credentials: admin / admin123")
