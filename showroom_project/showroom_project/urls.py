from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from showroom import views

from .yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register(r"cars", views.CarViewSet)
router.register(r"showrooms", views.ShowroomViewSet)
router.register(r"showroomsalehistory", views.ShowroomSaleHistoryViewSet)
router.register(r"providersalehistory", views.ProviderSaleHistoryViewSet)
router.register(r"providers", views.ProviderViewSet)
router.register(r"clients", views.ClientViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include("users.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.urls.authtoken")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]
urlpatterns += doc_urls
