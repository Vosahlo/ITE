import json
import zipfile
from datetime import datetime
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont

soubor = zipfile.ZipFile('logs.dump.zip', 'r')
seznamSouboru = soubor.namelist()
JsonSoubor = soubor.open('0/00/000/00001.json', 'r')
# formatovani data a casu
method = datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')
# print datum

nasJson = json.loads(soubor.read('0/00/000/00001.json'))
date_object = datetime.strptime(nasJson[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')


# datum = datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')
# datum2 = datetime.strptime(json.loads(soubor.read('0/00/000/00002.json'))[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')

# class pro objekty do listu
class LogFile:
    def __init__(self, name, method):
        self.method = method
loglist = []
zipfilelist = soubor.namelist()
for x in zipfilelist:
    myJson = json.loads(soubor.read(x))
    method = myJson['method']
    loglist.append(LogFile(x, method))
del zipfilelist
SeznamMetod = {}
# spocitani jednotlivych datumu
for x in loglist:
    method=x.method
    if SeznamMetod.has_key(method):
        SeznamMetod[method] += 1
    else:
        SeznamMetod[method] = 1
for x in SeznamMetod:
    print(x)
