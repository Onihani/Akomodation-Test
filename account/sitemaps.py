from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class Account(Sitemap):
    changefreq = 'never'
    priority = 0.5
    def items(self):
        return ['home', 'about', 'contact', 'login_user', 'services', 'terms', 'signup']
    def location(self, obj):
        return reverse(obj)
