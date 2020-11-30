from django.contrib import admin
from base.models import ActionLogModel


@admin.register(ActionLogModel)
class VideoInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'log_type', 'action',
                    'content_object', 'created_at')
    search_fields = ('log_type', 'action', 'user__username',)
