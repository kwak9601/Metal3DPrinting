#!/usr/bin/env python

#   Label STX DataLength  Command DataPart    ETX CheckSum
#No.Bytes   1       1       2       0to510      1       1

## Do not modify
import serial
import time
import os
import matplotlib.pyplot as plt
#from drawnow import *
global comPort

def makeFig():
    plt.plot(xnew,ynew,'ro')

def readprof(length):
    flag=0
    if comPort.inWaiting():
        val=comPort.read(1)

        if val==b'\x02':
            buffer=[]
            buffer.append(val)
            counter=0
            while 1:
                counter=counter+1
                val=comPort.read(1)
                if val==b'\x03' and counter>length and flag==0:
                    flag=1
                    buffer.append(val)
                elif flag:
                    buffer.append(val) 
                    break
                elif val:
                    buffer.append(val)
                else:
                    break
            #print 'Time=', (time.time()-time1)
            return buffer

class Intarray():
    def __init__(self,xar,yar):
        self.xarray = xar
        self.yarray = yar
    

def profilometer():
#plt.ion()
#time.sleep(1)
#inputstring=(b'\x02\x00\x20\x1C\x03\x3C') #is camera settings command (working)
    while 1:
        try:
        #time.sleep(0.5)#without this time(not exact number yet the communication will fail after a few iterations
            time1=time.time()
            inputstring=([2, 3, 0, 2, 0, 119, 240, 4, 126, 47, 3, 211]) #is acquiring measured value (working)-needs to convert to meters
            loop=0
            length=[3,504,8]
            comPort.write(inputstring)
            time.sleep(0.001)
            data=None
            while comPort.inWaiting() > 0:
                # print(length[loop])
                data=readprof(length[loop])
                loop=loop+1
                if loop==1:
                    time.sleep(0.02)
                if loop==2:
                    break
                print(data)
            if data:
                pass
            else:
                continue
            if len(data)==514:                
                receive=[]
                for index in data:
                    x=ord(index)
                    receive.append(x)
            #print(receive)
            #print('exited loop')
                new=receive[8:-2]
                x=[]
                y=[]
                toggle=False
                for index,item in enumerate(new):
                    if index%2==0:
                        toggle=not toggle
                    if toggle:
                        x.append(item)
                    else:
                        y.append(item)
                xnew=[]
                ynew=[]
                for var in range(0,len(x)):
                    if var%2==0:
                        xint=0x100*x[var]+x[var+1]
                        xnew.append(xint)
                        yint=0x100*y[var]+y[var+1]
                        ynew.append(yint)
            #drawnow(makeFig)
            #plt.show()
            #plt.plot(xnew,ynew,'ro')
                print 'LoopingAgain'
                print 'Time=', (time.time()-time1)
                array=Intarray(xnew,ynew)
                return array
                break
        except:
            print "error"+str(IOError)
            raise

# comPort=serial.Serial('/dev/serial0',2000000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout=0.001)
comPort=serial.Serial('/dev/ttyUSB0',2000000,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout=0.001)
comPort.isOpen()
##t=profilometer()
##print t.xarray
##print t.yarray
