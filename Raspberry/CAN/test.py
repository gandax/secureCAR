#!python
from __future__ import print_function

import can
import time

def send_cyclic():
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    msg = can.Message(arbitration_id=0x400,
                      data=[2, 0, 0, 0, 0, 0, 0, 0],
                      extended_id=False)

    DELAY_PERIOD = 0.05 #the delay period btw sending
    timeLastSend = time.time()
    isRunning = True

    try:
        while(isRunning):
            if(time.time() - timeLastSend >= DELAY_PERIOD):
                bus.send(msg)
                timeLastSend = time.time()
                #time.sleep(0.02) #Change Delay to balance accuracy/CPU usage

        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

if __name__ == "__main__":
    send_cyclic()
