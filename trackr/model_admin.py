from django.contrib import admin
from django.db import transaction

from .models import TrackEntry


class TrackedModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            obj.save()
            if change:
                TrackEntry.objects.log(request=request, action=TrackEntry.Actions.UPDATE, obj=obj)
            else:
                TrackEntry.objects.log(request=request, action=TrackEntry.Actions.CREATE, obj=obj)

    def delete_model(self, request, obj):
        with transaction.atomic():
            TrackEntry.objects.log(request=request, action=TrackEntry.Actions.DELETE, obj=obj)
            obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            with transaction.atomic():
                TrackEntry.objects.log(request=request, action=TrackEntry.Actions.DELETE, obj=obj)
                obj.delete()

    def response_action(self, request, queryset):
        with transaction.atomic():
            for obj in queryset:
                TrackEntry.objects.log(
                    request=request, action=TrackEntry.Actions.ADMIN_ACTION,
                    description=request.POST['action'], obj=obj)
            return super().response_action(request, queryset)

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        if obj is not None:
            TrackEntry.objects.log(request=request, action=TrackEntry.Actions.VIEW, obj=obj)
        return super().render_change_form(request, context, add, change, form_url, obj)
