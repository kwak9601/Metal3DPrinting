#!/usr/bin/python
####in progress (threading)


#   Label STX DataLength  Command DataPart    ETX CheckSum
#No.Bytes   1       1       2       0to510      1       1

## Do not modify
import serial
import threading
import time
import array as arr

comPort=None
## Do not modify



##y=str(STX)
##x=str.encode(y+'\r\n')
##print(x)
##print(type(x))




      
##if (len(Commands)%2)!=0:
##    print('Error: Command not divisible by 2\n')
##    exit()
##

#Settings Functions




#Send Functions

def XOR(Buffer):
    xSum=0x0
    for b in Buffer:
        xSum=xSum^b
    return xSum


def createBuffer(Command,Output=[]):
    #creates the buffer of bytes that the profilometer recognises
    STX=0x02
    ETX=0x03
    Length=int(len(Output)/2)
    BUFFER=[STX,Length]
    BUFFER.extend(Command)
    BUFFER.extend(Output)
    BUFFER.append(ETX)
    SUM=XOR(BUFFER[1:-1])
    BUFFER.append(SUM)
    print(BUFFER,type(BUFFER))
    x=bytes(BUFFER)
    print(x)
    return x #x is the bytes string of Buffer
    
def AcqMValues():#pg 113
    Commands=[0xa0,0x17]
    Outputs=[0x00, 0x00]
    SendValue=createBuffer(Commands,Outputs)
    return SendValue

def AcqAddress():#pg 114
    Commands=[0x40,0x0B]
    SendValue=createBuffer(Commands)
    return SendValue

def AcqProfileSize(): #pg 115
    Commands=[0x00,0x02]
    Address=[]#not a static variable, must be replaced with address received from AcqAddress
    RLen=[]
    Fixed=[]

def ReadProfile(): #pg115
    Commands=[0x00,0x02]
    Address=[]#not a static variable, must be replaced with address received from AcqAddress
    RLen=[]
    Thinning=[]






#Reply Functions

def parseIncoming(Reply):
    #breaks the incoming data from profilometer into the different parts of the data (Reply, Extract, SUM, Length, Command, Data)
    SUM=Reply[-1:] #SUM=Reply[-1]
    Extract=Reply[1:-2]
    Length=Extract[:1] #Length=Extract[0] (gives list instead of element) #Length,Command,Data=Extract[0],Extract[1:2],Extract[3:]
    Command=Extract[1:3]
    Data=Extract[3:]
    print(Reply, Extract, SUM, Length, Command, Data)
    
#Simple Functions

def byte2List(Bytestr):
    NewList=list(Bytestr)
    #ex. : print(list(b'\x02\x01\xa0\x17\x00\x00\x03\xb6')) -> [2, 1, 160, 23, 0, 0, 3, 182]
    return NewList



#Main

t=AcqAddress()#might have bug with showing ascii
print(t)
#AcqMValues()

#parseIncoming(b'\x02\x01\xa0\x17\x00\x00\x03\xb6')
#x=byte2List(b'\x02\x01\xa0\x17\x00\x00\x03\xb6')



