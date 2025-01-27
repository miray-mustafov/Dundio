from django.contrib import admin
from apps.cards.models import ClubCard


@admin.register(ClubCard)
class ClubCardAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ['is_active', 'type', ]
    search_fields = ('number',)
