import modelestep
import os
import sys
import socket
from threading import Thread
import time

class runModel(Thread):
       
    
    def __init__(self, entry_file, output_file):
        Thread.__init__(self)
        self.daemon = True
        self.entry_file = entry_file
        self.output_file = output_file
        self.start()
        
    def parse(self, string):
        found = False
        data = ["","",""]
        i = len(string)-2
        nb=0
        while(not(found)):
            if(nb==0):
                if(string[i]!='#'):
                    data[2]=string[i]+data[2]
                else:
                    nb+=1
            elif(nb==1):
                if(string[i]!='#'):
                    data[1]=string[i]+data[1]
                else:
                    nb+=1
            elif(nb==2):
                if(i<0):
                    found=True
                elif(string[i]!='#'):
                    data[0]=string[i]+data[0]
                else:
                    found=True
            i-=1
        return data
    
    def createServer(self):
        server_address = "/tmp/data_model"
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise
        connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        connection.bind(server_address)
        connection.listen(1)
        connection_client, data_connection = connection.accept()
        connection_client.setblocking(False)
        return connection_client

    def run(self):
    
        old_x = 0
        old_y = 0
        old_theta = 0
        old_data = self.parse("0#0#134#")
    
        Te = 0.050 
        Rroue = 0.195/2 
        L = 0.57
        
        DELAY_PERIOD = 0.05
        
        timeLastSend = time.time()
        isRunning = True
        
        connection_client = self.createServer()
        
        while(isRunning):
            if(time.time() - timeLastSend >= DELAY_PERIOD):
                msg = b""
                try:
                    msg = connection_client.recv(1024)
                    if(msg != ""):
                        string = msg.decode() 
                        current_data = self.parse(string)
                        if(int(current_data[0])-int(old_data[0])<0):
                            phi1mes = 360 - int(old_data[0]) + int(current_data[0])
                        else:
                            phi1mes = int(current_data[0])-int(old_data[0])
                        if(int(current_data[1])-int(old_data[1])<0):
                            phi2mes = 360 - int(old_data[1]) + int(current_data[1])
                        else:
                            phi2mes = int(current_data[1])-int(old_data[1])
                        alpha = int(current_data[2])
                        self.entry_file.write(str(phi1mes) + "#" + str(phi2mes) + "#" + str(alpha) + "#" + str(old_x) + "#" + str(old_y) + "#" + str(old_theta) + "#" + str(Rroue) + "#" + str(L)+ "#" + str(Te)+"#\n")
                        output = modelestep.modelestep(phi1mes,phi2mes,alpha,old_x,old_y,old_theta,Rroue,L,Te)
                        self.output_file.write(str(output[0])+ "#" + str(output[1])+ "#" +str(output[2])+"#\n")
                        old_x = output[0]
                        old_y = output[1]
                        old_theta = output[2]
                        old_data = current_data
                        print(output)
                        timeLastSend = time.time()
                except BlockingIOError:
                    pass
        
    