from django.contrib import admin

from mobile_apps.models import App, Type

class AppAdmin(admin.ModelAdmin):
    list_filter = ('cost', 'published', 'user')
    list_display = ('name', 'type', 'cost', 'published', 'user')
    fieldsets = (
        ('App', {'fields': (
            'name',
            'description',
            'educational_uses',
            'type',
            'cost',
            'link',
            'levels',
            'content_areas',
        )}),

        ('Info', {'fields': (
            'user',
            'published',
            'created_at',
        )}),

        ('Info From Store', {'fields': (
            'store_name',
            'store_cost',
            'store_link',
        )})
    )

    class Media:
        js = ('/static/js/mobile_apps_admin.js',)

admin.site.register(App, AppAdmin)
admin.site.register(Type)