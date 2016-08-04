import tornado.web
from os.path import dirname, join
import StringIO
from datetime import datetime

import neco

# nacteni souboru

date_format = '%Y-%m-%d %H:%M:%S'
filename = 'logs.dump.zip'
log_list = neco.load_logs(filename)
last_search = []
PAGE_STEP = 100

print "Json loaded..."


# Handlery
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.arguments
        selected_log_list = []
        # vyhledani podle datumu
        if args.has_key("od") and (args.has_key("do")):
            if args["od"][0] == "":
                start = datetime.min
            else:
                start = datetime.strptime(args["od"][0], date_format)

            if args["do"][0] == "":
                end = datetime.max
            else:
                end = datetime.strptime(args["do"][0], date_format)
            selected_log_list = neco.select_by_date(log_list, start, end)
        # vyhledani podle textu
        if args.has_key("pattern"):
            pattern = args["pattern"][0]
            selected_log_list = neco.select_by_text(log_list, pattern)

        global last_search
        last_search = selected_log_list
        self.write(str(len(selected_log_list)))


class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.arguments
        offset = 0
        if args.has_key("offset"):
            offset = int(args["offset"][0])

        json_result = neco.log_list_to_json(neco.select_by_range(last_search, offset, offset + PAGE_STEP))
        self.write(json_result)


# handler pro histogram
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
                start = datetime.strptime(args["od"][0], date_format)

            if args["do"][0] == "":
                end = datetime.max
            else:
                end = datetime.strptime(args["do"][0], date_format)
            histogram = neco.make_nice_histogram_layout(
                neco.imghistogram(600, 300, neco.select_by_date(log_list, start, end), hourly_daily))
        if args.has_key("pattern"):
            pattern = args["pattern"][0]
            #vytvoreni obrazku
            histogram = neco.make_nice_histogram_layout(
                neco.imghistogram(600, 300, neco.select_by_text(log_list, pattern), hourly_daily))
        output = StringIO.StringIO()
        histogram.save(output, 'PNG')
        self.write(output.getvalue())


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": join(dirname(__file__), "js")}),
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
        (r"/search", SearchHandler),
        (r"/show", ShowHandler),
        (r"/histogram", HistogramHandler)
    ])
    app.listen(8885)
    print ("Server Loaded...")
    tornado.ioloop.IOLoop.current().start()
