#!/usr/bin/env python3

import datetime
import urllib.request
import urllib.parse
import urllib.error
import re
from geopy.distance import vincenty
import time
import csv

url = "http://www.ip2location.com/demo/"

############################################## RECORD DATA SECTIONS ####################################################

html_table = re.compile(r"""
            <(?:(?:tr)(?:\s+[a-zA-Z][-:a-zA-Z0-9]*(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^"'`=<>\s]+))?)*\s*/?)>.*?
            <(?:(?:td)(?:\s+[a-zA-Z][-:a-zA-Z0-9]*(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^"'`=<>\s]+))?)*\s*/?)>
            <b>(.*?)</b>    #   Row record name
            <(?:/(?:td)\s*)>.*?
            <(?:(?:td)(?:\s+[a-zA-Z][-:a-zA-Z0-9]*(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^"'`=<>\s]+))?)*\s*/?)>
            (.*?)           #   Value: e.g. Location ... Country, Region, City or Location ... Latitude, Longitude
            <(?:/(?:td)\s*)>.*?
            <(?:/(?:tr)\s*)>""", re.VERBOSE | re.DOTALL)

html_location = re.compile(r"""
            <(?:(?:img)(?:\s+[a-zA-Z][-:a-zA-Z0-9]*(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^"'`=<>\s]+))?)*\s*/?)>
            \s*(.*?)    #   Country
            ,(.*?)      #   Region
            ,(.*)       #   City
            """, re.VERBOSE | re.DOTALL)

html_lat_lon = re.compile(r"""    ([-+\d\.]+)         #   Latitude
                                     ,\s*
                                  ([-+\d\.]+)         #   Longitude
                         .*""", re.VERBOSE | re.DOTALL)

database_limit = re.compile('Query limit is.*?([\d]{1,2})/50', re.DOTALL)

############################################### CHECK IP'S METHOD ######################################################

