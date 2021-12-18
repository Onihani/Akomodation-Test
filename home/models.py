from django.db import models
from account.models import User
from django.urls import reverse

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=400)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Regions"
class Plan(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = 'plans'
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=400)
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

class Property(models.Model):
    choices = (('room_type', 'room_type'), ('land_type', 'land_type'), ('selling_house', 'selling_house'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=20)
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties')
    date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=200, verbose_name="City/Town")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'properties'
        permissions = (('update_property', 'can update property'),)
    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        return reverse('item', args=(self.pk, self.date.month, self.date.year, self.date.day))
