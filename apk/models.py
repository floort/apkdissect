from django.db import models
from django.conf import settings

import os

from analyze import get_all_classes, get_permissions

# Create your models here.

class Permission(models.Model):
    name = models.CharField(max_length=512)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        if len(self.name) > 45:
            return self.name[:42]+"..."
        return self.name
        
class DalvikClass(models.Model):
    name = models.CharField(max_length=512)
    apk = models.ForeignKey('APK')
    javasource = models.TextField()
    
    def __unicode__(self):
        return self.name


class APK(models.Model):
    apk = models.FileField(upload_to="apks/")
    sha256 = models.CharField(max_length=64, db_index=True)
    md5 = models.CharField(max_length=32, db_index=True)
    permissions = models.ManyToManyField(Permission)
    
    def __unicode__(self):
        return self.sha256
        
    def _load_permissions(self):
        self.permissions.clear()
        for p in get_permissions(os.path.join(settings.MEDIA_ROOT, self.apk.name)):
            perm, created = Permission.objects.get_or_create(name=p)
            if created: perm.save()
            self.permissions.add(perm)
        self.save()
    
    def _load_classes(self):
        for c in DalvikClass.objects.filter(apk=self):
            c.delete()
        for name, source in get_all_classes(os.path.join(settings.MEDIA_ROOT, self.apk.name)):
            dalvikclass = DalvikClass(name=name)
            dalvikclass.javasource = source
            dalvikclass.apk = self
            dalvikclass.save()
        self.save()
        
        
        
    
class Device(models.Model):
    identifier = models.CharField(max_length=256)
    notes = models.TextField()
    
    def __unicode__(self):
        return self.identifier

class ImportBatch(models.Model):
    device = models.ForeignKey(Device)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s @ %s' % (self.device, self.timestamp)

class App(models.Model):
    name = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    apk = models.ForeignKey(APK)
    batch = models.ForeignKey(ImportBatch)
    
    def __unicode__(self):
        return self.name
