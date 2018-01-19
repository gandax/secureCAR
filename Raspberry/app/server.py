import tornado.ioloop
import tornado.web
import os.path
import socket
import time
import json

connection_to_server = 0
connection_client_can = None
connection_can = None
connection_client_model = None
connection_model = None
oldTheta = 0
oldGyroscope = 0



# Afficher index.html quand on se connecte au serveur
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class DataHandler(tornado.web.RequestHandler):
    #Fonction declencher quand le client demande les informations venant de la voiture
	def get(self):
		if(self!=None):
			global connection_client_can
			global connection_client_model
			global oldTheta
			global oldGyroscope
	        found = False
	        nb = 0
	        potentiometer = ""
	        left_odo = ""
	        right_odo = ""
	        x = ""
	        y = ""
	        theta = ""
	        gyroscope = ""
	        gap = ""
	        json_data = None
            
            # Lecture des donnees venant du CAN
	        if(connection_client_can!=None):
			  msg = b""
			  msg = connection_client_can.recv(1024)
			  if(msg != ""):
			      string = msg.decode()
			      # Parsage des donnees presentes sur le socket
			      i = len(string)-2
			      while(not(found)):
		                if(nb==0):
                			        if(string[i]!='#'):
							gyroscope=string[i]+gyroscope
						else:
							nb+=1
			      	elif(nb==1):
			      		if(string[i]!='#'):
			      			potentiometer=string[i]+potentiometer
			      		else:
			      			nb+=1
			      	elif(nb==2):
			      		if(string[i]!='#'):
			      			right_odo=string[i]+right_odo
			      		else:
			      			nb+=1
				elif(nb==3):
			      		if(string[i]!='#'):
			      			left_odo=string[i]+left_odo
			      		else:
			      			found=True
			      	i-=1
			      data = {}
			      data['left'] = left_odo
			      data['right'] = right_odo
			      data['potentiometer'] = potentiometer
			      data['gyroscope'] = gyroscope
			      delta_gyro = (float(gyroscope) - float(oldGyroscope))
			      oldGyroscope = gyroscope				  
			      # Lecture des donnees venant du modele
			      if(connection_client_model!=None):
			          msg = b""
			          msg = connection_client_model.recv(1024)
			          if(msg != ""):
			          	string = msg.decode()
                                        # Parsage des donnees
			          	found = False
			          	nb = 0
			          	i = len(string)-2
			          	while(not(found)):
                          			if(nb==0):
                            				if(string[i]=='#'):
                              					nb+=1
                          			elif(nb==1):
                            				if(string[i]!='#'):
                              					theta = string[i] + theta
                            				else:
                              					nb+=1
                          			elif(nb==2):
                            				if(string[i]!='#'):
                              					y = string[i] + y
                            				else:
                               					nb+=1
                          			elif(nb==3):
                           				if(string[i] != '#'):
                              					x = string[i]+x
                            				else:
                              					found = True
                          			i -= 1
			          	data['x'] = x
			          	data['y'] = y
			          	data['theta'] = theta
					delta_model = (float(theta)-float(oldTheta))
					oldTheta = theta
			          	data['gap'] = (delta_gyro - delta_model)/0.5
			      # Envoi des donnees au client au format json                
			      json_data = json.dumps(data)
                #print(json_data)
	        self.write(json_data)		      

	# Fonction declenchee quand le client envoie les commandes            
	def post(self):
		recordCommands(tornado.escape.json_decode(self.request.body));
		self.write("");

# Initialisation du serveur        
def make_app():
	settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
	)
	return tornado.web.Application([
		(r"/", MainHandler),
		(r"/data", DataHandler)
	], **settings
	)

# Creation des serveurs pour lire les donnees venant du CAN et du modele
def createServerSocket():
	global connection_can
	global connection_client_can
	global connection_model
	global connection_client_model
    
    # Serveur pour le CAN
	server_can_address = "/tmp/data_server"
	try:
	   os.unlink(server_can_address)
	except OSError:
	   if os.path.exists(server_can_address):
	       raise
	connection_can = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	connection_can.bind(server_can_address)
	connection_can.listen(1)
	connection_client_can, data_connection = connection_can.accept()
	connection_client_can.setblocking(False)
    
    # Serveur pour le modele
	server_model_address = "/tmp/output_model"
	try:
	   os.unlink(server_model_address)
	except OSError:
	   if os.path.exists(server_model_address):
	       raise
	connection_model = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	connection_model.bind(server_model_address)
	connection_model.listen(1)
	connection_client_model, data_connection = connection_model.accept()
	connection_client_model.setblocking(False)


# Fonction pour se connecter au serveur du socket pour le CAN    
def connectSocket():
	global connection_to_server
	server_address = "/tmp/command"
	connection_to_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	connection_to_server.connect(server_address)
	print("Connection to CAN process")

# Envoi des donnees (commandes) au thread gerant le CAN via le socket    
def recordCommands(data):
	global connection_to_server
	print(data)
	msg = str(data['motors'])+"#"+str(data['direction'])
	bytes_msg = msg.encode()
	connection_to_server.send(bytes_msg)

if __name__ == "__main__":
	connectSocket()
	createServerSocket()
	msg = "0#15"
	connection_to_server.send(msg.encode())
	try:
	   app = make_app()
	   app.listen(8080)
	   tornado.ioloop.IOLoop.current().start()
	except KeyboardInterrupt:
	   print("Stop")
	   connection_to_server.close()
	   connection_client.close()
	   connection.close()
