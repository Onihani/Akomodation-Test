from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from .models import Property

@receiver(post_save, sender=Property)
def set_permission(sender, instance, **kwargs):
    """Add object specific permission to the author"""
    assign_perm(
        "update_property",  # The permission we want to assign.
        instance.owner,  # The user object.
        instance  # The object we want to assign the permission to.
    )
