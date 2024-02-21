from django.contrib import admin

from scores.models import Score


class ScoreAdmin(admin.ModelAdmin):
    list_display = ['score', 'comment', 'user', 'listing']


admin.site.register(Score, ScoreAdmin)
