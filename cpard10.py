#!/usr/bin/python

import serial
import re

def __wL(ser, string, encoding = 'utf-8'):
    print('sending', string)
    n = ser.write(bytes(string + '\r\n', encoding))
    print('sent', n, 'bytes')

def writeTo(outputPath, string, device='/dev/ttyACM0', baud=115200):
    ser = serial.Serial(device, baud, timeout=2)
    ser.write(b'\x03')

    __wL(ser, 'f = open("{}", "w")'.format(outputPath))
    __wL(ser, 'f.write("{}")'.format(string))
    __wL(ser, 'f.close()')
    __wL(ser, 'exit()')
    ser.close()

def readFrom(inputPath, device='/dev/ttyACM0', baud=115200):
    ser = serial.Serial(device, baud, timeout=2)
    print(ser.getSettingsDict())
    ser.write(b'\x03')

    __wL(ser, 'f = open("{}", "r")'.format(inputPath))
    __wL(ser, 'data = f.read()')
    __wL(ser, 'f.close()')

    ser.flushInput()

    __wL(ser, 'print("<\\x43ARD10DATA>" + data + "</\\x43ARD10DATA>")')


    data = ser.read_until('</CARD10DATA>')
    print(len(data))
    print(data)

    ser.close()

    match = re.search('<CARD10DATA>(.*)</CARD10DATA>', data.decode(),
      re.DOTALL)

    return match.group(1) if match else None
