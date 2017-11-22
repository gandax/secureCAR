#!python
from __future__ import print_function

import can
import time
import logging
from threading import Thread

class Receive_listener(can.Listener):
    """
    The Printer class is a subclass of :class:`~can.Listener` which simply prints
    any messages it receives to the terminal.

    :param output_file: An optional file to "print" to.
    """

    def __init__(self, output_file=None):
        if output_file is not None:
            #logging.log.info("Creating log file '{}' ".format(output_file))
            output_file = open(output_file, 'wt')
        self.output_file = output_file

    def on_message_received(self, msg):
        if self.output_file is not None:
            self.output_file.write(str(msg) + "\n")
        else:
            print(msg)

    def __del__(self):
        self.output_file.write("\n")
        if self.output_file:
            self.output_file.close()

class Send(Thread):
    def __init__(self, period):
        Thread.__init__(self)
        self.period= period
        self.daemon = True
        self.start()

    def run(self):
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        msg = can.Message(arbitration_id=0x400,
                              data=[2, 0, 0, 0, 0, 0, 0, 0],
                              extended_id=False)

        DELAY_PERIOD = self.period #the delay period btw sending
        timeLastSend = time.time()
        isRunning = True
        while(isRunning):
            if(time.time() - timeLastSend >= DELAY_PERIOD):
                    #remplir message CAN depuis socket
                try:
                    bus.send(msg)
                    timeLastSend = time.time()
                    #time.sleep(0.02) #Change Delay to balance accuracy/CPU usage
                    print("Message sent on {}".format(bus.channel_info))
                except can.CanError:
                    print("Message NOT sent")

class Receive(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        notifier = can.Notifier(bus, [Receive_listener("../log.txt")])

Send(0.5)
Receive()
while True:
    pass