def check_ips(ipRecords, separator, cut, replace, verbose):

    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    try:
        current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
        filename = "./results/ip2LocDb24_" + current_date_and_time + ".dat"
        output_file = open(filename, "w", encoding="utf-8")

        #   Initial check for current limit
        response = urllib.request.urlopen(url)
        response_data = response.read().decode('utf-8')
        current_limit = re.search(database_limit, response_data)

        for ipRecord in ipRecords:

            #   Checking for Incorrect input record
            if ipRecord.correct == 0:
                output_file.write(separator.join(ipRecord.row) + separator + "ip2LocDb24" + separator + "Error in input data in this line\n")
                continue

            #   If we reached daily limit, write out to file and continue to next line
            if current_limit is not None and int(current_limit.group(1)) == 0:
                #output_file.write("Maximum free requests reached!\n")
                #output_file.close()
                output_file.write(separator.join(ipRecord.row) + separator + "ip2LocDb24" + separator + "Maximum free requests reached!\n")
                continue
                #return

            values = {'ipAddress': ipRecord.ip}
            data = urllib.parse.urlencode(values)
            headers = {'User-Agent': 'Mozilla/5.0'}
            data = data.encode('utf-8')

            request = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(request)

            response_data = response.read().decode('utf-8')

            #   Get current limit

            current_limit = re.search(database_limit, response_data)

            #################################### PROCESSING RETRIEVED DATA #############################################

            table_rows = html_table.findall(response_data)

            if table_rows is not None:
                for row in table_rows:
                    # print(row)
                    if row[0] == "Location":
                        # print(row[1])
                        location = html_location.search(row[1])
                        if location is not None:
                            # print(location.group(3))
                            country_estimation = location.group(1).strip()
                            region_estimation = location.group(2).strip()
                            city_estimation = location.group(3).strip()
                            # print("Country: ", country_estimation)
                            # print("Region: ", region_estimation)
                            # print("City: ", city_estimation)
                        else:
                            country_estimation = None
                            region_estimation = None
                            city_estimation = None
                            # ... or own Exception
                    if row[0] == "Latitude & Longitude":
                        lat_lon = html_lat_lon.search(row[1])
                        if lat_lon is not None:
                            # print(lat_lon.group(1))
                            # print(lat_lon.group(2))
                            latitude_estimation = float(lat_lon.group(1))
                            longitude_estimation = float(lat_lon.group(2))
                            # print(latitude_estimation)
                            # print(longitude_estimation)
                        else:
                            latitude_estimation = None
                            longitude_estimation = None
                            # ... or own Exception
            else:
                print("Exception!")  # Exception

            ###################################### CUT & REPLACE MODIFICATION ##########################################

            #   REPLACE

            if replace != '':
                replace_file = open(replace, "r", encoding='utf-8')
                reader = csv.reader(replace_file, delimiter='\t')
                for row in reader:
                    # print(row[0], ' will by replaced by ', row[1])
                    if country_estimation is not None:
                        if row[0] in country_estimation:
                            previous = country_estimation
                            country_estimation = country_estimation.replace(row[0], row[1]).strip()
                            if verbose:
                                print('ROW: ',
                                      separator.join(ipRecord.row),
                                      ', FIELD: COUNTRY, OPERATION: REPLACE, BEFORE:',
                                      previous,
                                      'AFTER: ', country_estimation)

                    if region_estimation is not None:
                        if row[0] in region_estimation:
                            previous = region_estimation
                            region_estimation = region_estimation.replace(row[0], row[1]).strip()
                            if verbose:
                                print('ROW: ',
                                      separator.join(ipRecord.row),
                                      ', FIELD: REGION, OPERATION: REPLACE, BEFORE:',
                                      previous,
                                      'AFTER: ', region_estimation)

                    if city_estimation is not None:
                        if row[0] in city_estimation:
                            previous = city_estimation
                            city_estimation = city_estimation.replace(row[0], row[1]).strip()
                            if verbose:
                                print('ROW: ',
                                      separator.join(ipRecord.row),
                                      ', FIELD: CITY, OPERATION: REPLACE, BEFORE:',
                                      previous,
                                      'AFTER: ', city_estimation)
                replace_file.close()
            #   CUT

            if cut != '':
                cut_file = open(cut, "r", encoding='utf-8')
                #reader = csv.reader(cut_file, delimiter=' ')
                for row in cut_file:
                    row = row.strip()
                    # print(row[0], ' will by replaced by ', '<empty>')
                    if country_estimation is not None:
                        if row in country_estimation:
                            previous = country_estimation
                            country_estimation = country_estimation.replace(row, '').strip()
                            if verbose:
                                print('ROW: ',
                                      separator.join(ipRecord.row),
                                      ', FIELD: COUNTRY, OPERATION: CUT, BEFORE:',
                                      previous,
                                      'AFTER: ', country_estimation)

                    if region_estimation is not None:
                        if row in region_estimation:
                            previous = region_estimation
                            region_estimation = region_estimation.replace(row, '').strip()
                            if verbose:
                                print('ROW: ',
                                      separator.join(ipRecord.row),
                                      ', FIELD: REGION, OPERATION: CUT, BEFORE:',
                                      previous,
                                      'AFTER: ', region_estimation)

                    if city_estimation is not None:
                        if row in city_estimation:
                            previous = city_estimation
                            city_estimation = city_estimation.replace(row, '').strip()
                            if verbose:
                                print('ROW: ',
                                      separator.join(ipRecord.row),
                                      ', FIELD: CITY, OPERATION: CUT, BEFORE:',
                                      previous,
                                      'AFTER: ', city_estimation)
                cut_file.close()
            ########################################## COMPARISON & OUTPUT #############################################

            #   COUNTRY
            if country_estimation is not None:
                if country_estimation == ipRecord.countryCoordinate.strip('"'):
                    country_estimation_match = "YES"
                else:
                    country_estimation_match = "NO"
            else:
                country_estimation = "-"
                country_estimation_match = "UNK"

            #   REGION
            if region_estimation is not None:
                if region_estimation == ipRecord.regionCoordinate.strip('"'):
                    region_estimation_match = "YES"
                else:
                    region_estimation_match = "NO"
            else:
                region_estimation = "-"
                region_estimation_match = "UNK"

            #   CITY
            if city_estimation is not None:
                if city_estimation == ipRecord.cityCoordinate.strip('"'):
                    city_estimation_match = "YES"
                else:
                    city_estimation_match = "NO"
            else:
                city_estimation = "-"
                city_estimation_match = "UNK"

            if latitude_estimation is not None and longitude_estimation is not None:
                input_coordinates = (float(ipRecord.latitudeCoordinate), float(ipRecord.longitudeCoordinate))
                output_coordinates = (latitude_estimation, longitude_estimation)
                error_estimation = vincenty(input_coordinates, output_coordinates).kilometers

                latitude_estimation = str(latitude_estimation)
                longitude_estimation = str(longitude_estimation)
                error_estimation = str(error_estimation)

            else:
                latitude_estimation = "-"
                longitude_estimation = "-"
                error_estimation = "-"

            # print(separator.join(ipRecord) + separator + "ip2LocDb24" + separator + country_estimation +
            #              separator + country_estimation_match + separator + region_estimation + separator +
            #              region_estimation_match + separator + city_estimation + separator + city_estimation_match +
            #              separator + latitude_estimation + separator + longitude_estimation + separator +
            #              error_estimation + "\n")

            # if separator == '\t':
            #     print("TABULATOR")
            # else:
            #     print("MEDZERA")

            output_file.write(separator.join(ipRecord.row) + separator + "ip2LocDb24" + separator + country_estimation +
                         separator + country_estimation_match + separator + region_estimation + separator +
                         region_estimation_match + separator + city_estimation + separator + city_estimation_match +
                         separator + latitude_estimation + separator + longitude_estimation + separator +
                         error_estimation + "\n")

            time.sleep(2);

    except (OSError, IOError) as error:
        print(error)
    else:
        pass
    finally:
        if output_file is not None:
            output_file.close()