from django.contrib import admin

import feedback


__all__ = ()


@admin.register(feedback.models.Feedback)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.status.field.name,
    )

    def save_model(self, request, obj, form, change):
        if change:
            user = request.user
            to = form.cleaned_data["status"]
            old_status = feedback.models.Feedback.objects.get(pk=obj.pk).status
            if old_status != to:
                feedback.models.StatusLog.objects.create(
                    user=user,
                    from_status=old_status,
                    to_status=to,
                )
        super().save_model(request, obj, form, change)


admin.site.register(feedback.models.StatusLog)
