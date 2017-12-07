import modelestep
import os
import sys
from threading import Thread
import time

class runModel(Thread):
       
    
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
    
        old_x = 0
        old_y = 0
        old_theta = 0
        old_data = "0#0#134#"
    
        Te = 0.050 
        Rroue = 0.195/2 
        L = 0.57
        
        DELAY_PERIOD = 0.05
        
        timeLastSend = time.time()
        isRunning = True
        
        connection_client = createServer()
        
        while(isRunning):
            if(time.time() - timeLastSend >= DELAY_PERIOD):
                msg = b""
                msg = connection_client.recv(1024)
                if(msg != ""):
                    string = msg.decode() 
                    current_data = parse(string)
                    phi1mes = current_data[0]-old_data[0]
                    phi2mes = current_data[1]-old_data[1]
                    alpha = current_data[2]-old_data[2]
                    output = modelestep(phi1mes,phi2mes,alpha,old_x,old_y,old_theta,Rroue,L,Te)
                    old_x = output[0]
                    old_y = output[1]
                    old_theta = output[2]
                    old_data = current_data
                    print(output)
                    timeLastSend = time.time()
        
    def parse(string):
        found = False
        data = []
        for i in range(3):
            data[i]=""
        i = len(string)-2
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
    
    def createServer():
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