from django.contrib import admin

from mobile_apps.models import App, Type

class AppAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_filter = ('cost', 'published', 'created_at', 'type')
    list_display = ('name', 'type', 'cost', 'published', 'created_at', 'user')
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
            'productivity',
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
    search_fields = ('name',)

    class Media:
        js = ('/static/js/mobile_apps_admin.js',)

admin.site.register(App, AppAdmin)
admin.site.register(Type)