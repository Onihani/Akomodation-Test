from django.contrib.auth import authenticate
import re
import unicodedata
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.text import capfirst
from django.contrib.auth import password_validation



from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from home.models import Property
from django.forms import ModelForm
from .models import User
from django import forms
from django.contrib.auth.tokens import default_token_generator

from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)

UserModel = get_user_model()

class SignupForm(forms.ModelForm):
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'telephone', 'email', 'password', 'password2']
        widgets = {'password':forms.PasswordInput()}

    def clean_password(self):
        password1 = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:

            # Method inherited from BaseForm
            self.add_error('password', error)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match")

        return password2

    def clean_email(self):

        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("That email is taken already")
        return email

    def clean_username(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError("An account associated with this user name already exist")
        return user
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if len(telephone) > 13 or len(telephone) < 10:
            raise forms.ValidationError("Your telephone number shouldn't be more than 13 or less than 10 numbers.")
        return telephone
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not(first_name.isalpha()):
            raise forms.ValidationError("Your first name cannot contain non-alphabets charactors")
        return first_name
    def clean_last_name(self):
        second_name = self.cleaned_data['last_name']
        if not(second_name.isalpha()):
            raise forms.ValidationError("Your second name cannot contain non-alphabets charactors")
        return second_name

class LoginForms(forms.Form):
    username = forms.CharField(max_length=300, label="Your user name")
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    def clean_username(self):
        self._name = self.cleaned_data['username']
        if not(User.objects.filter(username=self._name).exists()):
            raise forms.ValidationError("Account with this user name does not exist")
        if not(User.objects.get(username=self._name).is_active):
            raise forms.ValidationError("Account with this user name is inactive contact us to get your account activated")
        return self._name
    def clean_password(self):
        name = self._name
        password = self.cleaned_data['password']
#        try:
        if User.objects.filter(username=name).exists():
            if not(User.objects.get(username=name).check_password(password)):

                raise forms.ValidationError(f"The password for {name} account is invalid")
#        except:
#            forms.ValidationError("The user does not exist")
        return password


class CreateProp(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'type', 'plan', 'price', 'image', 'region', 'location']
        labels = {'price': "Type a price without the currency sign. If your property is for rent, the price is per month."}

    def clean_price(self):
        price = self.cleaned_data['price'].strip()
        if not(re.search(r'\d+,\d+$|\d{1}|\d{2}|\d{3}', price)):
            raise forms.ValidationError("Write your price in the correct format eg: 1,000,000")

        return price
    def clean_image(self):
        image  = self.cleaned_data['image']
        size = image.size
        if size > 10000000:
            raise forms.ValidationError("Your image size should be 10mb or less")
        return image
    def clean_title(self):
        title = self.cleaned_data['title']
        if Property.objects.filter(title=title).exists():
            raise forms.ValidationError("An item with this name already exist")
        return title

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password




class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


