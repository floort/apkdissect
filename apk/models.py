from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

import os
from hashlib import sha1, sha256

from pygments import highlight
from pygments.lexers import JavaLexer
from pygments.formatters import HtmlFormatter

#from analyze import get_classes, get_permissions, get_name

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
    apk = models.ForeignKey('APK', on_delete=models.CASCADE)
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


def create_APK_from_file(filename, decompile=True):
    with open(filename, 'rb') as f:
        sha1sum = sha1(f.read()).hexdigest()
        f.seek(0,0)
        sha256sum = sha256(f.read()).hexdigest()
        apk, created = APK.objects.get_or_create(sha1=sha1sum, sha256=sha256sum)
        if not created:
            print("Skiped duplicate")
            return apk
        f.seek(0,0)
        apk.apk.save(os.path.basename(filename), ContentFile(f.read()))
        apk.save()
    if decompile:
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
    sha1 = models.CharField(max_length=40, db_index=True)
    name = models.CharField(max_length=256, null=True)
    permissions = models.ManyToManyField(Permission)
    permissions_loaded = models.BooleanField(default=False)
    decompiled = models.BooleanField(default=False)
    bug_tags = models.ManyToManyField('BugTag')
    
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
        self.name = ""
        #self.name = get_name(os.path.join(settings.MEDIA_ROOT, self.apk.name))
        self.save()
    
    def _classify_bugs(self):
        # ALLOW_ALL_HOSTNAME_VERIFIER
        tag, created = BugTag.objects.get_or_create(name="ALLOW_ALL_HOSTNAME_VERIFIER", defaults={
            "description": "Disabled certificate checks"
        })
        print(tag, created)
        if len(self.dalvikclass_set.filter(javasource__contains='ALLOW_ALL_HOSTNAME_VERIFIER')) > 0:
            self.bug_tags.add(tag)
    def num_bug_tags(self):
        return len(self.bug_tags.all())
        
        
        
    
class Device(models.Model):
    identifier = models.CharField(max_length=256)
    notes = models.TextField()
    
    def __unicode__(self):
        return self.identifier

class ImportBatch(models.Model):
	device = models.ForeignKey(Device, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return u'%s @ %s' % (self.device, self.timestamp)
	
	def admin_apps_link(self):
		return u'<a href="/admin/apk/app/?batch__id__exact=%d">Show apps</a>' % (self.id)
	admin_apps_link.allow_tags = True

class App(models.Model):
	name = models.CharField(max_length=256)
	location = models.CharField(max_length=256)
	apk = models.ForeignKey(APK, on_delete=models.CASCADE)
	batch = models.ForeignKey(ImportBatch, on_delete=models.CASCADE)
	
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

class BugTag(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
	
    def __unicode__(self):
	    return self.name
		
		
