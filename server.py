
import tornado.ioloop
import tornado.web
from os.path import dirname, join



import json
import zipfile
import StringIO
from datetime import datetime
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont


#nacteni souboru
soubor = zipfile.ZipFile('logs.dump.zip', 'r')


#class pro objekty do listu
class LogFile:
    def __init__(self, name, date, method, message):
        self.name = name
        self.date = date
        self.method = method
        self.message = message

loglist = []

#pridani dat do seznamu
zipfilelist = soubor.namelist()
for x in zipfilelist:
    myJson = json.loads(soubor.read(x))
    datum = datetime.strptime(myJson[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')
    method = myJson[u'method']
    message = myJson[u'message']
    loglist.append(LogFile(x, datum, method, message))

del zipfilelist

datehistogram = {}
#spocitani jednotlivych datumu
for x in loglist:
    datum = x.date
    #zjednoduseni casu pro porovnani
    datum = datum.replace(second=0, microsecond=0, minute=0)
    if datehistogram.has_key(datum):
        datehistogram[datum] += 1
    else:
        datehistogram[datum] = 1


def imghistogram(width, height, start=datetime.min, end=datetime.max):
    maxcount = 0
    mindate = datetime.max
    maxdate = datetime.min
    for x in datehistogram:
        if (x >= start) and (x <= end):
            maxcount = max(datehistogram[x], maxcount)
            if (mindate > x):
                mindate = x
            if (maxdate < x):
                maxdate = x

#vytvoreni obrazku
    img = Image.new('RGB', (width, height), "white")
    draw = ImageDraw.Draw(img)
    delta = maxdate - mindate
    deltahours = delta.total_seconds() / 3600
#vykresleni usecek v obrazku
    for x in datehistogram:
        if (x >= mindate) and (x <= maxdate):
            lx1 = (((x - mindate).total_seconds() / 3600) * width) / deltahours
            lx2 = ((((x + timedelta(hours=1)) - mindate).total_seconds() / 3600) * width) / deltahours -1
            ly = (datehistogram[x] * height) / maxcount
            draw.rectangle((lx1,height,lx2,height - ly),fill="blue",outline="black")

    return [img, mindate, maxdate, maxcount]

#ramecek obrazku s popisky
def make_nice_histogram_layout(imghistogramreturn, iteration):
    old_image = imghistogramreturn[0]
    min_date = imghistogramreturn[1]
    max_date = imghistogramreturn[2]
    max_count = imghistogramreturn[3]
    x_shift = 100
    corner = 25
    img = Image.new('RGB', (old_image.size[0] + x_shift + corner * 2, old_image.size[1] + corner * 2), "white")
    draw = ImageDraw.Draw(img)
    img.paste(old_image, (x_shift + corner, corner))
    draw.text((x_shift + corner, old_image.size[1] + corner + 3), unicode(min_date), fill="red")
    draw.text((img.size[0] - corner - draw.textsize(unicode(max_date))[0], old_image.size[1] + corner + 3),
              unicode(max_date), fill="red")
    carka = 0
    while (carka < max_count):
        ly = old_image.size[1] + corner - ((carka * old_image.size[1]) / max_count)
        draw.line((x_shift, ly, x_shift + corner, ly), fill="orange")
        draw.text((x_shift - draw.textsize(unicode(carka))[0], ly), unicode(carka), fill="orange")
        carka += iteration
    return img



print "najeto"



class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class SearchHandler(tornado.web.RequestHandler):
    def post(self):
        args = self.request.arguments
        if args.has_key("od")and(args.has_key("do")) :
            od = datetime.strptime(args["od"], '%Y-%m-%d %H:%M:%S,%f')
            do = datetime.strptime(args["do"], '%Y-%m-%d %H:%M:%S,%f')


class HistogramHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.arguments
        if args.has_key("od")and(args.has_key("do")) :

            if args["od"][0]=="":
                od = datetime.min
            else:
                od = datetime.strptime(args["od"][0], '%Y-%m-%d %H:%M:%S')

            if args["do"][0]=="":
                do = datetime.max
            else:
                do = datetime.strptime(args["do"][0], '%Y-%m-%d %H:%M:%S')
            histogram = make_nice_histogram_layout(imghistogram(600,300,od,do),200)
            output = StringIO.StringIO()
            histogram.save(output,'PNG')
            self.write(output.getvalue())


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": join(dirname(__file__),"js")}),
        (r"/search",SearchHandler),
        (r"/histogram", HistogramHandler)
    ])
    app.listen(8885)
    tornado.ioloop.IOLoop.current().start()
