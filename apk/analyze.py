#!/usr/bin/env python

import sys
from optparse import OptionParser
from pprint import pprint
import os

from androguard.core import *
from androguard.core.androgen import *
from androguard.core.androconf import *
from androguard.core.bytecode import *
from androguard.core.bytecodes.dvm import *
from androguard.core.bytecodes.apk import *

from androguard.core.analysis.analysis import *
from androguard.core.analysis.ganalysis import *
from androguard.core.analysis.risk import *
from androguard.decompiler.decompiler import *

def get_classes(apk_filename):
	a = apk.APK(apk_filename)
	d = dvm.DalvikVMFormat(a.get_dex())
	d.create_python_export()
	dx = uVMAnalysis(d)
	gx = GVMAnalysis(dx, None)
	d.set_vmanalysis(dx)
	d.set_gvmanalysis(gx)
	d.set_decompiler(DecompilerDAD(d, dx))
	d.create_xref()
	d.create_dref()
	
	for cur_class in d.get_classes():
		yield [cur_class.get_name(), cur_class.get_source()]

def get_all_classes(filename):
    a = apk.APK(filename)
    raw_dex = a.get_dex()
    if raw_dex:
        d = dvm.DalvikVMFormat(raw_dex)
        vmx = analysis.VMAnalysis(d)
        
        for cur_class in d.get_classes():
            dc = decompile.DvClass(cur_class, vmx)
            print [cur_class.get_name(), dc.get_source()]
            yield [cur_class.get_name(), dc.get_source()]

def get_permissions(filename):
    a = apk.APK(filename)
    return  a.get_permissions()
    
    
def get_name(filename):
	a = apk.APK(filename)
	return a.package
