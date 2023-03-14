from apps.mbc.views import http_404, http_500, melding_aanmaken, root
from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", root, name="root"),
    path("melding/aanmaken", melding_aanmaken, name="melding_aanmaken"),
    path(
        "melding/verzonden",
        TemplateView.as_view(template_name="melding/verzonden.html"),
        name="melding_verzonden",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
