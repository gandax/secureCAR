#!/bin/sh
ifconfig wlan0 up
wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant.conf -Dwext && dhclient wlan0
