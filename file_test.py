import zipfile
import json
from datetime import datetime
soubor=zipfile.ZipFile('logs.dump.zip','r')
seznamSouboru=soubor.namelist()
JsonSoubor=soubor.open('0/00/000/00001.json','r')
datum=datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')


print datum


nasJson=json.loads(soubor.read('0/00/000/00001.json'))
date_object = datetime.strptime(nasJson[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')

datum=datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')
datum2=datetime.strptime(json.loads(soubor.read('0/00/000/00002.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')


print datum2>datum



