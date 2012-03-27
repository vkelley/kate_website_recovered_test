from django.contrib import admin

from mobile_apps.models import App, Type

class AppAdmin(admin.ModelAdmin):
    list_filter = ('cost',)

    class Media:
        js = ('/static/js/mobile_apps_admin.js',)

admin.site.register(App, AppAdmin)
admin.site.register(Type)