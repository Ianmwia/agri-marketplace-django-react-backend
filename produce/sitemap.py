from django.contrib.sitemaps import Sitemap
from .models import Produce

class ProduceSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Produce.objects.all()
    def location(self, obj):
        return f'/produce/{obj.id}/'