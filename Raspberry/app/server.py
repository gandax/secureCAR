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

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class DataHandler(tornado.web.RequestHandler):
	def get(self):
		if(self!=None):
			global connection_client_can
			global connection_client_model
	        found = False
	        nb = 0
	        potentiometer = ""
	        left_odo = ""
	        right_odo = ""
	        x = ""
	        json_data = None
	        if(connection_client_can!=None):
			  msg = b""
			  msg = connection_client_can.recv(1024)
			  if(msg != ""):
			      string = msg.decode()		          	               
			      i = len(string)-2
			      while(not(found)):
			      	if(nb==0):
			      		if(string[i]!='#'):
			      			potentiometer=string[i]+potentiometer
			      		else:
			      			nb+=1
			      	elif(nb==1):
			      		if(string[i]!='#'):
			      			right_odo=string[i]+right_odo
			      		else:
			      			nb+=1
			      	elif(nb==2):
			      		if(i<0):
			      			found=True
			      		elif(string[i]!='#'):
			      			left_odo=string[i]+left_odo
			      		else:
			      			found=True
			      	i-=1
			      data = {}
			      data['left'] = left_odo
			      data['right'] = right_odo
			      data['potentiometer'] = potentiometer
			      if(connection_client_model!=None):
			          msg = b""
			          msg = connection_client_model.recv(1024)
			          if(msg != ""):
			          	string = msg.decode()
			          	found = False
			          	i = len(string)-2
			          	while(not(found)):
			          		if(string[i] != '#'):
			          			x = string[i]+x
			          		else:
			          			found = True
			          		i -= 1
			          	data['x'] = x															
			      json_data = json.dumps(data)
	        self.write(json_data)		      

	def post(self):
		recordCommands(tornado.escape.json_decode(self.request.body));
		self.write("");

def make_app():
	settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
	)
	return tornado.web.Application([
		(r"/", MainHandler),
		(r"/data", DataHandler)
	], **settings
	)

def createServerSocket():
	global connection_can
	global connection_client_can
	global connection_model
	global connection_client_model
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


def connectSocket():
	global connection_to_server
	server_address = "/tmp/command"
	connection_to_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	connection_to_server.connect(server_address)
	print("Connection to CAN process")

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
