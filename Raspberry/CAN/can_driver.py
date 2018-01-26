#!python
from __future__ import print_function

import can
import time
from threading import Thread
import socket
import os
import thread_model

# Variables pour savoir dans quel sens vont les moteurs (0 = arret, 1 = marche arriere et 2 = marche avant)
state_motor = 0
speed_command = 0
# Commande sur le volant
direction = 0
# Valeur pour le calcul de la pente en acceleration
slope_up = 2
# Valeur pour le calcul de la pente en deceleration
slope_down =10

max_speed=100

connection_client=None
connection_to_server_server=None
connection_to_server_model=None

g_file=None
gyro_file=None

lastState = 0
nb_message = 1


# Classe pour gerer la reception de message sur le CAN
class Receive_listener(can.Listener):

    def __init__(self, output_file=None):
        global path
        global g_file
        global file_gyro
        # Creation d'un fichier pour enregistrer les donnees venant du CAN
        if output_file is not None:
            output_file = open(output_file, 'wt')
        gyro_file = open("../gyro.txt",'wt')
        self.gyro_file = gyro_file
        self.output_file = output_file
        g_file=output_file

    def on_message_received(self, msg):
        global connection_to_server_server
        global connection_to_server_model
        global nb_message
        if self.output_file is not None:
            # si le message vient du stm32
            if(msg.arbitration_id==10):
                # on ecrit dans le fichier
                self.output_file.write(str(msg) + "\n")
                # on ecrit les recupere les donnees du message et on les concatene
                left_odo = msg.data[0] + (msg.data[1]<<8)
                right_odo = msg.data[2] + (msg.data[3]<<8)
                potentiometer = int(int(msg.data[4]-135)*35/48)
                gyroscope = msg.data[6] + (msg.data[7]<<8)
                if(gyroscope > 32767):
                    gyroscope = (65536-gyroscope) * -1
                self.gyro_file.write(str(gyroscope) + "\n")
                msg_socket_server = str(nb_message) + '#' + str(left_odo) +'#' + str(right_odo) +'#'+str(potentiometer)+'#'+str(gyroscope)+'#'
                msg_socket_model = str(nb_message) + '#' + str(left_odo) +'#' + str(right_odo) +'#'+str(potentiometer)+'#'
                nb_message += 1
                bytes_msg_server = msg_socket_server.encode()
                bytes_msg_model = msg_socket_model.encode()
                # On envoie ces donnees au serveur et au modele via des sockets
                if(connection_to_server_server != None):
                    connection_to_server_server.send(bytes_msg_server)
                if(connection_to_server_model != None):
                    connection_to_server_model.send(bytes_msg_model)
        else:
            print(msg)

    def __del__(self):
        self.output_file.write("\n")
        if self.output_file:
            self.output_file.close()

# Classe gerant l'envoi de message sur le CAN            
class Send(Thread):
    def __init__(self, period):
        Thread.__init__(self)
        self.period= period
        self.daemon = True
        self.start()

    def run(self):
        global connection_client
        global state_motor
        global speed_command
        global lastState
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        can_msg = can.Message(arbitration_id=0x14,
                              data=[0, 0, 0],
                              extended_id=False)
        # Valeur de la periode d'envoi des messages
        DELAY_PERIOD = self.period 
        timeLastSend = time.time()
        isRunning = True
        recule=False
        avance=False
        chgt=False
        lastState=0
        direction=0
        state_motor=0
        speed_command=0
        while(isRunning):
            # A chaque periode
            if(time.time() - timeLastSend >= DELAY_PERIOD):
                msg = b""
                try:
                    # Lecture des donnees venant du serveur web via le socket
                    msg = connection_client.recv(1024)
                    if(msg != ""):
                        string = msg.decode()
                        # Parsage des donnees
                        if(len(string)>0):
                            state_motor = string[0]
                            string_direction = ""
                            for i in range(2,4):
                                string_direction += string[i]
                            direction = string_direction
                # si rien sur le socket, on ne fait rien
                except BlockingIOError:
                    pass

                try:
                    # si on ne veut plus avancer
                    if(int(state_motor)==0):
                        # si on avance encore, on decremente jusqu'a attendre une vitesse nulle
                      if(speed_command>slope_down):
                          speed_command-=slope_down
                        # si on a atteint une vitesse nulle, on reinitialise les variables
                      elif(speed_command<=slope_down):
                          recule=False
                          avance=False
                          chgt=False
                          speed_command=0
                          lastState=0                                                
                    else:
                      # Si on veut avancer                        
                      if(int(state_motor)==2):
                          lastState=2                            
                          avance=True
                          # si on reculait => il y a changement de sens  
                          if(recule):
                              chgt=True
                              recule=False
                      # Inversement quand on veut reculer                    
                      else:
                          lastState=1
                          recule=True
                          if(avance):
                              chgt=True
                              avance=False
                      # si pas de changement => on augmente la vitesse tant qu'elle n'a pas atteint le maximum
                      if(not(chgt)):
                          if(speed_command<max_speed):
                              speed_command+=slope_up
                      # sinon => on diminue la vitesse jusqu'a atteindre 0 avant de reprendre un comportement normal
                      else:
                          if(speed_command>slope_down):
                              speed_command-=slope_down                                                        
                          elif(speed_command<=slope_down):
                              chgt=False
                              speed_command=0
                              if(lastState==2):
                                lastState=1
                              elif(lastState==1):
                                lastState=2
                    # envoi des donnees sur le CAN                                
                    can_msg.data[0]=lastState
                    can_msg.data[1]=int(direction)
                    can_msg.data[2]=int(speed_command)
                    bus.send(can_msg)
                    timeLastSend = time.time()
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

# Creation du serveur socket pour que le serveur web puisse envoyer des commandes        
def createServer():
    global connection_client
    global connection
    server_address = "/tmp/command"
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

# Connexion au socket du serveur web pour envoyer les donnees de la voiture    
def connectServerServer():
    global connection_to_server_server
    server_address = "/tmp/data_server"
    connection_to_server_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    connection_to_server_server.connect(server_address)
    print("Connection to web server process")
    
# Connexion au socket du modele pour envoyer les donnees de la voiture      
def connectServerModel():
    global connection_to_server_model
    server_address = "/tmp/data_model"
    connection_to_server_model = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    connection_to_server_model.connect(server_address)

createServer()
time.sleep(0.5)
connectServerServer()
Send(0.05)
Receive()
entries_file = open("../entries.txt", 'wt')
model_output_file = open("../output.txt", 'wt')
thread_model.runModel(entries_file, model_output_file)
time.sleep(0.5)
connectServerModel()
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stop")
    connection_client.close()
    connection.close()
    connection_to_server_server.close()
    connection_to_server_model.close()
    g_file.close()
    gyro_file.close()
    entries_file.close()
    model_output_file.close()
