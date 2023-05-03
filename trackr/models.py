import pgtrigger
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip


class TrackEntryManager(models.Manager):
    def log(self, *, request, action, obj, principal=None, description=None):
        self.model.objects.create(
            principal=principal or request.user,
            action=action,
            description=description,
            object=f'{obj.__class__.__module__}.{obj.__class__.__name__}',
            object_id=obj.pk,
            ip_address=get_client_ip(request)[0],
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
        )


class TrackEntry(models.Model):
    class Actions(models.TextChoices):
        CREATE = 'create', _('Create')
        VIEW = 'view', _('View')
        UPDATE = 'update', _('Update')
        DELETE = 'delete', _('Delete')

        # Users
        LOGIN = 'login', _('Login')
        LOGOUT = 'logout', _('Logout')
        LOGIN_FAILED = 'login-failed', _('Login failed')
        LOGIN_LOCKED = 'login-locked', _('Login locked')

        # Misc
        ADMIN_ACTION = 'admin-action', _('Admin action')
        OTHER = 'other', _('Other')

    date = models.DateTimeField(default=timezone.now)
    principal = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    action = models.CharField(max_length=100, choices=Actions.choices)
    description = models.CharField(max_length=100, null=True, blank=True)
    object = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, null=True, blank=True)

    objects = TrackEntryManager()

    class Meta:
        triggers = [
            pgtrigger.ReadOnly(name="read_only")
        ]
