#!/usr/bin/env python

import urllib2
import subprocess
import os

# Yes, I am using python as a poor substitute for bash.
# No, I don't care.

adb_usb_ini = "./adb_usb.ini"
vendors = "./VENDORS"

# Format vendor_id int as hex string with leading 0s
def vendor_id_hex(vendor_id):
	return "0x%0.4x" % vendor_id

def vendor_exists_file(vendor_id, f):
	s = subprocess.Popen(("grep", "-i", "%s" % vendor_id, f), stdout = subprocess.PIPE)
	o = s.communicate()[0]
	return o.rstrip() != ""

def has_newline_adb():
	s = subprocess.Popen(("tail", "-c", "1", "%s" % adb_usb_ini), stdout = subprocess.PIPE)
	o = s.communicate()[0]
	return o.rstrip() == ""

def remove_newline_adb():
	f = adb_usb_ini + "tmp"
	os.system("perl -pe 'chomp if eof' %s > %s" % (adb_usb_ini, f))
	os.system("mv %s %s" % (f, adb_usb_ini))

def vendor_add_adb(vendor_id):
	if has_newline_adb():
		v = vendor_id
	else:
		v = "'%s%s'" % ("\\n", vendor_id)
	print "Adding %s to %s" % (vendor_id, adb_usb_ini)
	os.system("echo %s >> %s" % (v, adb_usb_ini))

def vendor_add_listing(vendor_id, vendor_name):
	print "Adding %s %s to %s" % (vendor_id, vendor_name, vendors)
	# Assume not an Android device vendor
	v = "\"%s %s %s\"" % (vendor_id, "0", vendor_name)
	os.system("echo %s >> %s" % (v, vendors))

# vendor_id must be first formatted via vendor_id_hex
def handle_vendor(vendor_id, vendor_name):
	if not vendor_exists_file(vendor_id, adb_usb_ini):
		vendor_add_adb(vendor_id)
	if not vendor_exists_file(vendor_id, vendors):
		vendor_add_listing(vendor_id, vendor_name)

# Pull data from
#  1) http://www.usb.org/developers/tools/comp_dump
#  2) http://www.linux-usb.org/usb.ids

url = "http://www.usb.org/developers/tools/comp_dump"
ids = urllib2.urlopen(url)
for l in ids.readlines():
	if l == "" or not '|' in l:
		continue
	s = l.split("|")
	vendor_id_10 = s[0]
	vendor_name = s[1].rstrip()
	handle_vendor(vendor_id_hex(int(vendor_id_10)), vendor_name)

url = "http://www.linux-usb.org/usb.ids"
ids = urllib2.urlopen(url)
for l in ids.readlines():
	if l.startswith("# List of known device classes, subclasses and protocols"):
		break;
	if l == "" or l[0] == "#" or not '  ' in l:
		continue
	if l.startswith(" ") or l.startswith("\t"):
		continue
	vendor_id_16 = l[0:4]
	vendor_name = l[5:].strip()
	handle_vendor(vendor_id_hex(int(vendor_id_16, 16)), vendor_name)

remove_newline_adb()
