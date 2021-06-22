#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
test_serial.py - 测试你的串口,在运行前应该使能串口

@Created on MAY 1 2021
@author:菜伟
@email:li_wei_96@163.com
"""

import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # open serial port
print (ser.name)         # check which port was really used

if __name__ == "__main__":
    while(1):
        ser.flush()             # it is buffering. required to get the data out *now*
        line = ser.readline()   # read a '\n' terminated line
        print (line) #int(ang), int(deg)
    ser.close()             # close port