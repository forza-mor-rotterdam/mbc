from apps.mbc.views import http_404, http_500, melding_aanmaken, melding_email, root
from apps.signalen.viewsets import SignaalViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"signaal", SignaalViewSet, basename="signaal")

urlpatterns = [
    path("api/v1/", include((router.urls, "app"), namespace="v1")),
    path("", root, name="root"),
    path("melding/aanmaken", melding_aanmaken, name="melding_aanmaken"),
    path("melding/email", melding_email, name="melding_email"),
    path(
        "melding/verzonden",
        TemplateView.as_view(template_name="melding/verzonden.html"),
        name="melding_verzonden",
    ),
    path("health/", include("health_check.urls")),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
