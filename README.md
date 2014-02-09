apkdissect
==========

Apkdissect is a Python/Django application that uses androguard for the analysis 
of apk files.

Installation
============

Dependencies:
	* `adb` in your `$PATH`
	* `androguard`
	* `django`
	
Before running apkdissect on a new system, some changes should be made to `apkdissect/settings.py`:
	* `ADMINS` should be set to your name and email
	* `DATABASES` has a good default `sqlite3` database, but can be updated to use other databases.
	* `MEDIA_ROOT` should be set to the location of the `apkdissect/mediaroot` directory.
	* `SECRET_KEY` should be given a new random value

