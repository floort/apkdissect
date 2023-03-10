from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from subprocess import call, check_output
from apk.models import *
import os
import sys
from hashlib import sha1, sha256

ADB = "adb"

def fastprint(s):
	print(s,)
	sys.stdout.flush()

def get_connected_devices():
	out = check_output([ADB, "devices"])
	lines = out.strip().split(b"\n")[1:]
	return [l.split()[0].decode() for l in lines]
	
def list_packages(device=None):
	out = check_output([ADB, 'shell', 'pm', 'list', 'packages', '-f'])
	#if device == None:
	#	out = check_output([ADB, 'shell', 'pm', 'list', 'packages', '-f'])
	#else:
	#	out = check_output([ADB, '-s', device, 'shell', 'pm', 'list', 'packages', '-f'])
	for line in out.split():
		print(line)
		label, rest = line.split(b':')
		path, name = rest.rsplit(b'=', 1)
		yield [label.decode(), path.decode(), name.decode()]

class Command(BaseCommand):
	args = ''
	help = 'Import all apk\'s from connected device'

	def handle(self, *args, **options):
		for deviceid in get_connected_devices():
			device, created = Device.objects.get_or_create(identifier=deviceid)
			if created: device.save()
			importbatch = ImportBatch(device=device)
			importbatch.save()
			self.stdout.write('Importing from "%s"' % device)
			for p in list_packages(deviceid):
				out = check_output([ADB, 'shell', 'sha1sum', p[1]])
				sha1sum = out.split()[0].strip().decode()
				if len(sha1sum) != 40:
					print("Could not read", p[2])
					continue
				if len(APK.objects.filter(sha1=sha1sum).all()) > 0:
					print("Skipping duplicate", p[2])
					continue
				tmpfile = os.path.join('/tmp/', p[2])
				print(p[2])
				out = check_output([ADB, '-s', deviceid, 'pull', p[1], tmpfile])
				if not os.path.isfile(tmpfile):
					print("ERROR: skipping apk")
					continue
				apk = create_APK_from_file(tmpfile, decompile=False)
				os.remove(tmpfile)
				apk._load_name()
				apk.save()
				app = App(name = p[2], location = p[1], apk = apk, batch = importbatch)
				app.save()

