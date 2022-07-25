from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        help_text=_(
            "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=True, null=True)
    is_playing = models.BooleanField(default=False)


class VariantStats(models.Model):
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    class Meta:
        abstract = True


class ReallyBadChessStats(VariantStats):
    pass


class MagicChessStats(VariantStats):
    pass


class UserStats(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    really_bad_chess = models.ForeignKey(ReallyBadChessStats, on_delete=models.SET_NULL, null=True)
    magic_chess = models.ForeignKey(MagicChessStats, on_delete=models.SET_NULL, null=True)
