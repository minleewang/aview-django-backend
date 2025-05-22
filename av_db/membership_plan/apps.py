# membership_plan/apps.py

from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MembershipConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "membership_plan"

    def ready(self):
        from .membership_initializer import create_default_memberships
        post_migrate.connect(create_default_memberships, sender=self)
