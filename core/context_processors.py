from django.core.cache import cache
from .models import TempleInformation


def temple_info_context(request):
    """Make temple information available in all templates with caching."""
    cached_info = cache.get('global_temple_info')
    if cached_info is None:
        cached_info = TempleInformation.objects.first()
        cache.set('global_temple_info', cached_info, 86400)
    return {
        'global_temple_info': cached_info,
    }
