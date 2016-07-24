import json
import zipfile
from datetime import datetime
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont

# nacteni souboru
soubor = zipfile.ZipFile('logs.dump.zip', 'r')
seznamSouboru = soubor.namelist()
JsonSoubor = soubor.open('0/00/000/00001.json', 'r')
# formatovani data a casu
datum = datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')
# print datum

nasJson = json.loads(soubor.read('0/00/000/00001.json'))
date_object = datetime.strptime(nasJson[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')


# datum = datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')
# datum2 = datetime.strptime(json.loads(soubor.read('0/00/000/00002.json'))[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')

# class pro objekty do listu
class LogFile:
    def __init__(self, name, date, method, message):
        self.name = name
        self.date = date
        self.method = method
        self.message = message


loglist = []

# pridani dat do seznamu
zipfilelist = soubor.namelist()
for x in zipfilelist:
    myJson = json.loads(soubor.read(x))
    datum = datetime.strptime(myJson[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')
    method = myJson[u'method']
    message = myJson[u'message']
    loglist.append(LogFile(x, datum, method, message))

del zipfilelist

# print loglist[3].name
# print loglist[3].date
# print loglist[3].method
# print loglist[3].message

datehistogram = {}
# spocitani jednotlivych datumu
for x in loglist:
    datum = x.date
    # zjednoduseni casu pro porovnani
    datum = datum.replace(second=0, microsecond=0, minute=0, hour=0)
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

                # vytvoreni obrazku
    img = Image.new('RGB', (width, height), "white")
    draw = ImageDraw.Draw(img)
    delta = maxdate - mindate
    deltahours = delta.total_seconds() / 3600
    # vykresleni usecek v obrazku
    for x in datehistogram:
        if (x >= mindate) and (x <= maxdate):
            lx = (((x - mindate).total_seconds() / 3600) * width) / deltahours
            ly = (datehistogram[x] * height) / maxcount
            draw.line((lx, height, lx, height - ly), fill="black")

    return [img, mindate, maxdate, maxcount]


# ramecek obrazku s popisky
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


image = make_nice_histogram_layout(imghistogram(1000, 500), 1000)
# image.show()
image.save("histogram.jpg", format=None)
