import tornado.ioloop
import tornado.web
import os.path



class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

def recordCommands(data):
	print(data)
	
class DataHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("get data")
	def post(self):
		recordCommands(self.request.body);
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

if __name__ == "__main__":
	app = make_app()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
