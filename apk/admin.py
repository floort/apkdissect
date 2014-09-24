from django.contrib import admin
from apk.models import *

class AppAdmin(admin.ModelAdmin):
	list_display = ['name', 'apk', 'admin_source_link']
	list_filter = ['batch']

class APKAdmin(admin.ModelAdmin):
    list_display = ['name', 'sha256', 'permissions_loaded', 'decompiled']
    list_filter = ['decompiled', 'permissions']
    search_fields = ['name', 'sha256', 'md5', 'apk']

class ImportBatchAdmin(admin.ModelAdmin):
	list_display = ['device', 'timestamp', 'admin_apps_link']
	date_hierarchy = 'timestamp'
	list_filter = ['device']

class DalvikClassAdmin(admin.ModelAdmin):
	list_display = ['name', 'source_apk_name', 'source_link']
	list_filter = ['apk']
	search_fields = ['name', 'javasource']

admin.site.register(APK, APKAdmin)
admin.site.register(Device)
admin.site.register(ImportBatch, ImportBatchAdmin)
admin.site.register(App, AppAdmin)
admin.site.register(DalvikClass, DalvikClassAdmin)
admin.site.register(Permission)

