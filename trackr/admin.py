from django.contrib import admin

from .model_admin import TrackedModelAdmin
from .models import TrackEntry


@admin.register(TrackEntry)
class TrackEntryAdmin(TrackedModelAdmin):
    list_display = ['id', 'date', 'principal', 'action', 'description', 'object', 'object_id']
    list_filter = ['date', 'action', 'object']
    search_fields = [
        'id', 'principal__id', 'description', 'object', 'object_id',
        'principal__username', 'principal__nome', 'principal__email'
    ]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
