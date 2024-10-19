from .models import SiteSettings

def site_settings(request):
    settings = SiteSettings.objects.first()  # Get the first and only instance of SiteSettings
    return {
        'site_settings': settings,  # Make this available in all templates
    }
