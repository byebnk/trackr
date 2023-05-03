from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import TrackEntry


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    if user.is_staff:
        TrackEntry.objects.log(request=request, action=TrackEntry.Actions.LOGIN, obj=user, principal=user)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    if user and user.is_staff:
        TrackEntry.objects.log(request=request, action=TrackEntry.Actions.LOGOUT, obj=user)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    try:
        UserModel = get_user_model()
        user = UserModel.objects.get(username=credentials['username'], is_staff=True)
        TrackEntry.objects.log(request=request, action=TrackEntry.Actions.LOGIN_FAILED, obj=user, principal=user)
    except UserModel.DoesNotExist:
        pass
