from django.contrib import admin
from django import forms

from tick.models import *

class CoreContentAdmin(admin.ModelAdmin):
    search_fields = ('code',)
        
class TechnologyStandardAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {'fields': ('point', 'subpoint', 'description', 'category', 'name'),}),
    )
    class Media:
        js = ('/static/js/admin.js',)

class ProgramOfStudyAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    list_filter = ('level', 'bigidea')

class ResourceAdminForm(forms.ModelForm):
    """
    This is to fix an issue with the URL field.
    
    If a field has unique=True and blank=True, it does not treat a blank string
    as a NULL.  If you left the URL blank before, it would raise an IntegrityError.
    This changed with the query refactoring, so I used a custom `ModelForm` and 
    cleaned the URL.  I tested to see if it was a blank string, and if so, I set it
    to None.
    """
    class Meta:
        model = Resource
    
    def __init__(self, *args, **kwargs):
        select_fields = ('content_standards', 'tech_sub_component', 'tech_standards')

        for field in select_fields:
            self.base_fields[field].widget.attrs['size'] = 12
            
        super(ResourceAdminForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        if self.cleaned_data['url'] == '':
            self.cleaned_data['url'] = None
        return self.cleaned_data 

class ResourceAdmin(admin.ModelAdmin):
    form = ResourceAdminForm
    filter_horizontal = ('content_standards','common_core_standards')
    fieldsets = (
        ('Resource General', {'fields': ('resource_type', 'entered_by', 'focus', 'sub_focus', 'levels', 'content_areas', 'loti_level')}),
        ('Resource Information', {'fields': ('title', 'description', 'url', 'filename', 'feebased', 'source', 'created', 'user')}),
        ('Technology', {'fields': ('tech_standards', 'tech_component', 'tech_sub_component')}),
        ('Core Content', {'fields': ('content_standards',)}),
        ('Common Core Standard', {'fields': ('common_core_standards','aligned_to_common_core', 'aligned_by', 'status')}),
        ('Other', {'classes': 'collapse', 'fields': ('published', 'disabled')}),
    )
    list_display = ('title', 'created', 'published', 'aligned_to_common_core','entered_by', 'aligned_by', 'status', 'user')
    list_filter = ('aligned_to_common_core', 'status', 'created', 'content_areas', 'levels', 'resource_type', 'tech_sub_component', 'entered_by', 'published', 'disabled')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    save_on_top = True
    
    class Media:
        js = ('/static/js/admin.js',)
        
class AnnouncementAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Announcement', {'fields': ('body', 'picture')}),
    )
    list_display = ('body',)
    search_fields = ('body',)
    
class NoticeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Notice', {'fields': ('body',)}),
    )
    filter_horizontal = ('winner',)
    list_display = ('body',)
    search_fields = ('body',)

class CommonCoreStandardAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'grade', 'domain', 'standard', 'description')
    list_filter = ('grade', 'domain')
    
admin.site.register(CoreContent, CoreContentAdmin)
admin.site.register(TechIndicator)
admin.site.register(TechnologyComponent)
admin.site.register(TechnologySubComponent)
admin.site.register(TechnologyStandard, TechnologyStandardAdmin)
admin.site.register(ProgramOfStudy, ProgramOfStudyAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Favorite)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(CommonCoreStandard, CommonCoreStandardAdmin)

