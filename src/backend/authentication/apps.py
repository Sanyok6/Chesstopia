from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Class used to configure a 64-bit int as the field for authentication."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
