from guardian.decorators import permission_required_or_403
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.db.models import Q
from .models import Property
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .forms import ReportForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_page

# Create your views here.
def home(request):
    houses = Property.objects.filter(type__name__icontains="Houses").all()[:15]
    lands = Property.objects.filter(type__name__icontains="Lands").all()[:15]
    rooms = Property.objects.filter(type__name__icontains="Rooms").all()[:15]
    t_houses = "Houses";t_rooms = "Rooms";t_lands = "Lands"
    return render(request, 'home/home.html', {'houses':houses, 'lands':lands, 'rooms':rooms, "t_houses":t_houses, "t_lands":t_lands, "t_rooms":t_rooms})

@login_required
def update(request):
    return render(request, 'home/item_update.html')

def properties(request):
    if request.GET.get('search'):
        q = request.GET.get('search')
        properties = Property.objects.filter(Q(description__icontains=q) | Q(title__icontains=q) | Q(location__icontains=q))
        if q is not None:
            prop = Paginator(properties, 12)
            page = request.GET.get('page')
            page_obj = prop.get_page(page)
            return render(request, 'list/properties.html', {'page_obj': page_obj})

class Item(DetailView):
    model = Property
    template_name = 'list/detail.html'
    context_object_name = 'item'

def report(request, pk):
    name = request.POST.get("name")
    telephone = request.POST.get("telephone")
    email = request.POST.get("email")
    msg = request.POST.get("message, """)
    obj = get_object_or_404(Property, pk=pk)
    owner = obj.owner.username
    item = obj.title
    t = obj.owner.telephone
    send_mail(f"{name} reporting {owner} for {item} property owner tel: {t}", f"Content: {msg}"+"\n"+f"reporter email {email}\n"+f"reporter tel: {telephone}", email, ["eritten2@gmail.com"], fail_silently=False)
    messages.success(request, "We have received your report")
    return redirect("home")

def about(request):
    return render(request, 'home/about.html')

def privacy(request):
    return render(request, 'home/privacy.html')

def terms(request):
    return render(request, 'home/terms.html')

def services(request):
    return render(request, 'home/services.html')

def contact(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        msg = request.POST.get('msg')
        tel = request.POST.get('telephone')
        send_mail("Customer contact",  f"The name is {username.capitalize()}. The email is {email}. The content of the message is {msg} ", email, ['eritten2@gmail.com'], fail_silently=True)
        messages.success(request, f'Thank you for contacting us {username.capitalize()}. We will reply you within 24 hours to {email}.')
        return redirect('/')
    return render(request, 'home/contact.html')

def category(request, name):
    page = request.GET.get('page')
    category = Property.objects.filter(type__name=name).all()
    obj = Paginator(category, 20)
    page_obj = obj.get_page(page)
    return render(request, 'home/category.html', {'page_obj':page_obj, "name":name})

def region(request):
    page = request.GET.get('page')
    region = request.GET.get('region')
    items = Property.objects.filter(region__name__icontains=region).all()
    filters = [{"title":item.title, "description":item.description, "date":item.date, "url":item.get_absolute_url, "image":item.image.url, "price": item.price, "location": item.location, "plan": item.plan.name,} for item in items]
    obj = Paginator(filters, 12)
    pages = obj.num_pages
    page_obj = obj.get_page(page)
#    page_obj = page_obj.object_list.append({"pages":pages})

    return JsonResponse(page_obj.object_list+[{"pages":pages}], safe=False)
