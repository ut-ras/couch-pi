#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:38:56 2019

@author: takuma
"""

import evdev
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)
found = False
while not found:
    try:
        found = True
        """
        change InputDevice to actual device path
        """
        device = evdev.InputDevice('/dev/input/event18')
    except Exception:
            found = False
            print("yeet")
            pass
print("yote")