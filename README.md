apkdissect
==========

Apkdissect is a Python/Django application that uses androguard for the analysis 
of apk files.

Installation
============

For Ubuntu 15.04:
 * `sudo apt-get install git python-pip python-django python-pygments android-tools-adb`
 * `sudo pip install -e git+https://github.com/androguard/androguard.git#egg=androguard`
 * `git clone https://github.com/floort/apkdissect.git`
 * `cd apkdissect`

Before running apkdissect on a new system, some changes should be made to `apkdissect/settings.py`:
 * `ADMINS` should be set to your name and email
 * `DATABASES` has a good default `sqlite3` database, but can be updated to use other databases.
 * `MEDIA_ROOT` should be set to the location of the `apkdissect/mediaroot` directory.
 * `SECRET_KEY` should be given a new random value

Create database:
 * `./manage.py syncdb`
 

Importing APKs
==============

Connect a Android device to the computer and make sure `adb` can connect to it.
Run `./manage.py apkimport` to import all installed apk files from the connected device.

All apks will be deduplicated to save storage space and to improve import and analysis speed.
Each import will be given a unique importbatch that specifies the device identifier, import timestamp
and all apks that are installed on the device at that time.

Admin interface
===============

Imported apks can be explored through the Django admin interface in a webbrowser.
The webserver can be started with `./manage.py runserver` and the data can be 
explored by pointing your webbrowser to `http://localhost:8000/admin/`.

Bugs
====

 * In general: This tool is not even close to being finished


