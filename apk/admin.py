from django.contrib import admin
from apk.models import *

class APKAdmin(admin.ModelAdmin):
    list_display = ['sha256', 'apk']
    list_filter = ['permissions']
    search_fields = ['sha256', 'md5', 'apk']

class DalvikClassAdmin(admin.ModelAdmin):
	list_display = ['name', 'source_link']
	list_filter = ['apk']
	search_fields = ['name', 'javasource']

admin.site.register(APK, APKAdmin)
admin.site.register(Device)
admin.site.register(ImportBatch)
admin.site.register(App)
admin.site.register(DalvikClass, DalvikClassAdmin)
admin.site.register(Permission)

