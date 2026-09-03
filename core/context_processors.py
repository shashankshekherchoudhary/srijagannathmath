from .models import TempleInformation


def temple_info_context(request):
    """Make temple information available in all templates for the footer."""
    return {
        'global_temple_info': TempleInformation.objects.first(),
    }
