from django.shortcuts import render, redirect, get_object_or_404
from .models import Property
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse

def send_owner_mail(request, pk):
    obj = get_object_or_404(Property, pk=pk)
    owner = obj.owner.email
    item = obj.title
    tel = request.POST.get("telephone")
    email = request.POST.get("email")
    msg = request.POST.get("message")
    name = request.POST.get("name")
    send_mail(f"{name} contacting you for {item} property uploaded by you tel: {tel}", msg, email, [owner], fail_silently=False)
    messages.success(request, "The message has been sent")
    return redirect("home")
