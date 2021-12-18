from django.contrib import admin
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static
from home.email import send_owner_mail
from home.sitemaps import PropertyMap
from django.contrib.sitemaps import GenericSitemap # new
from django.contrib.sitemaps.views import sitemap # new
from home.models import Property
from account.sitemaps import Account


maps = {"property": PropertyMap, "urls":Account}

urlpatterns = [
path('item_updated/', views.update, name='item_update'),
path('account/', include('account.urls')),
path('api/', include('apis.urls')),
path("report/<int:pk>/", views.report, name='report'),
path('send_mail/', send_owner_mail, name='send_mail'),
path('item/<int:pk>/<int:year>/<int:month>/<int:day>/', views.Item.as_view(), name='item'),
path('', views.home, name='home'),
path('contact/', views.contact, name='contact'),
path('about/', views.about, name='about'),
path('terms/', views.terms, name='terms'),
path('services/', views.services, name='services'),
path('results/', views.properties, name='property'),
path('email/<int:pk>/', send_owner_mail, name='email'),
    path('admin/', admin.site.urls),
path('category/<str:name>/', views.category, name='category'),
path('region/', views.region, name='region'),
    path('sitemap.xml', sitemap, # new
        {'sitemaps': maps},
        name='django.contrib.sitemaps.views.sitemap'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# error handlers.
handler404 = 'home.errors.error404'
handler403 = 'home.errors.error403'
handler500 = 'home.errors.error500'
handler503 = 'home.errors.error503'
handler504 = 'home.errors.error504'
handler400 = 'home.errors.error400'
