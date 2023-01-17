import factory
from django.contrib.auth.models import User

from .models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_showroom = factory.Faker("random_element", elements=[True, False])
    is_provider = factory.Faker("random_element", elements=[True, False])
    is_client = factory.Faker("random_element", elements=[True, False])
    is_verified = factory.Faker("random_element", elements=[True, False])
    can_edit = False


class AdminUserFactory(CustomUserFactory):
    is_staff = True
    is_superuser = True
    is_showroom = True
    is_provider = True
    is_client = True
    can_edit = True


class ProviderUserFactory(CustomUserFactory):
    is_showroom = False
    is_provider = True
    is_client = False
    can_edit = True
