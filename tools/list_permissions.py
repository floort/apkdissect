#!/usr/bin/env python

import sys
from optparse import OptionParser
from pprint import pprint
import os

try:
	from androguard.core import *
	from androguard.core.androgen import *
	from androguard.core.androconf import *
	from androguard.core.bytecode import *
	from androguard.core.bytecodes.jvm import *
	from androguard.core.bytecodes.dvm import *
	from androguard.core.bytecodes.apk import *
	
	from androguard.core.analysis.analysis import *
	from androguard.core.analysis.ganalysis import *
	from androguard.core.analysis.risk import *
	from androguard.decompiler.dad import decompile
except:
	print "Androguard not found"
	print "See https://code.google.com/p/androguard/wiki/Installation"
	sys.exit(0)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: %s filename.apk [filename2.apk] [filename3.apk] ..." % (sys.argv[0])
		sys.exit(0)
	for f in sys.argv[1:]:
		a = apk.APK(f)
		for p in a.get_permissions():
			print "%s: %s" % (f, p)

