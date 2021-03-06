#!/usr/bin/env python3

#   Python 3 Library modules
import argparse
import os
import sys

<<<<<<< HEAD
from resources import fileprocessing
from resources.commerciallDBs import db_ip, eurek, ip2location, geobytes, ipinfo, maxmind, skyhook
from resources.commerciallDBs import neustar
from resources.nonCommerciallDbs import freegeoip, ip2locdb11lite
from resources.nonCommerciallDbs import maxmindgeolite2city
=======
import mapgenerator

import fileprocessing
from commerciallDBs import db_ip, eurek, ip2location, geobytes, ipinfo, neustar, maxmind, skyhook
from nonCommerciallDbs import maxmindgeolite2city, freegeoip, ip2City, ip2locdb11lite
>>>>>>> parent of 82047a2... folium map generation fully implemented +  some minor code changes and reformatting

__author__ = "Frantisek Farkas"

delimiter = "\t"

if sys.version_info.major != 3:
    print("ERROR: Run this script with Python 3.5!", file=sys.stderr)
    sys.exit(1)

parser = argparse.ArgumentParser(usage="""
python3 geolocator.py FILE [-h] [-v] -i {tab,space} -o {tab,space} -c {file} -r {file} -d {all,DB-IP,MaxMind,IPInfo,
IP2Location,Skyhook,Neustar,Geobytes,Freegeoip, Maxmindgeolite2city, Ip2locdb11lite}

examples:
python3 main.py input.dat -d IPInfo -v -i tab -o space
python3 main.py -d MaxMind -v -i tab input.dat
python3 main.py -d DB-IP -i tab -v -o space input.dat

#dalsie DBs

Databases & Links:
  IPInfo                    http://www.iplocation.net/ (2nd table records "ipInfo.io")
  MaxMind                   http://www.maxmind.com/en/home
  DB-IP                     http://db-ip.com/
  IP2Location               http://www.ip2location.com/demo
  Skyhook                   https://context.skyhookwireless.com
  Neustar                   http://www.neustar.biz/services
  Geobytes                  http://www.geobytes.com/IpLocator.htm?GetLocation
  Eurek                     REGISTRATION REQUIRED ! Fill the KEY string in source file at the begining.
                            https://www.eurekapi.com

                            Eurek key section in source file ...

                            ############### KEY ###########################
                            key = 'SAK535233J496335F36Z'        #AUTH KEY!#
                            ###############################################

  maxmindgeolite2city       http://www.maxmind.com/en/home
  Freegeoip                 http://freegeoip.net/
  Ip2locdb11lite            http://lite.ip2location.com/
""")
parser.add_argument("FILE", help="Input File")
parser.add_argument("-d", help='Geolocation Database to be used', dest='database', required=True, choices=['all',
                                                                                                           'DB-IP',
                                                                                                           'MaxMind',
                                                                                                           'IPInfo',
                                                                                                           'IP2Location',
                                                                                                           'Skyhook',
                                                                                                           'Neustar',
                                                                                                           'Geobytes',
                                                                                                           'Eurek',
                                                                                                           # 'Ip2City',
                                                                                                           'Maxmindgeolite2city',
                                                                                                           'Freegeoip',
                                                                                                           'Ip2locdb11lite',
                                                                                                           # 'hostIP'
                                                                                                           ])

parser.add_argument("-i", help='Input File Records Delimiter', default='tab', dest='input_separator',
                    choices=['tab', 'space'])
parser.add_argument("-o", help='Output File Records Delimiter', default='tab', dest='output_separator',
                    choices=['tab', 'space'])
parser.add_argument("-v", help='Increase Output Verbosity', dest='verbose', action='store_true')
parser.add_argument("-c", help='Cut words in specified file', dest='cut', default='')
parser.add_argument("-r", help='Replace words in specified file', dest='replace', default='')

arguments = parser.parse_args()

# Databases modules Dictonary
databases = dict()
databases["DB-IP"] = db_ip
databases["MaxMind"] = maxmind
databases["IP2Location"] = ip2location
databases["Neustar"] = neustar
databases["Geobytes"] = geobytes
databases["Skyhook"] = skyhook
databases["IPInfo"] = ipinfo
databases["Eurek"] = eurek
databases["Ip2locdb11lite"] = ip2locdb11lite
# databases["ip2City"] = ip2City
databases["Maxmindgeolite2city"] = maxmindgeolite2city
databases["Freegeoip"] = freegeoip
# databases["hostIP"] = hostIp

# Database or ALL Databases will be used

if arguments.verbose:
    print("Input file to be used:", arguments.FILE)
    print("Databases to be used:", arguments.database)
    print("Input file record delimiter:", arguments.input_separator)
    print("Output file record delimiter:", arguments.output_separator)
    print("File used for cutting:", arguments.cut)
    print("File used for replacement:", arguments.replace)

# Preparing Results Directory

path = "./results"

try:
    if not os.path.exists(path):
        os.makedirs(path)
except OSError as error:
    print(error)


# Definition of Main Processing
def main():
<<<<<<< HEAD
    # ip_records = fileprocessing.get_ip_records(arguments.FILE, arguments.input_separator)
    #
    # if ip_records is None:
    #     print("Program exiting ...", file=sys.stderr)
    #     return
    #
    # if arguments.verbose:
    #     print(
    #         "Correct input record identified by 'correct=1' last field in _IP_RECORD tuple. Incorrect record identified by 'correct=0' field.")
    #     for ipRecord in ip_records:
    #         print(ipRecord)
    #
    # if arguments.database == "all":
    #     for value in databases.values():
    #         value.check_ips(ip_records, arguments.output_separator, arguments.cut, arguments.replace, arguments.verbose)
    # else:
    #     try:
    #         databases[arguments.database].check_ips(ip_records, arguments.output_separator, arguments.cut,
    #                                                 arguments.replace, arguments.verbose)
    #     except KeyError as error:
    #         print("Wrong Database name:", error, "See Help (-h) for Dabatases & Links name to use !", file=sys.stderr)
    #
    fileprocessing.process_output(path, '\t')


=======
    ip_records = fileprocessing.get_ip_records(arguments.FILE, arguments.input_separator)

    if ip_records is None:
        print("Program exiting ...", file=sys.stderr)
        return

    if arguments.verbose:
        print(
            "Correct input record identified by 'correct=1' last field in _IP_RECORD tuple. Incorrect record identified by 'correct=0' field.")
        for ipRecord in ip_records:
            print(ipRecord)

    if arguments.database == "all":
        for value in databases.values():
            value.check_ips(ip_records, arguments.output_separator, arguments.cut, arguments.replace, arguments.verbose)
    else:
        try:
            databases[arguments.database].check_ips(ip_records, arguments.output_separator, arguments.cut,
                                                    arguments.replace, arguments.verbose)
        except KeyError as error:
            print("Wrong Database name:", error, "See Help (-h) for Dabatases & Links name to use !", file=sys.stderr)

    fileprocessing.process_output('input.dat',path, '\t', '\t' )
>>>>>>> parent of 82047a2... folium map generation fully implemented +  some minor code changes and reformatting
main()
