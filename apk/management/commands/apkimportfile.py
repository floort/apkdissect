from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from subprocess import call, check_output
from apk.models import *
import os
import sys
from hashlib import md5, sha256

def fastprint(s):
	print s,
	sys.stdout.flush()

class Command(BaseCommand):
	args = ''
	help = 'Import apk from file'

	def handle(self, *args, **options):
		if len(args) == 1:
			q = args[0]
		else:
			q = False
		if q:
			create_APK_from_file(q)