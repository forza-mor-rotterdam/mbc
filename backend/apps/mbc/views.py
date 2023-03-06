from django.shortcuts import render, redirect
from django.urls import reverse
from apps.mbc.forms import MeldingAanmakenForm


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


def melding_aanmaken(request):
    form = MeldingAanmakenForm()
    if request.POST:
        form = MeldingAanmakenForm()

    return render(
        request,
        "melding/aanmaken.html",
        {
            "form": form
        },
    )

