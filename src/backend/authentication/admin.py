from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserStats, ReallyBadChessStats, MagicChessStats


admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserStats)
admin.site.register(ReallyBadChessStats)
admin.site.register(MagicChessStats)
