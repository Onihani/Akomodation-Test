from django import template
from ..models import Property
import timeago, datetime, pytz

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v

    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.inclusion_tag('hiring.html')
def hiring():
    obj = Property.objects.filter(plan__name__icontains='renting').all().order_by('date')[:15]
    return {"obj":obj}

@register.inclusion_tag('selling.html')
def selling():
    obj = Property.objects.filter(plan__name__icontains='selling').all().order_by('date')[:15]
    return {"obj":obj}

@register.filter
def ago(d):
    current = datetime.datetime.now(tz=pytz.utc)
#     z = pytz.utc(current)
    return timeago.format(d, current)
