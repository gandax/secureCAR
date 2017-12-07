import tornado.ioloop
import tornado.web
import os.path
import socket
import time
import json

connection_to_server = 0
connection_client = None
connection = None

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class DataHandler(tornado.web.RequestHandler):
	def get(self):
		if(self!=None):
			global connection_client
	        found = False
	        nb = 0
	        potentiometer = ""
	        left_odo = ""
	        right_odo = ""
	        json_data = None
	        if(connection_client!=None):
			  msg = b""
			  msg = connection_client.recv(1024)
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
	global connection
	global connection_client
    server_address = "/tmp/data_server"
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

