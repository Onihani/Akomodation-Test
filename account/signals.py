from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail
from guardian.shortcuts  import assign_perm

@receiver(post_save, sender=User)
def email_user(sender, instance, **kwargs):
    send_mail("Account created", f"Helllo {instance.first_name} your accoumt has been created", "eritten2@gmail.com", [instance.email], fail_silently=False)


@receiver(post_save, sender=User)
def update(sender, instance, **kwargs):
    assign_perm('update_user', instance, instance)
