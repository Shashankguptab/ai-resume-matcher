from django.contrib import admin
from .models import MatchResult


class MatchResultAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "resume",
        "job",
        "match_score",
        "created_at",
    ]


admin.site.register(
    MatchResult,
    MatchResultAdmin
)