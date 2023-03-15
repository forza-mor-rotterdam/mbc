from apps.mbc.forms import MeldingAanmakenForm
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


def melding_aanmaken(request):
    if request.POST:
        form = MeldingAanmakenForm(request.POST)
        is_valid = form.is_valid()
        if is_valid:
            return redirect("melding_verzonden")
    else:
        form = MeldingAanmakenForm()

    return render(
        request,
        "melding/aanmaken.html",
        {"form": form},
    )
