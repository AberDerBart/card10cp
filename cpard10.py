#!/usr/bin/python
import re
import time
from textwrap import wrap

import serial


def __wL(ser, string):
    print('sending', string)
    n = ser.write(string + b'\r\n')
    print('sent', n, 'bytes')

def writeTo(outputPath, string, device='/dev/ttyACM0', baud=115200, encoding='utf-8'):

    ser = serial.Serial(device, baud, timeout=2)
    ser.write(b'\x03')

    __wL(ser, bytes('f = open("{}", "w")'.format(outputPath), 'utf-8'))
    for chunk in wrap(string, 512):
        time.sleep(0.1)
        escapedChunk = str(chunk.encode(encoding=encoding))
        __wL(ser, bytes('f.write({})'.format(escapedChunk), 'utf-8'))
    __wL(ser, b'f.close()')
    ser.close()

def readFrom(inputPath, device='/dev/ttyACM0', baud=115200, encoding='utf-8'):
    ser = serial.Serial(device, baud, timeout=2)
    print(ser.getSettingsDict())
    ser.write(b'\x03')

    __wL(ser, bytes('f = open("{}", "r")'.format(inputPath), 'utf-8'))
    __wL(ser, b'data = f.read()')
    __wL(ser, b'f.close()')

    ser.flushInput()

    # spaces are necessary, otherwise end tag can get corrupted
    __wL(ser, b'print("<\\x43ARD10DATA>" + data +      "</\\x43ARD10DATA>")')


    data = ser.read_until('</CARD10DATA>\r\n')
    print(len(data))
    print(data)

    ser.close()

    match = re.search('<CARD10DATA>(.*)</CARD10DATA>', data.decode(encoding=encoding),
      re.DOTALL)

    return match.group(1) if match else None