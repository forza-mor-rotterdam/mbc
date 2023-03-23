from apps.mbc.views import http_404, http_500, melding_aanmaken, melding_email, root
from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", root, name="root"),
    path("melding/aanmaken", melding_aanmaken, name="melding_aanmaken"),
    path("melding/email", melding_email, name="melding_email"),
    path(
        "melding/verzonden",
        TemplateView.as_view(template_name="melding/verzonden.html"),
        name="melding_verzonden",
    ),
    path("health/", include("health_check.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
