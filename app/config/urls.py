from apps.mbc.views import (
    gebruiker_informatie,
    http_404,
    http_500,
    login_mislukt,
    login_verplicht,
    melding_aangemaakt_email,
    melding_aanmaken,
    melding_afgesloten_email,
    melding_verzonden,
    root,
    sso_logout,
)
from apps.signalen.viewsets import SignaalViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"signaal", SignaalViewSet, basename="signaal")

urlpatterns = [
    path("api/v1/", include((router.urls, "app"), namespace="v1")),
    path("api-token-auth/", views.obtain_auth_token),
    path("", root, name="root"),
    path("melding/aanmaken", melding_aanmaken, name="melding_aanmaken"),
    path(
        "melding/verzonden/<uuid:signaal_uuid>/",
        melding_verzonden,
        name="melding_verzonden",
    ),
    path(
        "email/melding-aangemaakt/<uuid:signaal_uuid>/",
        melding_aangemaakt_email,
        name="melding_aangemaakt_email",
    ),
    path(
        "email/melding-afgesloten/<uuid:signaal_uuid>/",
        melding_afgesloten_email,
        name="melding_afgesloten_email",
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

if settings.OIDC_RP_CLIENT_ID:
    urlpatterns += [
        path(
            "gebruiker-informatie/", gebruiker_informatie, name="gebruiker_informatie"
        ),
        path("login-verplicht/", login_verplicht, name="login_verplicht"),
        path("login-mislukt/", login_mislukt, name="login_mislukt"),
        path("sso-logout/", sso_logout, name="sso_logout"),
        path("oidc/", include("mozilla_django_oidc.urls")),
    ]

if settings.DEBUG:
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
