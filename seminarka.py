import zipfile
import os
import json
from datetime import datetime
soubor=zipfile.ZipFile('C:\Users\milan\ITE\logs.dump.zip','r')
seznamSouboru=soubor.namelist()
JsonSoubor=soubor.open('0/00/000/00001.json','r')
#nasJson=json.loads(soubor.read('0/00/000/00001.json'))
datum=datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')

#vedlejsi
nasJson[u'asctime']
from datetime import datetime
date_object = datetime.strptime(nasJson[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')
datum=datetime.strptime(json.loads(soubor.read('0/00/000/00001.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')
datum2=datetime.strptime(json.loads(soubor.read('0/00/000/00002.json'))[u'asctime'],'%Y-%m-%d %H:%M:%S,%f')
datum2>datum