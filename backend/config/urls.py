from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from core.views import (
    PublicLoginView,
    PublicLogoutView,
    dashboard,
    profile,
    profile_edit,
    register,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("accounts/register/", register, name="accounts_register"),
    path("accounts/login/", PublicLoginView.as_view(), name="accounts_login"),
    path("accounts/logout/", PublicLogoutView.as_view(), name="accounts_logout"),
    path("accounts/profile/", profile, name="accounts_profile"),
    path("accounts/profile/edit/", profile_edit, name="accounts_profile_edit"),
    path("items/", include("core.urls")),
    path("occurrences/", include("occurrences.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
