import factory

from ..models import User


class UnactivatedUserFactory(factory.django.DjangoModelFactory):
    """
    Automatically create Users with good names
    """
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = '123qwe'
    email_verified = False
    is_active = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class PasswordlessUserFactory(UnactivatedUserFactory):
    """
    Sets password to None, thus making the password unusable(not setting it really equal None but just unusable value)
    you can use user.has_usable_password() to check if the user has entered a password or not.
    """
    password = None


class ActivatedUserFactory(UnactivatedUserFactory):
    email_verified = True
    is_active = True


class ClosedAccountFactory(ActivatedUserFactory):
    is_active = False


UserFactory = ActivatedUserFactory  # easier name For easier consumption by other apps
