from django.contrib import admin
from logger.models import Entry

class EntryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'action', 'created_at',)
    list_filter = ('action', 'created_at',)

admin.site.register(Entry, EntryAdmin)