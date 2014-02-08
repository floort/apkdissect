from django.contrib import admin
from apk.models import *

class APKAdmin(admin.ModelAdmin):
    list_display = ['sha256', 'md5']
    list_filter = ['permissions']

class DalvikClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'apk']
    search_fields = ['name', 'javasource']

admin.site.register(APK, APKAdmin)
admin.site.register(Device)
admin.site.register(ImportBatch)
admin.site.register(App)
admin.site.register(DalvikClass, DalvikClassAdmin)
admin.site.register(Permission)

