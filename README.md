One true adb_usb.ini to rule them all!
======================================

This is an adb_usb.ini containing every known Android vendor ID (and all other known USB vendors on the planet,
just for good measure).

To clone into your .android directory (for easy updating via git):

    $ cd ~/.android
    $ rm adb_usb.ini
    $ git init
    $ git remote add origin git@github.com:apkudo/adbusbini.git
    $ git pull origin master

Alternatively, to just copy the latest file directly into your .android:

    $ curl https://raw.githubusercontent.com/apkudo/adbusbini/master/adb_usb.ini > ~/.android/adb_usb.ini

A parseable listing is included in VENDORS, using the following format:

    <vendor_id> <is_android_vendor> <vendor_name>

For data sources, we used every Android device that we have (which is, we believe, all of them), the Linux USB
listing at http://www.linux-usb.org/usb.ids, and the USB listing at http://www.usb.org/developers/tools/comp_dump.
If you're interested, the tool used to scrape the web data sources is in adbusbini_scrape.py.

Updates are very much encouraged and appreciated - please either submit a pull request or email to
josh@apkudo.com.

Brought to you by the friendly hackers at Apkudo (www.apkudo.com / @apkudo).

(Obligatory legal note: All code, listings, etc. is released into the public domain, is provided as-is,
and carries no warranties.)
