
import sick_profiler_2 as profiler
import time
import binascii

i = 0

if not profiler.com_port.isOpen():
    profiler.com_port.open()

while i < 20:

    ## Read OUTs
    # Acquire the OUT
    profiler.acquire_measurement(1, False)
    # profiler.acquire_output_status(True)

    # Get the response
    response, dt = profiler.get_response(False)
    print(profiler.extract_value_out(response))
    i += 1
    time.sleep(0.1)
    
    
profiler.com_port.close()
