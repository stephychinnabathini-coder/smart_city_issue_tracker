from django.contrib import admin
from .models import Issue, Notification

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'user', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        if change:
            old = Issue.objects.get(pk=obj.pk)
            if old.status != obj.status:
                Notification.objects.create(
                    user=obj.user,
                    message=f"Status of '{obj.title}' changed to {obj.get_status_display()}.")
        super().save_model(request, obj, form, change)

admin.site.register(Notification)
