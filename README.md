<<<<<<< HEAD
Overview
-------------------
Author: Frantisek Farkas <br />
Date:   24.04.2017 <br />
repo: https://github.com/Frantisekf/IP-to-Geolocation <br />


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

Argument flags: <br />
    -i  input File Records Delimiter <br />
    -o  Output File Records Delimiter <br />
    -v  Increase Output Verbosity <br />
    -c  Cut words in specified file <br />
    -r  Replace words in specified file <br />


Directory Structure
-------------------

* resources
    * helpers
    * nonCommerciallDBS - resource modules for querying DBs
    * commerciallDBs
    * databaseFiles - files containing downloadable database(.BIN)
    * dependencies - dependecy libraries for working
    * fileprocessing.py - handles all the file parsing, data manipulation, and output generation
* results - folders contains .dat files with estimated results, CDF graph, table containing median and quantile map files

* input.dat - input file of IP queries (tab or space separated)
* main.py - entrypoint for the application
* README.md

Dependencies 
-------------------

Pandas 0.19.2^ <br />
Matplotlib 2.00^ <br />
maxmindDb 1.2.1^ <br />
numpy 1.12.0^ <br />
geoip 2.4.0^ <br />
geopy 1.11.0^ <br />
folium 0.2.1^ <br />


Databases & Links 
-------------------

IPInfo                    http://www.iplocation.net/ <br />
MaxMind                   http://www.maxmind.com/en/home <br />
DB-IP                     http://db-ip.com/ <br />
IP2Location               http://www.ip2location.com/demo <br />
Skyhook                   https://context.skyhookwireless.com <br />
Neustar                   http://www.neustar.biz/services <br />
Geobytes                  http://www.geobytes.com/IpLocator.htm?GetLocation <br />
Eurek                     https://www.eurekapi.com <br />  REGISTRATION REQUIRED
maxmindgeolite2city       http://www.maxmind.com/en/home <br />
Freegeoip                 http://freegeoip.net/ <br />
Ip2locdb11lite            http://lite.ip2location.com/ <br />

=======
This application implements commerciall and non-commerciall IP Geolocation databases and analyses the results.
>>>>>>> parent of 34ac9a7... minor fixes
