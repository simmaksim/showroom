from django.urls import path
from rest_framework import routers

from users import views

from .views import RegisterView, VerifyEmail

router = routers.DefaultRouter()
router.register(r"users", views.CustomUserViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
]

urlpatterns += router.urls
