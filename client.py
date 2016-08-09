from __future__ import print_function
import requests
from PIL import Image
import StringIO
import neco


# TODO

def main():
    od = "2015-01-11 10:10:31"
    do = "2016-01-11 10:10:31"
    args={}
    while (len(args)==0):
        call = raw_input("Prejete hledat podle casoveho obdobi/retezce?: o/r ")
        if call == "o":
            print ("format casu: 2015-01-11 10:10:31")
            od = raw_input("Zadejte od: ")
            do = raw_input("Zadejte do: ")
            args["od"]=od
            args["do"]=do
        elif call == "r":  # Pokud vyhledavam podle vyrazu.
            text = raw_input("Zadejte hledany retezec: ")
            args["pattern"] = text
    args_count = len(args)
    while (len(args) == args_count):
        call = int(raw_input("Histogram po hodinach(1), dnech(2)?: 1/2 "))
        if call==1 or call==2:
            args["hd"] = int(call)
    histogramUrl = "http://localhost:8885/histogram"
    searchUrl = "http://localhost:8885/search"
    showUrl = "http://localhost:8885/show"

    try:
        response = requests.get(histogramUrl, args)  # Prvdepodobne spatna URI, ale neumim s nima moc dobre pracovat.
        image = Image.open(StringIO.StringIO(response.content))
        image.save("histogram.png", "PNG")
        print("histogram ulozen do histogram.png")
        image.show()
    except requests.ConnectionError as error:
        print("Histogram error!")
    search_count = 0
    try:
        search_count = int(requests.get(searchUrl, args).content)
        print("hledani vraci "+str(search_count)+" vysledku")
    except requests.ConnectionError as error:
        print("Search error!")

    if search_count>0 :
        if search_count<=100 :
            # TOOOOOOOOOODOOOOOOOOOOOOOOO

while (1):
    main()
    print()
    print("Nove hledani")