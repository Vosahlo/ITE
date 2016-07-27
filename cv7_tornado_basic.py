import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        with codecs.open('index.html','r', 'utf8') as fr:
            self.write(fr.read())  

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
    ])
    app.listen(8885)
    tornado.ioloop.IOLoop.current().start()
