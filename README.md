Overview
-------------------
Author: Frantisek Farkas
Date:   24.04.2017
repo: https://github.com/Frantisekf/IP-to-Geolocation

This application queries various geolocation DBs with input file which contains a set of IP addresses.
Processes the input and generates results such as CDF plot of the vincenty error between original lat & lon
and the estimated point returned by a DB. Map files generated using folium which shows the geographical positions
of the original and the estimate, and a table that contains median and quantile of the vincety error for each database result




Usage
-------------------


Script tested on Python 3.5.3

Execution of script for help print:
   
   python3 main.py -h
  
Example of script usage:

   python3 main.py input.dat -d IPInfo -v -i tab -o space
   python3 main.py -d MaxMind -v -i tab input.dat
   python3 main.py -d DB-IP -i tab -v -o space input.dat

Argument flags:
    -i  input File Records Delimiter
    -o  Output File Records Delimiter
    -v  Increase Output Verbosity
    -c  Cut words in specified file
    -r  Replace words in specified file


Structure
-------------------

├── resources
│   ├── helpers
|   |── nonCommerciallDBS - resource modules for querying DBs
│   └── commerciallDBs
|   ├── databaseFiles - files containing downloadable database(.BIN)
│   ├── dependencies - dependecy libraries for working  
│   └── fileprocessing.py - handles all the file parsing, data manipulation, and output generation
|
├── results - folders contains .dat files with estimated results, CDF graph, table containing median and quantile
│             map files with original and estimated results generated by folium              
|
├── input.dat - input file of IP queries (tab or space separated)
├── main.py - entrypoint for the application 
└── README.md

Dependencies 
-------------------

Pandas 0.19.2^
Matplotlib 2.00^
maxmindDb 1.2.1^
numpy 1.12.0^
geoip 2.4.0^
geopy 1.11.0^
folium 0.2.1^


Databases & Links 
-------------------

IPInfo                    http://www.iplocation.net/ (2nd table records "ipInfo.io")
MaxMind                   http://www.maxmind.com/en/home
DB-IP                     http://db-ip.com/
IP2Location               http://www.ip2location.com/demo
Skyhook                   https://context.skyhookwireless.com
Neustar                   http://www.neustar.biz/services
Geobytes                  http://www.geobytes.com/IpLocator.htm?GetLocation
Eurek                     REGISTRATION REQUIRED !  https://www.eurekapi.com
maxmindgeolite2city       http://www.maxmind.com/en/home
Freegeoip                 http://freegeoip.net/
Ip2locdb11lite            http://lite.ip2location.com/

