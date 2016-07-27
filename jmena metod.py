import json
import zipfile

soubor = zipfile.ZipFile('logs.dump.zip', 'r')

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
