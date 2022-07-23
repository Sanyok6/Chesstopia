from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField("username", max_length=25)
    email = models.EmailField("email address", unique=True)
    is_online = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)


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
