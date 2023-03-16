from apps.mbc.forms import MeldingAanmakenForm
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse


def http_404(request):
    return render(
        request,
        "404.html",
    )


def http_500(request):
    return render(
        request,
        "500.html",
    )


def root(request):
    return redirect(reverse("melding_aanmaken"))


def handle_uploaded_file(f):
    with open("/media/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def melding_aanmaken(request):
    if request.POST:
        form = MeldingAanmakenForm(request.POST, request.FILES)
        is_valid = form.is_valid()
        print(request.FILES)
        if is_valid:
            send_to = ["maurice@tiltshift.nl"]
            if form.cleaned_data.get("email_melder"):
                send_to.append(form.cleaned_data.get("email_melder"))
            send_mail(
                "Begraven & cremeren Service aanvraag",
                "Dit is een standaard tekst voor B&C",
                settings.DEFAULT_FROM_EMAIL,
                send_to,
                fail_silently=False,
            )
            return redirect("melding_verzonden")
    else:
        form = MeldingAanmakenForm()

    return render(
        request,
        "melding/aanmaken.html",
        {"form": form},
    )
