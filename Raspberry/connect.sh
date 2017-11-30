#!/bin/sh
sysctl -w net.ipv4.ip_forward=1
connmanctl enable wifi
sleep 2
connmanctl tether wifi on secureCar 123456789