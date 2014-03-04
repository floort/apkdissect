from django.core.management.base import BaseCommand, CommandError
from apk.models import *


class Command(BaseCommand):
	args = ''
	help = 'Decompile apks in the database'
	
	def handle(self, *args, **options):
		for apk in APK.objects.filter(decompiled=False):
			print apk.apk
			try:
				# clean all classes that should not be there
				DalvikClass.objects.filter(apk=apk).delete()
				# Start decompilation
				apk._load_classes()
				apk.decompiled = True
			except:
				apk.decompiled = False
				print "\tFailed!"
			apk.save()

