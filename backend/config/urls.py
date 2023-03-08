from apps.mbc.views import http_404, http_500, melding_aanmaken, root
from django.conf import settings
from django.urls import path

urlpatterns = [
    path("", root, name="root"),
    path("melding/aanmaken", melding_aanmaken, name="melding_aanmaken"),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
