from django.contrib import admin

from mobile_apps.models import App, Type

class AppAdmin(admin.ModelAdmin):
    list_filter = ('cost', 'free')

admin.site.register(App, AppAdmin)
admin.site.register(Type)