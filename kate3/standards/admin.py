from django.contrib import admin

from standards.models import Subject, Cluster, Category, Subcategory, Grade, CommonCoreStandard, Activity, Website, Application

class SubcategoryAdmin(admin.ModelAdmin):
	filter_horizontal = ('category',)

class ActivityInline(admin.TabularInline):
	model = Activity
	extra = 3

class WebsiteInline(admin.TabularInline):
	model = Website
	extra = 3

class ApplicationInline(admin.TabularInline):
	model = Application
	extra = 3

class CommonCoreStandardAdmin(admin.ModelAdmin):
	search_fields = ('description',)
	list_display = ('standard_code', 'grade', 'domain', 'strand', 'standard', 'substandard', 'category', 'subcategory', 'description')
	list_filter = ('grade', 'domain', 'subject')
	inlines = [ActivityInline, WebsiteInline, ApplicationInline]

admin.site.register(Subject)
admin.site.register(Cluster)
admin.site.register(Category)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Grade)
admin.site.register(CommonCoreStandard, CommonCoreStandardAdmin)