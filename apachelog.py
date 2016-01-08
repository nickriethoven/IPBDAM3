import os


def format_element(w):
    # counter voor de replacement van aanhalingstekens
    count = 0
    for x in w:
        # verwijderen van aanhalingstekens in de gehele file
        w[count] = x.replace('"', "", 3)
        count += 1

    # Opmaak van bepaalde blokken
    # [30/Nov/2014:06:25:46 +0100] -> 30/Nov/2014,06:25:46
    w[3] = w[3].replace('[', "", 1)
    # 30/Nov/2014:06:25:46 -> 30/Nov/2014,06:25:46
    w[3] = w[3].replace(":", ",", 1)

    # Date van 30/Nov/2014 -> 30/11/2014
    if w[3].__contains__("Jan"):
        w[3] = w[3].replace("Jan", "01", 1)
    elif w[3].__contains__("Feb"):
        w[3] = w[3].replace("Feb", "02", 1)
    elif w[3].__contains__("Mar"):
        w[3] = w[3].replace("Mar", "03", 1)
    elif w[3].__contains__("Apr"):
        w[3] = w[3].replace("Apr", "04", 1)
    elif w[3].__contains__("May"):
        w[3] = w[3].replace("May", "04", 1)
    elif w[3].__contains__("Jun"):
        w[3] = w[3].replace("Jun", "05", 1)
    elif w[3].__contains__("Jun"):
        w[3] = w[3].replace("Jun", "06", 1)
    elif w[3].__contains__("Jul"):
        w[3] = w[3].replace("Jul", "07", 1)
    elif w[3].__contains__("Aug"):
        w[3] = w[3].replace("Aug", "08", 1)
    elif w[3].__contains__("Sep"):
        w[3] = w[3].replace("Sep", "09", 1)
    elif w[3].__contains__("Oct"):
        w[3] = w[3].replace("Oct", "10", 1)
    elif w[3].__contains__("Nov"):
        w[3] = w[3].replace("Nov", "11", 1)
    elif w[3].__contains__("Dec"):
        w[3] = w[3].replace("Dec", "12", 1)
    # +0100] -> +0100
    w[4] = w[4].replace(']', "", 1)

    # GET /whole_genome/view/F2 naar -> GET,whole_genome view F2
    w[6] = w[6].replace('/', "", 1)
    w[6] = w[6].replace('/', " ")
    w[6] = w[6].replace(',', " ")
    # returnen van de opgeschoonde lijst
    return w


# functie voor de standaard opmaak van de Apache Log, IP;
# DATE; HTTP request; request; http answer; http awnser size ; browser;
def write_format_standard(w, outfile):
    # IP
    outfile.write(w[0] + ',')
    # 30/11/2014 + +0100
    outfile.write(w[3] + ',' + w[4] + ',')
    # http request type "GET"/"Post"; request /shared/view/hgdf12; HTTP/1.1
    outfile.write(w[5] + ',' + w[6] + ',' + w[7] + ',')
    # HTTP Answer + HTTP answer size
    outfile.write(w[8] + ',' + w[9] + ',')
    # browser en versie
    outfile.write(w[11] + ',')


def write_format(w, outfile):
    # input is: 66.249.64.4 - - [30/Nov/2014:06:25:46 +0100] "GET /whole_genome/view/F2 HTTP/1.1" 200 293498 "-" "Mozilla/5.0
    # output is: 66.249.64.4,30/Nov/2014,06:25:46,+0100,GET,whole_genome view F2,HTTP/1.1,200,293498,Mozilla/5.0
    format_element(w)
    # als de lengte onder de 12 is dan voldoet de lijst aan de standaard opmaak
    if len(w) == 12:
        write_format_standard(w, outfile)
        outfile.write("\n")
    # Wanneer de lijst kleiner is dan 12 woorden
    elif len(w) < 12:
        write_format_standard(w, outfile)
        # loop die net zolang door met seperators(',') toevoegen tot de lengte 12 is
        while len(w) < 12:
            w.append(",")
        outfile.write("\n")
    # als de lengte groter is dan 12 loopt de code tot er niks meer in de lijst staat
    elif len(w) > 12:
        write_format_standard(w, outfile)
        # zodra de lengte langer is dan de stadaard
        # dan begint de loop waar de standaard opmaak eindigt, net zo lang als de lijst lang is.
        # dit heeft geen invloed op de lengte van 10 blokken
        for x in w[12:]:
            x = x.replace('(', '')
            x = x.replace(')', '')
            x = x.replace(',', '')
            outfile.write(x + " ")
        outfile.write("\n")


# checkt een directory op "apache_access_log" maar zonder "_clean"
def directory_check():
    list1 = os.listdir(path='C:/Users/Nick/Dropbox/nick/School/Scripts Log files/Script')
    list2 = []
    for x in list1:
        if x.__contains__("apache_access_log") and not x.__contains__("_clean"):
            list2.append(x)
    return list2


# processed de gefilterde lijst van logs
def process_files(list):

    y = 0;
    # gaat de hele lijst door en verwerkt de logs stuk voor stuk
    for x in list:
        f = open(x, 'r')
        # open een outfile
        outfile = open(f.name + "_clean.txt", 'w')
        # eerste regel van elk bestand, nodig voor analyse
        outfile.write("IP,Date,Time,Timezone,HTTP Request,Doel Locatie,Protocol,Response,Package size,Browser,Source")
        outfile.write("\n")
        print("Opschonen Apache Log File: " + str(y))
        y += 1

        for line in f:
            # woorden opsplitsen
            words = line.split()
            # wegschrijven van de woorden
            write_format(words, outfile)


process_files(directory_check())
