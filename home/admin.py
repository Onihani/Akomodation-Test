from django.contrib import admin
from .models import Property
from .models import Category, Region, Plan

# Register your models here.

class PropAdmin(admin.ModelAdmin):
    model = Property
    list_display = ['description', 'type', 'image', 'date', 'price']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Region)
admin.site.register(Property, PropAdmin)
admin.site.site_title = "Akomodation"
admin.site.site_header = "Akomodation"
admin.site.register(Plan)
