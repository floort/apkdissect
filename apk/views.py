# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from apk.models import *

def showclass(request, class_id):
	dc = get_object_or_404(DalvikClass, pk=class_id)
	return render(request, 'apk/source.html', {'dalvikclass': dc})

def apkindex(request):
	pass
