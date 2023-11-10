from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import AuthorForm, FeedbackFileForm, FeedbackForm
from feedback.models import FeedbackFile


__all__ = ()


def feedback(request):
    template = "feedback/feedback.html"
    form = FeedbackForm(request.POST or None)
    author_form = AuthorForm(request.POST or None)
    file_form = FeedbackFileForm(request.POST or None)
    context = {
        "feedback_form": form,
        "author_form": author_form,
        "file_form": file_form,
    }
    if (
        request.method == "POST"
        and form.is_valid()
        and author_form.is_valid()
        and file_form.is_valid()
    ):
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
        author = author_form.save()
        fb = form.save(commit=False)
        fb.author = author
        fb.save()
        # instance = FeedbackFile(file=request.FILES["files"])
        files = request.FILES.getlist("files")
        for file in files:
            FeedbackFile.objects.create(
                file=file,
                feedback=fb,
            )
        return redirect("feedback:feedback")

    return render(request, template, context)
