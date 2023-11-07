from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm


__all__ = ()


def feedback(request):
    template = "feedback/feedback.html"
    form = FeedbackForm(request.POST or None)
    context = {
        "feedback_form": form,
    }
    if request.method == "POST" and form.is_valid():
        text = form.cleaned_data.get("text")
        mail_to = form.cleaned_data.get("mail")
        send_mail(
            "Обратная связь получена",
            text,
            settings.DJANGO_MAIL,
            [mail_to],
            fail_silently=False,
        )
        messages.success(
            request,
            "Письмо успешно отправлено!",
        )
        return redirect("feedback:feedback")

    return render(request, template, context)
