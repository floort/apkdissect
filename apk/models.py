from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

import os
from hashlib import md5, sha256

from pygments import highlight
from pygments.lexers import JavaLexer
from pygments.formatters import HtmlFormatter

from analyze import get_classes, get_permissions, get_name

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
    
    def source_link(self):
    	return u'<a href="/showclass/%d">Source</a>' % (self.id)
    source_link.allow_tags = True
    
    def java_html(self):
    	return highlight(self.javasource, JavaLexer(), HtmlFormatter())

    def source_apk_name(self):
        return self.apk.name


def create_APK_from_file(filename):
    with open(filename) as f:
        md5sum = md5(f.read()).hexdigest()
        f.seek(0,0)
        sha256sum = sha256(f.read()).hexdigest()
        apk, created = APK.objects.get_or_create(md5=md5sum, sha256=sha256sum)
        if not created:
            print "Skiped duplicate"
            return apk
        f.seek(0,0)
        apk.apk.save(os.path.basename(filename), ContentFile(f.read()))
        apk.save()
    try:
        apk._load_name()
        apk._load_permissions()
        apk._load_classes()
    except:
        pass
    return apk


class APK(models.Model):
    apk = models.FileField(upload_to="apks/")
    sha256 = models.CharField(max_length=64, db_index=True)
    md5 = models.CharField(max_length=32, db_index=True)
    name = models.CharField(max_length=256, null=True)
    permissions = models.ManyToManyField(Permission)
    permissions_loaded = models.BooleanField(default=False)
    decompiled = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.sha256

    def _load_permissions(self):
        self.permissions.clear()
        for p in get_permissions(os.path.join(settings.MEDIA_ROOT, self.apk.name)):
            perm, created = Permission.objects.get_or_create(name=p)
            if created: perm.save()
            self.permissions.add(perm)
        self.permissions_loaded = True
        self.save()
    
    def _load_classes(self):
        for c in DalvikClass.objects.filter(apk=self):
            c.delete()
        for name, source in get_classes(os.path.join(settings.MEDIA_ROOT, self.apk.name)):
            dalvikclass = DalvikClass(name=name)
            dalvikclass.javasource = source
            dalvikclass.apk = self
            dalvikclass.save()
        self.decompiled = True
        self.save()
 	
    def _load_name(self):
        self.name = get_name(os.path.join(settings.MEDIA_ROOT, self.apk.name))
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
	
	def admin_apps_link(self):
		return u'<a href="/admin/apk/app/?batch__id__exact=%d">Show apps</a>' % (self.id)
	admin_apps_link.allow_tags = True

class App(models.Model):
	name = models.CharField(max_length=256)
	location = models.CharField(max_length=256)
	apk = models.ForeignKey(APK)
	batch = models.ForeignKey(ImportBatch)
	
	def __unicode__(self):
		return self.name
	
	def admin_source_link(self):
		return u'<a href="/admin/apk/dalvikclass/?apk__id__exact=%d">Show source</a>' % (self.id)
	admin_source_link.allow_tags = True
	
class File(models.Model):
	sha256 = models.CharField(max_length=64, db_index=True)
	apk = models.FileField(upload_to="apks/")
	
	def __unicode__(self):
		return u'File:%s' % (self.sha256)
		
		
		
