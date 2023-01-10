from rest_framework import routers

from users import views

router = routers.DefaultRouter()
router.register(r"users", views.CustomUserViewSet)

urlpatterns = router.urls
