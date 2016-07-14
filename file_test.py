import json
import zipfile
from datetime import datetime

#import Image, ImageDraw



soubor=zipfile.ZipFile('logs.dump.zip','r')
seznamSouboru=soubor.namelist()
JsonSoubor=soubor.open('0/00/000/00001.json','r')
datum=datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')


print datum


nasJson=json.loads(soubor.read('0/00/000/00001.json'))
date_object = datetime.strptime(nasJson[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')

datum=datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')
datum2=datetime.strptime(json.loads(soubor.read('0/00/000/00002.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')



class LogFile:
    def __init__(self, name, date, method, message) :
        self.name = name
        self.date = date
        self.method = method
        self.message = message


loglist = []


zipfilelist = soubor.namelist()
for x in zipfilelist :
    myJson = json.loads(soubor.read(x))
    datum =  datetime.strptime(myJson[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')
    method=myJson[u'method']
    message = myJson[u'message']
    loglist.append(LogFile(x, datum,method,message))

del zipfilelist


print loglist[3].name
print loglist[3].date
print loglist[3].method
print loglist[3].message


datehistogram = {}
for x in loglist :
    datum = x.date
    datum = datum.replace(second=0, microsecond=0 , minute = 0)
    if datehistogram.has_key(datum):
        datehistogram[datum] = datehistogram[datum] + 1
    else:
        datehistogram[datum] = 1






