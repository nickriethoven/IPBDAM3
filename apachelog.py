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
    w[3] = w[3].replace(':', ",", 1)
    w[4] = w[4].replace(']', "", 1)

    # GET /whole_genome/view/F2 naar -> GET,whole_genome view F2
    w[6] = w[6].replace('/', "", 1)
    w[6] = w[6].replace('/', " ")
    return w


# functie voor de standaard opmaak van de Apache Log, IP;
# DATE; HTTP request; request; http answer; http awnser size ; browser;
def write_format_standard(w, outfile):
    # IP
    outfile.write(w[0] + ',')
    # Date + timezone
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
    if len(w) <= 12:
        write_format_standard(w, outfile)
        outfile.write("\n")
    else:
        write_format_standard(w, outfile)
        # zodra de lengte langer is dan de stadaard
        # dan begint de loop waar de standaard opmaak eindigt, net zo lang als de lijst lang is.
        # dit heeft geen invloed op de lengte van 10 blokken
        for x in w[12:]:
            x = x.replace(',', '')
            outfile.write(x + " ")
        outfile.write("\n")

        # test test
def directory_check():
    list1 = os.listdir(path='C:\Users\Nick\Dropbox\nick\School\Scripts Log files\Script\Dirty\Apache Log')
    list2 = []
    for x in list1:
        if x.__contains__("apache_access_log") and not x.__contains__("_clean"):
            list2.append(x)
    return list2


def process_files(list):
    y = 0;
    for x in list:
        f = open(x, 'r')
        outfile = open(f.name + "_clean.txt", 'w')
        for line in f:
            # woorden opsplitsen
            words = line.split()
            # wegschrijven van de woorden
            print("Opschonen Apache Log File: " + str(y))
            write_format(words, outfile)
            y += 1


process_files(directory_check())
