import tornado.ioloop
import tornado.web
from os.path import dirname, join

import json
import zipfile
import StringIO
from datetime import datetime
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
import neco

# nacteni souboru

dateformat = '%Y-%m-%d %H:%M:%S'
filename = 'logs.dump.zip'
log_list = neco.load_logs(filename)

print "Json loaded..."


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.arguments
        selected_log_list = []
        if args.has_key("od") and (args.has_key("do")):
            if args["od"][0] == "":
                start = datetime.min
            else:
                start = datetime.strptime(args["od"][0], dateformat)

            if args["do"][0] == "":
                end = datetime.max
            else:
                end = datetime.strptime(args["do"][0], dateformat)
            selected_log_list = neco.select_by_date(log_list,start,end)
        if args.has_key("pattern"):
            pattern = args["pattern"][0]
            selected_log_list = neco.select_by_text(log_list, pattern)

        self.write(str(len(selected_log_list)))


class HistogramHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.arguments
        histogram = None
        hourly_daily = neco.daily
        if args.has_key("hd"):
            hourly_daily = int(args["hd"][0])

        if args.has_key("od") and (args.has_key("do")):

            if args["od"][0] == "":
                start = datetime.min
            else:
                start = datetime.strptime(args["od"][0], dateformat)

            if args["do"][0] == "":
                end = datetime.max
            else:
                end = datetime.strptime(args["do"][0], dateformat)
            histogram = neco.make_nice_histogram_layout(
                neco.imghistogram(600, 300, neco.select_by_date(log_list, start, end), hourly_daily))
        if args.has_key("pattern"):
            pattern = args["pattern"][0]
            histogram = neco.make_nice_histogram_layout(
                neco.imghistogram(600, 300, neco.select_by_text(log_list, pattern), hourly_daily))
        output = StringIO.StringIO()
        histogram.save(output, 'PNG')
        self.write(output.getvalue())


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": join(dirname(__file__), "js")}),
        (r"/search", SearchHandler),
        (r"/histogram", HistogramHandler)
    ])
    app.listen(8885)
    print ("Server Loaded...")
    tornado.ioloop.IOLoop.current().start()
