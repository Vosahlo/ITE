import json
import zipfile
from datetime import datetime
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont


# class pro objekty do listu
class LogFile:
    def __init__(self, name, date, method, message):
        self.name = name
        self.date = date
  #      self.datestring = datestring
        self.method = method
        self.message = message


def load_logs(filename):
    loaded_file = zipfile.ZipFile(filename, 'r')
    zipfilelist = loaded_file.namelist()
    loglist = []
    for x in zipfilelist:
        myJson = json.loads(loaded_file.read(x))
        datum = datetime.strptime(myJson[u'asctime'], '%Y-%m-%d %H:%M:%S,%f')
        method = myJson[u'method']
        message = myJson[u'message']
        loglist.append(LogFile(x, datum, method, message))
    return loglist


def select_by_date(loglist, start=datetime.min, end=datetime.max):
    new_log_list = []
    for x in loglist:
        if (x.date >= start) and (x.date <= end):
            new_log_list.append(x)
    return new_log_list


def select_by_text(log_list, pattern):
    new_log_list = []
    for x in log_list:
        if (x.message.find(pattern) > -1):
            new_log_list.append(x)
    return new_log_list


def select_by_range(log_list, start, end):
    new_log_list = []
    if (len(log_list)<end):
        end = len(log_list) - 1
    for x in range(start,end) :
        new_log_list.append(log_list[x])
    return new_log_list


def log_list_to_json(log_list):
    json_output = "["
    for x in log_list:
        item = "{"\
               "\"name\" : \"" + x.name + "\","\
               "\"date\" : \"" + str(x.date) + "\","\
               "\"method\" : \"" + x.method + "\","\
               "\"message\" : \"" + x.message + "\"}"
        json_output = json_output + item + ","

    json_output = json_output[:-1] + "]"

    return json_output


def get_histogram_hourly(log_list):
    hourly_histogram = {}
    for x in log_list:
        datum = x.date
        datum = datum.replace(second=0, microsecond=0, minute=0)
        if hourly_histogram.has_key(datum):
            hourly_histogram[datum] += 1
        else:
            hourly_histogram[datum] = 1
    return hourly_histogram


def get_histogram_daily(log_list):
    daily_histogram = {}
    for x in log_list:
        datum = x.date
        datum = datum.replace(second=0, microsecond=0, minute=0, hour=0)
        if daily_histogram.has_key(datum):
            daily_histogram[datum] += 1
        else:
            daily_histogram[datum] = 1
    return daily_histogram


hourly = 1
daily = 2


def imghistogram(width, height, loglist, hourly1_daily2=1):
    maxcount = 0
    datehistogram = {}
    if hourly1_daily2 == 1:
        datehistogram = get_histogram_hourly(loglist)
    else:
        datehistogram = get_histogram_daily(loglist)

    mindate = datetime.max
    maxdate = datetime.min
    for x in datehistogram:
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
            lx1 = (((x - mindate).total_seconds() / 3600) * width) / deltahours
            lx2 = ((((x + timedelta(hours=1)) - mindate).total_seconds() / 3600) * width) / deltahours - hourly1_daily2
            if hourly1_daily2 == 2:
                lx2 = ((((x + timedelta(days=1)) - mindate).total_seconds() / 3600) * width) / deltahours - 2
            ly = (datehistogram[x] * height) / maxcount
            draw.rectangle((lx1, height, lx2, height - ly), fill="blue", outline="black")

    return [img, mindate, maxdate, maxcount]


# ramecek obrazku s popisky
def make_nice_histogram_layout(imghistogramreturn):
    old_image = imghistogramreturn[0]
    min_date = imghistogramreturn[1]
    max_date = imghistogramreturn[2]
    max_count = imghistogramreturn[3]

    iteration = 0
    if max_count < 20:
        iteration = 1
    elif max_count < 200:
        iteration = 10
    elif max_count < 2000:
        iteration = 100
    else:
        iteration = 1000

    x_shift = 100
    corner = 25
    img = Image.new('RGB', (old_image.size[0] + x_shift + corner * 2, old_image.size[1] + corner * 2), "white")
    draw = ImageDraw.Draw(img)
    img.paste(old_image, (x_shift + corner, corner))
    draw.text((x_shift + corner, old_image.size[1] + corner + 3), unicode(min_date), fill="red")
    draw.text((img.size[0] - corner - draw.textsize(unicode(max_date))[0], old_image.size[1] + corner + 3),
              unicode(max_date), fill="red")
    carka = 0
    while (carka <= max_count):
        ly = old_image.size[1] + corner - ((carka * old_image.size[1]) / max_count)
        draw.line((x_shift, ly, x_shift + corner, ly), fill="orange")
        draw.text((x_shift - draw.textsize(unicode(carka))[0], ly), unicode(carka), fill="orange")
        carka += iteration
    return img

