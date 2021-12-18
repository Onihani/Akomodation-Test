from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.conf import settings
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect, JsonResponse, QueryDict
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.core.exceptions import ValidationError

from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from django.views.generic.base import TemplateView
#from django.contrib.auth.mixings import PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect

from django.utils.decorators import method_decorator

from django.contrib.auth.tokens import default_token_generator

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail
from django.views.generic.edit import FormView
from .forms import (
    PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)


from django.contrib.auth.hashers import make_password
from django.views.generic import ListView
from home.views import Property
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForms
from .models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateProp
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from guardian.mixins import PermissionRequiredMixin, LoginRequiredMixin
from guardian.decorators import permission_required_or_403
from django.views.decorators.cache import cache_page 
# Create your views here.
UserModel = get_user_model()
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():    
            password = request.POST.get('password')
            user = form.save(commit=False)
            user.password = make_password(password)
            email,first_name = request.POST.get('email'), request.POST.get('first_name')
            user.save()
            messages.success(request, f"Your account has been created. Welcome to the Akomodation family! \nYou can visit {email} to see confirmation ")
            return redirect('login_user')
        return render(request, 'registration/signup.html', {'form':form})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})
# signup view

def user_login(request):
    if request.method == "POST":
        form = LoginForms(request.POST)
        if form.is_valid():
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        return render(request, 'registration/login.html', {'form':form})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForms()
        return render(request, 'registration/login.html', {'form':form})

@login_required
def log_out(request):
    logout(request)
    return render(request, 'dashboard/logout.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def read(request):
    if request.GET.get('search'):
        q = request.GET.get('search')
        properties = Property.objects.filter(owner__username=request.user.username).filter(Q(description__icontains=q))
        if q is not None:
            prop = Paginator(properties, 12)
            page = request.GET.get('page')
            page_obj = prop.get_page(page)
            return render(request, 'crud/read.html', {'page_obj': page_obj, 'p': q})

# a view to display user specific items.

@login_required
def create(request):
    if request.method == "POST":
        form = CreateProp(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.owner = request.user
            user.save()
            messages.success(request, 'You have successfully uploaded your property.')
            return redirect('dashboard')
        return render(request, 'crud/create.html', {'form':form})
    else:
        form = CreateProp()
        return render(request, 'crud/create.html', {'form':form})

class Update(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'home.update_property'
    model = Property
    raise_exception = True
    permission_denied_message = 'Please you are trying to access item which was not uploaded by you. If you persist this activity you will loose your account'
    fields = ['title', 'description', 'image', 'price', 'location']
    context_object_name = 'item'
    template_name = 'crud/update.html'
    success_url = reverse_lazy('item_update')

class Latest(ListView):
    model = Property
    context_object_name = 'items'
    template_name = 'crud/latest.html'

    def get_queryset(self):
         return super().get_queryset().filter(owner__username=self.request.user.username).all()[:6]
# displaying latest 6 items uploaded by a specific user.


@login_required
def delete_obj(request):
    pk = request.GET.get('pk')
    obj = get_object_or_404(Property, pk = pk)
    obj.delete()
    return JsonResponse({'okay': 'yes'})

@login_required
def delete_user(request, pk):
#    pk = request.GET.get('pk')
    obj = get_object_or_404(User, pk=pk)
    user = obj.is_active = False
    obj.save()
    messages.success(request, 'account deleted')
    return redirect('home')
#from django.contrib.auth.mixins import PermissionRequiredMixin

class UpdateUser(PermissionRequiredMixin,UpdateView):
    permission_required = 'account.update_user'
    model = User
    raise_exception = True
    fields = ['username', 'first_name', 'last_name', 'email', 'telephone']
    template_name = 'registration/change_info.html'


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context

@login_required
def info(request):
    return render(request, 'info.html')


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

@login_required
def message(request):
    name = request.user.username
    msg = request.POST.get("message")
    user = get_object_or_404(User, username=name)
    send_mail(f"Message from member {user.username} tel: {user.telephone}. email: {user.email}", msg, user.email, ['eritten2@gmail.com'], fail_silently=False)
    messages.success(request, "Your message has been sent")
    return redirect('dashboard')
