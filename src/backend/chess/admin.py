from django.contrib import admin

from . import models


class ChessMatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')


admin.site.register(models.ChessMatch, ChessMatchAdmin)
