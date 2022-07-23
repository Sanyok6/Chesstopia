from django.db.models.signals import post_save

from . import models


def setup_user_stats(sender, instance, created, **kwargs):
    if created:
        really_bad_chess_stats = models.ReallyBadChessStats.objects.create()
        magic_chess_stats = models.MagicChessStats.objects.create()

        models.UserStats(user=instance, really_bad_chess=really_bad_chess_stats, magic_chess=magic_chess_stats).save()


post_save.connect(setup_user_stats, sender=models.CustomUser, dispatch_uid="setup_user_stats")
