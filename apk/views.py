# Create your views here.

import json
from pprint import pprint
from io import BytesIO
import zipfile

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from apk.models import *

def index(request):
	apk = APK.objects.all()[0]
	return HttpResponseRedirect("/dissect/%d" % (apk.pk,))

def showclass(request, class_id):
	dc = get_object_or_404(DalvikClass, pk=class_id)
	return render(request, 'apk/source.html', {'dalvikclass': dc})

def appindex(request):
	return render(request, 'apk/apklist.html', {
		'apps': App.objects.all()
	})
	
def menu_json(request):
	obj = {	
		"name": "toolbar",
		"items": [
			{	"type": "menu", 
				"id": "menu_open",
				"caption": "Open APK",
				"img": "icon-edit",
				"items": [{
					"text": '<a href="/dissect/%d">%s</a>' % (apk.pk, apk.name),
					"img": "icon-page"
				} for apk in APK.objects.all()]
			}
		]
	}
	return HttpResponse(json.dumps(obj), content_type="application/json")

def showapk(request, apk_id):
	apk = get_object_or_404(APK, pk=apk_id)
	return render(request, 'apk/apk.html', {
		'apk': apk
	})

def classes_to_tree(tree, path, cid):
	if len(path) == 1:
		tree[path[0]] = cid
		return tree
	if tree.has_key(path[0]):
		tree[path[0]] = classes_to_tree(tree[path[0]], path[1:], cid)
	else:
		tree[path[0]] = classes_to_tree(dict(), path[1:], cid)
	return tree

def tree_to_menu(tree, parent=""):
	l = []
	for k, v in tree.iteritems():
		if type(v) == dict:
			l.append({
				"id": "classpath_"+parent+k,
				"text": k,
				"img": "icon-folder",
				"nodes": tree_to_menu(v, parent+k+"/")
			})
		else:
			l.append({
				"id": "class_%d" %(v,),
				"text": k,
				"img": "icon-page",
			})
	return l

def classes_menu_json(request, apk_id):
	apk = get_object_or_404(APK, pk=apk_id)
	tree = dict()
	for c in DalvikClass.objects.filter(apk=apk):
		tree = classes_to_tree(tree, c.name.split("/"), c.pk)
	return HttpResponse(json.dumps(tree_to_menu(tree)), content_type="application/json")
	
def classes_zip(request, apk_id):
	apk = get_object_or_404(APK, pk=apk_id)
	output = BytesIO()
	with zipfile.ZipFile(output, 'w') as myzip:
		for c in DalvikClass.objects.filter(apk=apk):
			myzip.writestr(c.name+".java", bytes(c.javasource))
		myzip.close()
	print dir(output)
	response = HttpResponse(output.getvalue(), mimetype="application/zip")
	response['Content-Disposition'] = "attachment;filename=%d_source.zip" % (apk.pk, )
	return response
	
def dissect(request, apk_id):
	apk = get_object_or_404(APK, pk=apk_id)
	return render(request, "apk/browser.html", {"apk": apk})
