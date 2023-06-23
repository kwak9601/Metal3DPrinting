
import serial
import time
import binascii
import copy

com_port = serial.Serial('/dev/ttyUSB0', 2000000, parity=serial.PARITY_NONE, \
                         stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
                         # timeout=0.001)

def xor(buffer):
    x_sum=0x0
    for b in buffer:
        x_sum=x_sum^b
    return x_sum
    

def construct_message(command, output=[], is_debug=False):
    #creates the buffer of bytes that the profilometer recognises
    STX = 0x02
    ETX = 0x03
    length=int(len(output)/2)
    buffer=[STX, length]
    buffer.extend(command)
    buffer.extend(output)
    buffer.append(ETX)
    SUM=xor(buffer[1:-1])
    buffer.append(SUM)
    data_send=bytearray(buffer)
    if is_debug:
        print_list_hex(buffer)
    # print(data_send)
    return data_send #x is the bytes string of Buffer


def acquire_address(is_debug=False): # Manual, pg 114
    command = [0x40, 0x0B]
    output = []
    data_send = construct_message(command, output, is_debug)
    com_port.write(data_send)


def acquire_profile_sz(address, is_debug=False): # Manual, pg 115
    rlen = 0x02
    fixed = 0x11
    command=[0x00, 0x02]
    output=[]
    output.extend(address)
    output.append(rlen)
    output.append(fixed)
    data_send = construct_message(command, output, is_debug)
    com_port.write(data_send)


def acquire_profile(address, rlen, thinning, is_debug=False): # Manual, pg 115
    command = [0x00, 0x02]
    output = []
    output.extend(address)
    output.append(rlen)
    output.append(thinning)
    data_send = construct_message(command, output, is_debug)
    com_port.write(data_send)
    
    
def acquire_measurement(out, is_debug=False):
    command = [0xa0, 0x17]
    output = [0x00, out-1]
    data_send = construct_message(command, output, is_debug)
    com_port.write(data_send)
    
    
def acquire_output_status(is_debug=False):
    command = [0xa0, 0x10]
    output = []
    data_send = construct_message(command, output, is_debug)
    com_port.reset_input_buffer()
    com_port.write(data_send)
    
    
def get_response(is_debug=False):
    t_start = time.time()
    while com_port.inWaiting() == 0:
        pass
    data = com_port.read(com_port.inWaiting())
    
    # TODO Verify checksum
        
    com_port.flushInput()
    if is_debug:
        print(list(data))
    return data, time.time() - t_start
    
    
def extract_value_out(data):
    # TODO Negative numbers do not work -> needs to be fixed
    value = data[4:8]
    value = float(twos_comp(int(value.encode('hex'), 16), 32))/1000
    return value
    
    
def extract_address(data):
    data = data[4:8]
    data_int = int(data.encode('hex'), 16)
    data_list = []
    for byte in data:
        data_list.append(int(byte.encode('hex'), 16))
    return data_list, data_int
    

def extract_profile_sz(data):
    sz_profile_hex = data[8:10]
    return int(sz_profile_hex.encode('hex'), 16)
    
    
def extract_profile(data):
    profile_hex = data[8:-2]
    i = 0
    # x = []
    # y = []
    x_array = []
    y_array = []
    # for i, byte in enumerate(profile_hex):
    #     if i%2==0:
    #         x.append()
    
    while i <= len(profile_hex)-4:
        # x_array.append(i/4)
        x = float(twos_comp(int(profile_hex[i:i + 2].encode('hex'), 16), 16))
        if x >= 0x7fff:
            # print("x invalid")
            x = float('nan')
        x_array.append(x)
        # print('i: ' + str(i) + ', i + 2: ' + str(i + 2))
        # print('i: ' + str(i) + ', x: ' + str(x))
        # y_array.append(i/4)
        y = float(twos_comp(int(profile_hex[i + 2:i + 4].encode('hex'), 16), 16))
        if y >= 0x7fff:
            # print("y invalid")
            y = float('nan')
        y_array.append(y)
        # print('i + 2: ' + str(i + 2) + ', i + 4: ' + str(i + 4))
        # print('i+2: ' + str(i + 2) + ', y: ' + str(x))
        i += 4
        # i += 2
        # print(i)
    
    return x_array, y_array
    # new=data[8:-2]
    # x=[]
    # y=[]
    # toggle=False
    # for index,item in enumerate(new):
    #     if index%2==0:
    #         toggle=not toggle
    #     if toggle:
    #         x.append(item)
    #     else:
    #         y.append(item)
    # xnew=[]
    # ynew=[]
    # for var in range(0,len(x)-2):
    #     if var%2==0:
    #         xint=0x100*x[var]+x[var+1]
    #         xnew.append(xint)
    #         yint=0x100*y[var]+y[var+1]
    #         ynew.append(yint)
    # # array=Intarray(xnew,ynew)
    # return xnew, ynew
    
    
def print_list_hex(array):
    print ' '.join([hex(i) for i in array])
    
    
def bytearray_to_list(byte_array):
    byte_list= []
    for byte in byte_array:
        byte_list.append(int(byte.encode('hex'), 16))
    
    
def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(binascii.hexlify(b), 16)
    return result
    
    
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is
