from django.shortcuts import render

def error404(request, exception):
    return render(request, 'errors/error404.html')

def error403(request, exception):
    return render(request, 'errors/error403.html')

def error400(request, exception):
    return render(request, 'errors/error400.html')

def error500(request):
    return render(request, 'errors/error500.html')

def error503(request, exception):
    return render(request, 'errors/error503.html')

def error504(request, exception):
    return render(request, 'errors/error504.html')
