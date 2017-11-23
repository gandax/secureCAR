import tornado.ioloop
import tornado.web
import os.path
import socket
import time

connection_to_server = 0

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")
	
class DataHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("get data")
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

def connectSocket():
	global connection_to_server
	host = "localhost"
	port = 12800
	connection_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection_to_server.connect((host, port))
	print("Connection to CAN process")

def recordCommands(data):
	global connection_to_server
	print(data)
	msg = str(data['motors'])+"#"+str(data['direction'])
	bytes_msg = msg.encode()
	connection_to_server.send(bytes_msg)

if __name__ == "__main__":
	app = make_app()
	app.listen(8080)
	connectSocket()
	msg = "0#24"
	connection_to_server.send(msg.encode())
	tornado.ioloop.IOLoop.current().start()

