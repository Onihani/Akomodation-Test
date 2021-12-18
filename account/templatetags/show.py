from django import template
from home.models import Property
register = template.Library()

@register.inclusion_tag('show.html')
def shows(user):
    obj = Property.objects.filter(owner__username=user).all()
    return {'obj': obj}
