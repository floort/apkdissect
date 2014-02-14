#!/usr/bin/env python

import sys

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
	if len(sys.argv) != 2:
		print "Usage: %s filename.apk" % (sys.argv[0])
		sys.exit(0)
	a = apk.APK(sys.argv[1])
	d = dvm.DalvikVMFormat(a.get_dex())
	vmx = analysis.VMAnalysis(d)
	
	for cur_class in d.get_classes():
		dc = decompile.DvClass(cur_class, vmx)
		print "=============================================="
		print cur_class.get_name()
		print "=============================================="
		print dc.get_source()		

