
import sick_profiler_2 as profiler
import time
import binascii
from matplotlib import pyplot as plt
import struct

i = 0

if not profiler.com_port.isOpen():
    profiler.com_port.open()

while i < 1:

    time_start = time.time()
    
    # Get the address 
    profiler.acquire_address()
    response, dt = profiler.get_response(False)
    
    # Extract the address from received message
    addr_list, addr_int = profiler.extract_address(response)
    print("Address: " + str(list(addr_list)))
    
    # Get the profile length
    profiler.acquire_profile_sz(addr_list, False)
    response, dt = profiler.get_response(False)
    print("Profile size response: " + str(list(response)))
    
    sz_profile = profiler.extract_profile_sz(response)
    print("Profile size: " + str(sz_profile/32))

    x_array_total = []
    y_array_total = []
    j = 0
    addr_int += 0x04
    max_j, rem = divmod((sz_profile/32), 126)
    while j <= max_j:
        addr_bytes = bytearray(struct.pack(">I", addr_int))
        print ("addr_bytes (list): " + str(list(addr_bytes)))
        # addr_list = profiler.bytearray_to_list(addr_bytes)
        # Get the profile
        div = 0x1
        thinning = 0x20 + div
        rlen = 0x7e
        if (rem != 0) and (j == max_j):
            rlen = rem
        profiler.acquire_profile(list(addr_bytes), rlen, thinning, False)
        response, dt = profiler.get_response(False)
        # Extract the profile and put in data structure
        x_array, y_array = profiler.extract_profile(response)
        x_array_total.extend(x_array)
        y_array_total.extend(y_array)
        time.sleep(0.02)
        addr_int += 0x7e * 2
        
        j += 1
        
    print("dt: " + str(time.time() - time_start))
    # # plot profile
    f = plt.figure(1)
    plt.plot(x_array_total, y_array_total)
    f.show()
    
    i += 1
    time.sleep(0.1)
    
    
profiler.com_port.close()


input("Press Enter to close")
