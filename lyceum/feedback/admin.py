from django.contrib import admin
from django.http.request import HttpRequest

import feedback.models


__all__ = ()


class FileInline(admin.TabularInline):
    model = feedback.models.FeedbackFile
    fields = ("file",)


class AuthorInline(admin.TabularInline):
    model = feedback.models.Author
    fields = ("name", "mail")

    def has_delete_permission(self, request: HttpRequest, obj) -> bool:
        return False


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.status.field.name,
    )

    inlines = [FileInline, AuthorInline]

    def save_model(self, request, obj, form, change):
        if change:
            to = form.cleaned_data["status"]
            old_status = feedback.models.Feedback.objects.get(pk=obj.pk).status
            if old_status != to:
                feedback.models.StatusLog.objects.create(
                    user=request.user,
                    from_status=old_status,
                    to_status=to,
                )
        super().save_model(request, obj, form, change)


admin.site.register(feedback.models.StatusLog)
