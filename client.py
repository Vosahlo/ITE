from __future__ import print_function
import requests
from PIL import Image
import StringIO
import neco
#TODO

def main():
    od= "2015-01-11 10:10:31"
    do= "2016-01-11 10:10:31"

    call = raw_input("Prejete hledat podle casoveho obdobi/retezce?: co/r ")
    if call=="co": #Pokud chci vyhledavat podle casu.
        od= raw_input("Zadejte od: ")
        do= raw_input("Zadejte do: ")

        startUri= "http://localhost:8885/histogram"
        try:
            post.requests(startUri,{"od":od,"do":do,"hd":2}) #Prvděpodobně špatná URI, ale neumím s nima moc dobře pracovat.
            image= Image.opne(StringIO.StringIO(response.content))
            image.save("hist_cas.png","PNG")

            img= Image.open('hist_cas.png')
            img.show()

        except Exception as error:
            print("URI error Img!")
    elif call=="r": #Pokud vyhledavam podle vyrazu.
        text= raw_input("Zadejte hledany retezec: ")

        try:
            #-----------Prvni verze-------------------------

            startUri= "http://localhost:8885/search" #Neznam URI vyhledavani, protoze se to pise primo do stranky...
            post.requests(startUri,{xxxx}) #nevim co tam, ale byla by to jednoduzsi verze

            #Pote to nějak zobrazit...
            #-----------------------------------------------


            #-----------Druhá verze-------------------------
            #Nevím jestli je korektní, nezískávám data ze serveru...
            search_list= []
            final= []
            json_file= ""
            count=10

            search_list= neco.load_logs(logs.dump.zip)
            final= neco.select_by_text(search_list,text)
            json_file= neco.log_list_to_json(final)

            print(json_file) #Špatný druh výpisu.... musí se vyřešit jestli použít nějakou již napsanou metodu nebo knihovnu.





            #-----------------------------------------------
