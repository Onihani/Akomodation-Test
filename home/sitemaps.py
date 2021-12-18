from django.contrib.sitemaps import Sitemap
from .models import Property

class PropertyMap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    def items(self):
        return Property.objects.all()
    def lastmod(self, obj):
        return obj.date
    def location(self, obj):
        return obj.get_absolute_url
