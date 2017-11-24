#!python
from __future__ import print_function

import can
import time
from threading import Thread
import socket

motor = 0
direction = 0

connection_client=0
connection_to_server=0

g_file=None


class Receive_listener(can.Listener):
    """
    The Printer class is a subclass of :class:`~can.Listener` which simply prints
    any messages it receives to the terminal.

    :param output_file: An optional file to "print" to.
    """

    def __init__(self, output_file=None):
        global g_file
        if output_file is not None:
            #log.info("Creating log file '{}' ".format(output_file))
            output_file = open(output_file, 'wt')
        self.output_file = output_file
        g_file=output_file

    def on_message_received(self, msg):
        global connection_to_server
        if self.output_file is not None:
            if(msg.arbitration_id==10):
                self.output_file.write(str(msg) + "\n")
                msg_socket = str(msg.data[0]) # +'#'str(msg.data[1])+'#'+str(msg.data[2])
                bytes_msg = msg_socket.encode()
                connection_to_server.send(bytes_msg)
        else:
            print(msg)

    def __del__(self):
        #bug fix : never close file ??
        print("Del")
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
        global connection_client
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        can_msg = can.Message(arbitration_id=0x16,
                              data=[0, 0],
                              extended_id=False)

        DELAY_PERIOD = self.period #the delay period btw sending
        timeLastSend = time.time()
        isRunning = True
        while(isRunning):
            if(time.time() - timeLastSend >= DELAY_PERIOD):
                msg = b""
                try:
                    msg = connection_client.recv(1024)
                    if(msg != ""):
                        string = msg.decode()
                        motor = string[0]
                        string_direction = ""
                        for i in range(2,4):
                            string_direction += string[i]
                        direction = string_direction
                        can_msg.data[0]=int(motor)
                        can_msg.data[1]=int(direction)
                except BlockingIOError:
                    pass

                try:
                    bus.send(can_msg)
                    timeLastSend = time.time()
                    #time.sleep(0.02) #Change Delay to balance accuracy/CPU usage
                    #print("Message sent on {}".format(bus.channel_info))
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

def createServer():
    global connection_client
    global connection
    host = ''
    port = 12800
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((host, port))
    connection.listen(1)
    connection_client, data_connection = connection.accept()
    connection_client.setblocking(False)

def connectServer():
    global connection_to_server
    host = "localhost"
    port = 12801
    connection_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_to_server.connect((host, port))
    print("Connection to web server process")


createServer()
connectServer()
Send(0.05)
Receive()
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stop")
    connection_client.close()
    connection.close()
    g_file.close()
