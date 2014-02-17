from django.contrib import admin
from apk.models import *

class AppAdmin(admin.ModelAdmin):
	list_display = ['name', 'apk', 'admin_source_link']
	list_filter = ['batch']

class APKAdmin(admin.ModelAdmin):
    list_display = ['sha256', 'apk']
    list_filter = ['permissions']
    search_fields = ['sha256', 'md5', 'apk']

class ImportBatchAdmin(admin.ModelAdmin):
	list_display = ['device', 'timestamp', 'admin_apps_link']
	date_hierarchy = 'timestamp'
	list_filter = ['device']

class DalvikClassAdmin(admin.ModelAdmin):
	list_display = ['name', 'source_link']
	list_filter = ['apk']
	search_fields = ['name', 'javasource']

admin.site.register(APK, APKAdmin)
admin.site.register(Device)
admin.site.register(ImportBatch, ImportBatchAdmin)
admin.site.register(App, AppAdmin)
admin.site.register(DalvikClass, DalvikClassAdmin)
admin.site.register(Permission)

