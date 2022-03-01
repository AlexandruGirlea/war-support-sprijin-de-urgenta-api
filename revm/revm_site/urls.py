from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from app_volunteering.views import CreateVolunteeringResourceViewSet, CreateVolunteeringRequestViewSet

admin_site_string = _("Emergency Support Admin")
admin.site.site_title = admin_site_string
admin.site.site_header = admin_site_string
admin.site.index_title = admin_site_string

router = routers.DefaultRouter()
router.register(r"item_request", CreateVolunteeringRequestViewSet, basename="item_request")
router.register(r"item_resources", CreateVolunteeringResourceViewSet, basename="item_resource")

router.register(r"other_request", CreateVolunteeringRequestViewSet, basename="other_request")
router.register(r"other_resources", CreateVolunteeringResourceViewSet, basename="other_resource")

router.register(r"transport_service_request", CreateVolunteeringRequestViewSet, basename="transport_request")
router.register(r"transport_service_resources", CreateVolunteeringResourceViewSet, basename="transport_resource")

router.register(r"volunteering_request", CreateVolunteeringRequestViewSet, basename="volunteering_request")
router.register(r"volunteering_resources", CreateVolunteeringResourceViewSet, basename="volunteering_resource")

urlpatterns = (
    i18n_patterns(
        # URL patterns which accept a language prefix
        path(
            "admin/password_reset/",
            auth_views.PasswordResetView.as_view(),
            name="admin_password_reset",
        ),
        path(
            "admin/password_reset/done/",
            auth_views.PasswordResetDoneView.as_view(),
            name="password_reset_done",
        ),
        path(
            "admin/reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(),
            name="password_reset_confirm",
        ),
        path(
            "admin/reset/done/",
            auth_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete",
        ),
        path("admin/", admin.site.urls, name="admin"),
        path("logout", LogoutView.as_view(), name="logout"),
    )
    + [
        # URL patterns which do not use a language prefix
        path("api/v1/", include(router.urls)),
        path("auth/", include("dj_rest_auth.urls")),
        path("i18n/", include("django.conf.urls.i18n")),
        path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/v1/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="swagger-ui"),
            name="swagger-ui",
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.ENABLE_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
