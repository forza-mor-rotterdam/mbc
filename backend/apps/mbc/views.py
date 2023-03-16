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
            return redirect("melding_verzonden")
    else:
        form = MeldingAanmakenForm()

    return render(
        request,
        "melding/aanmaken.html",
        {"form": form},
    )
