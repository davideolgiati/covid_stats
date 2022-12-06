# Davide Olgiati 14/03/2020
import http.client
import json
import datetime
from datetime import date
import sys

def compute_perc(new, old, Perc):
    diff = new - old
    if Perc:
        Negative = False

        if diff < 0:
            diff *= -1
            Negative = True

        if old > 0:
            perc = diff * 100 / old
        else:
            perc = 100

        tab = "\t\t"
        if perc > 999:
            tab = "\t"

        str_perc = str(round(perc, 1))

        if Negative:
            str_perc = '-' + str_perc + '%' + tab
        else:
            str_perc = '+' + str_perc + '%' + tab
    else:
        str_perc = str(diff) + "\t\t"

    return str_perc

def print_info(desc, json, entry, regione, stats, Perc):
    regioni = [
        4356406, 125666, 10060574, 118714,
        4905854, 1215220, 1550640, 4459477,
        3729641, 882015, 1525271, 5879082,
        1311580, 305617, 5801692, 4029053,
        562869, 1947131, 4999891, 1639591
    ]

    today = json[entry]
    yesterday = stats[regione]['yesterday'][entry]
    day3 = stats[regione]['day3'][entry]
    day4 = stats[regione]['day4'][entry]

    yperc = compute_perc(today, yesterday, Perc)
    perc3 = compute_perc(today, day3, Perc)
    perc4 = compute_perc(today, day4, Perc)

    print('\t ' + desc +
          str(json[entry]) +
          "\t\t" +
          str(round((json[entry] * 100 ) / regioni[regione - 1], 3))
          + "%\t\t" + yperc
          + perc3
          + perc4)


def banner():
    with open("resources/banner.txt", "r") as fp:
        print("\n".join(fp.readlines()))


def main(Input = "", Perc=True):
    baseURL = "raw.githubusercontent.com"
    page = "/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    conn = http.client.HTTPSConnection(baseURL)
    conn.request("GET", page)
    r1 = conn.getresponse()
    data1 = r1.read()
    data = json.loads(data1)
    today = date.today()
    if datetime.datetime.now().hour < 19:
        today = today - datetime.timedelta(days=1)
    yesterday = today - datetime.timedelta(days=1)
    day3 = today - datetime.timedelta(days=2)
    day4 = today - datetime.timedelta(days=3)
    d1 = today.strftime("%Y-%m-%d")
    d2 = yesterday.strftime("%Y-%m-%d")
    d3 = day3.strftime("%Y-%m-%d")
    d4 = day4.strftime("%Y-%m-%d")
    stats = {}
    print("Regione\t\t\t\t\t\tOggi\t\tIeri\t\t-2 giorni\t-3 giorni")
    for entry in data:
        if d1 in entry['data']:
            if Input.lower() in entry['denominazione_regione'].lower() or Input == "":
                print(entry['denominazione_regione'])
                print_info("Totale Ospedalizzati   : ",
                           entry,
                           'totale_ospedalizzati',
                           entry['codice_regione'],
                           stats, Perc)
                print_info("Ricoverati con sintomi : ",
                           entry,
                           'ricoverati_con_sintomi',
                           entry['codice_regione'],
                           stats, Perc)
                print_info("Terapia intensiava     : ",
                           entry,
                           'terapia_intensiva',
                           entry['codice_regione'],
                           stats, Perc)
                print_info("Isolamento Domiciliare : ",
                           entry,
                           'isolamento_domiciliare',
                           entry['codice_regione'],
                           stats, Perc)
                print_info("Totale Positivi        : ",
                           entry,
                           'totale_attualmente_positivi',
                           entry['codice_regione'],
                           stats, Perc)
                print_info("Nuovi Positivi         : ",
                           entry,
                           'nuovi_attualmente_positivi',
                           entry['codice_regione'],
                           stats, Perc)
                print_info("Dimessi                : ",
                           entry,
                           'dimessi_guariti',
                           entry['codice_regione'],
                           stats, Perc)
                print_info("Deceduti               : ",
                           entry,
                           'deceduti',
                           entry['codice_regione'],
                           stats, Perc)
                print_info("Totale Casi            : ",
                           entry,
                           'totale_casi',
                           entry['codice_regione'],
                           stats, Perc)
                print("\n")
        elif d2 in entry['data']:
            stats[entry['codice_regione']]['yesterday'] = entry
        elif d3 in entry['data']:
            stats[entry['codice_regione']]['day3'] = entry
        elif d4 in entry['data']:
            stats[entry['codice_regione']] = {}
            stats[entry['codice_regione']]['day4'] = entry
            #print(stats)

    conn.close()

def parse_argv(input):
    val = ["", True]
    for arg in input:
        if arg == "-f":
            val[1] = False
        else:
            val[0] = arg

    return val

if __name__ == "__main__":
    banner()
    if len(sys.argv) > 1:
        val = parse_argv(sys.argv)
        main(val[0], val[1])
    else:
        main("")
