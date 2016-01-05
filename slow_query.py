import os


def directory_check():
    list1 = os.listdir(path='C:/Users/Nick/Dropbox/nick/School/Scripts Log files/Script')
    list2 = []
    for x in list1:
        if x.__contains__("mysql_slow_log") and not x.__contains__("_clean"):
            list2.append(x)
    return list2


def process_files(list):
    y = 0;
    for x in list:
        f = open(x, 'r')
        outfile = open(f.name + "_clean.txt", 'w')
        print("Opschonen File: " + str(y))
        opschonen(striplines(f), outfile)
        y += 1


def striplines(f):
    # stript de regels uit de log file en slaat ze op in de variable table
    table1 = [line.rstrip('\n') for line in f]
    # verwijderd het symbool: #
    table1 = [line.replace("# ", '') for line in table1]
    return table1


def check_len(string, f_out):
    # standaard opmaak bevat 9x '×' zo niet ontbreekt de date en time
    if string.count("×") != 9:
        # voegt voor date en time null waarde in
        string = ("NULL×NULL×" + string)
        f_out.write(string + "\n")
        return
    else:
        f_out.write(string + "\n")
        return
    return


# start de loop op de 3e regel van het bestand
# dit slaat de standaard gegenereerde informatie, over het systeem en logs, over
# for line in table:
def opschonen(table, f_out):
    line_str = ""

    for line in table[3:]:

        # checkt of het de regel bepaalde statements bevat
        if line.__contains__("SELECT") \
                or line.__contains__("UPDATE") \
                or line.__contains__("REPLACE") \
                or line.__contains__("DELETE") \
                or line.__contains__("INSERT"):
            # schrijft de hele regel weg + new line
            line_str = (line_str + line)
            check_len(line_str, f_out)
            line_str = ""
            continue

        # checkt of de regel Query_time: bevat
        elif line.__contains__("Query_time:"):
            # specifieke opmaak
            # input: Query_time: 0.572071  Lock_time: 0.000119 Rows_sent: 19  Rows_examined: 276
            # output: 0.572071×0.000119×19×276
            line = line.replace("Query_time: ", '')
            line = line.replace("  Lock_time: ", "×")
            line = line.replace(" Rows_sent: ", "×")
            line = line.replace("  Rows_examined: ", "×")
            line_str = (line_str + line + "×")
            # f_out.write(line + "×")
            continue

        # checkt of de regel Time: bevat
        elif line.__contains__("Time:"):
            # specifieke opmaak
            # input: Time: 151119  6:30:58
            # output: 151119×6:30:58
            # gewenste output: 19/NOV/2015
            line = line.replace("Time: ", "")
            words = line.split()
            line_str = (line_str + (words[0] + "×" + words[1] + "×"))
            # f_out.write(words[0] + "×" + words[1] + "×")
            continue

        # checkt of de regel User@Host: bevat
        elif line.__contains__("User@Host:"):
            # specifieke opmaak
            # input: User@Host: mygenome[mygenome] @ localhost []
            # output: mygenome[mygenome]×localhost
            line = line.replace("User@Host: ", "")
            line = line.replace(" @ ", '×')
            line = line.replace(" []", '')
            line_str = (line_str + line + "×")
            # f_out.write(line+ "×")
            continue

        # checkt of de regel SET bevat
        elif line.__contains__("SET"):
            # specifieke opmaak
            # input: SET timestamp=1447911058;
            # output 1447911058
            line = line.replace("SET timestamp=", "")
            line = line.replace(';', "")
            line_str = (line_str + line + "×")
            # f_out.write(line + "×")
            continue

        elif line.__contains__("SHOW"):
            line = line.replace(";", "")
            line_str = (line_str + line)
            # f_out.write(line + "\n")
            check_len(line_str, f_out)
            line_str = ""
            continue

        elif line.__contains__("show"):
            line = line.replace(";", "")
            line_str = (line_str + line)
            check_len(line_str, f_out)
            line_str = ""
            # f_out.write(line + "\n")

        elif line.__contains__("administrator command:"):
            line = line.replace(";", "")
            line_str = (line_str + line)
            check_len(line_str, f_out)
            line_str = ""
            # f_out.write(line + "\n")
            continue

        # als er use in de line voorkomt wordt deze overgeslagen
        # use komt niet overal voor
        # de waarden hiervan wordt ook vastgelegd in user@host
        elif line.__contains__("use "):
            pass


process_files(directory_check())
