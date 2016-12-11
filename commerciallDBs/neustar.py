#!/usr/bin/env python3
"""
This module provides functionality for pre-processing input file for Geo IP location
It will create list of IP records which needs to be checked.

>>> checkIPs(ipRecords, separator)
[]
"""

import datetime
import urllib.request
import urllib.parse
import urllib.error
import re
from geopy.distance import vincenty
import time
import csv
#
url = "https://www.neustar.biz/resources/tools/ip-geolocation-lookup-tool"
#
def check_ips(ipRecords, separator, cut, replace, verbose):

    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    #   Get Current Time and Date for Filename
    current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

    #   Opening Input File
    try:
        filename = "./results/neustarWhere_" + current_date_and_time + ".dat"
        outputFile = open(filename, "w", encoding="utf-8")

        #   Debug
        #for ipRecord in ipRecords:
        #    outputFile.write(str(ipRecord) + "\n")

        for ipRecord in ipRecords:

            #   Checking for Incorrect input record
            if ipRecord.correct == 0:
                outputFile.write(separator.join(ipRecord.row) + separator + "neustarWhere" + separator + "Error in input data in this line\n")
                continue

            #print(ipRecord.countryCoordinate)
            values = {'ip' : ipRecord.ip }
            data = urllib.parse.urlencode(values)
            headers = {'User-Agent':'Mozilla/5.0'}
            data = data.encode('utf-8')

            request = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(request)
            responseData = response.read().decode(response.headers.get_content_charset())

            if re.search(r'Rate limit exceeded', responseData):
                outputFile.write(separator.join(
                    ipRecord.row) + separator + "neustarWhere" + separator + "Maximum free requests reached!\n")
                continue

            #break

            #print(responseData)
            #exit(1)

            countryEstimation = "-"
            regionEstimation = "-"
            cityEstimation = "-"
            latitudeEstimation = "-"
            longitudeEstimation = "-"
            errorEstimation = "-"

            countryEstimationMatch = "UNK"
            regionEstimationMatch = "UNK"
            cityEstimationMatch = "UNK"

            #print(type(responseData))

            ipInfoList = re.findall(r"\s*<td\s*[^<>]*>(\s*[^<>]*\s*)</td>\s*<td>(\s*[^<>]*\s*)</td>\s*", responseData)

            #ipInfoList = re.findall(r'<tr>\s*<td.*>\s*([\w\s.-]+:)\s*</td>\s*<td>\s*([\w\s.-]+)\s*</td>\s*</tr>', responseData)
            #print(ipInfoList)
            #outputFile.write(str(ipInfoList))

            #break

            for ipInfo in ipInfoList:
                if ipInfo[0] == "Country Code:":
                    countryEstimation = ipInfo[1].upper()
        #            print("CountryEstimation: ", countryEstimation)
        #            countryEstimation = countryEstimation.group().lstrip(' ').rstrip(' ')
                    ########################## CUT & REPLACE ############################

                    #   REPLACE

                    if replace != '':
                        replace_file = open(replace, "r", encoding='utf-8')
                        reader = csv.reader(replace_file, delimiter='\t')
                        for row in reader:
                            # print(row[0], ' will by replaced by ', row[1])
                            if row[0] in countryEstimation:
                                previous = countryEstimation
                                countryEstimation = countryEstimation.replace(row[0], row[1]).strip()
                                if verbose:
                                    print('ROW: ', separator.join(ipRecord.row),
                                          ', FIELD: COUNTRY, OPERATION: REPLACE, BEFORE:',
                                          previous, 'AFTER: ', countryEstimation)
                        replace_file.close()
                    # CUT

                    if cut != '':
                        cut_file = open(cut, "r", encoding='utf-8')
                        #reader = csv.reader(cut_file, delimiter=' ')
                        for row in cut_file:
                            row = row.strip()
                            # print(row[0], ' will by replaced by ', '<empty>')
                            if row in countryEstimation:
                                previous = countryEstimation
                                countryEstimation = countryEstimation.replace(row, '').strip()
                                if verbose:
                                    print('ROW: ', separator.join(ipRecord.row),
                                          ', FIELD: COUNTRY, OPERATION: CUT, BEFORE:',
                                          previous, 'AFTER: ', countryEstimation)
                        cut_file.close()
                        #####################################################################
                    if countryEstimation == ipRecord.countryCoordinate.upper():
                        countryEstimationMatch = "YES"
                    else:
                        countryEstimationMatch = "NO"

                if ipInfo[0] == "Region:" and len(ipInfo[1]) != 0:
                    regionEstimation = ipInfo[1].lower()
        #            print("regionEstimation: ", regionEstimation)
        #            regionEstimation = regionEstimation.group().lstrip(' ').rstrip(' ')
                    ########################## CUT & REPLACE ############################

                    #   REPLACE

                    if replace != '':
                        replace_file = open(replace, "r", encoding='utf-8')
                        reader = csv.reader(replace_file, delimiter='\t')
                        for row in reader:
                            # print(row[0], ' will by replaced by ', row[1])
                            if row[0] in regionEstimation:
                                previous = regionEstimation
                                regionEstimation = regionEstimation.replace(row[0], row[1]).strip()
                                if verbose:
                                    print('ROW: ', separator.join(ipRecord.row),
                                          ', FIELD: REGION, OPERATION: REPLACE, BEFORE:',
                                          previous, 'AFTER: ', regionEstimation)
                        replace_file.close()

                    # CUT

                    if cut != '':
                        cut_file = open(cut, "r", encoding='utf-8')
                        #reader = csv.reader(cut_file, delimiter=' ')
                        for row in cut_file:
                            row = row.strip()
                            # print(row[0], ' will by replaced by ', '<empty>')
                            if row in regionEstimation:
                                previous = regionEstimation
                                regionEstimation = regionEstimation.replace(row, '').strip()
                                if verbose:
                                    print('ROW: ', separator.join(ipRecord.row),
                                          ', FIELD: REGION, OPERATION: CUT, BEFORE:',
                                          previous, 'AFTER: ', regionEstimation)
                        cut_file.close()
                        #####################################################################
                    if regionEstimation == ipRecord.regionCoordinate.lower():
                        regionEstimationMatch = "YES"
                    else:
                        regionEstimationMatch = "NO"

                if ipInfo[0] == "City:":
                    cityEstimation = ipInfo[1].capitalize()
        #            print("CityEstimation: ", cityEstimation)
        #            cityEstimation = cityEstimation.group().lstrip(' ').rstrip(' ')
                    ########################## CUT & REPLACE ############################

                    #   REPLACE

                    if replace != '':
                        replace_file = open(replace, "r", encoding='utf-8')
                        reader = csv.reader(replace_file, delimiter='\t')
                        for row in reader:
                            # print(row[0], ' will by replaced by ', row[1])
                            if row[0] in cityEstimation:
                                previous = cityEstimation
                                cityEstimation = cityEstimation.replace(row[0], row[1]).strip()
                                if verbose:
                                    print('ROW: ', separator.join(ipRecord.row),
                                          ', FIELD: CITY, OPERATION: REPLACE, BEFORE:',
                                          previous, 'AFTER: ', cityEstimation)
                        replace_file.close()

                    # CUT

                    if cut != '':
                        cut_file = open(cut, "r", encoding='utf-8')
                        #reader = csv.reader(cut_file, delimiter=' ')
                        for row in cut_file:
                            row = row.strip()
                            # print(row[0], ' will by replaced by ', '<empty>')
                            if row in cityEstimation:
                                previous = cityEstimation
                                cityEstimation = cityEstimation.replace(row, '').strip()
                                if verbose:
                                    print('ROW: ', separator.join(ipRecord.row),
                                          ', FIELD: CITY, OPERATION: REPLACE, BEFORE:',
                                          previous, 'AFTER: ', cityEstimation)
                        cut_file.close()
                        #####################################################################
                    if cityEstimation == ipRecord.cityCoordinate.capitalize():
                        cityEstimationMatch = "YES"
                    else:
                        cityEstimationMatch = "NO"

                if ipInfo[0] == "Latitude:":
        #            Coordinates = (re.search(r'^\s*(\d+.\d+), (\d+.\d+)', ipInfo[1]))
                    latitudeEstimation = float(ipInfo[1])
        #            longitudeEstimation = float(Coordinates.group(2))
        #            print("LatitudeEstimation: ", latitudeEstimation)
        #            print("Longitude: ", longitudeEstimation)

                if ipInfo[0] == "Longitude:":
        #            Coordinates = (re.search(r'^\s*(\d+.\d+), (\d+.\d+)', ipInfo[1]))
        #            latitudeEstimation = float(ipInfo[1])
                    longitudeEstimation = float(ipInfo[1])
        #            print("LatitudeEstimation: ", latitudeEstimation)
        #            print("LongitudeEstimation: ", longitudeEstimation)

            #    print(ipInfo[0],":\t\t\t",ipInfo[1])

            if str(latitudeEstimation) != "-" and str(longitudeEstimation) != "-":
                inputCoordinates = (float(ipRecord.latitudeCoordinate), float(ipRecord.longitudeCoordinate))
        #        #print(inputCoordinates)
                dbipCoordinates = (latitudeEstimation, longitudeEstimation)
        #        #print(dbipCoordinates)

                errorEstimation = vincenty(inputCoordinates, dbipCoordinates).kilometers
                errorEstimation = str(errorEstimation)

                latitudeEstimation = str(latitudeEstimation)
                longitudeEstimation = str(longitudeEstimation)

        #    print(errorEstimation + "\n")
            outputFile.write(separator.join(ipRecord.row) + separator + "neustarWhere" + separator + countryEstimation +
                             separator + countryEstimationMatch + separator + regionEstimation + separator +
                             regionEstimationMatch + separator + cityEstimation + separator + cityEstimationMatch +
                             separator + latitudeEstimation + separator + longitudeEstimation + separator +
                             errorEstimation + "\n")

            time.sleep(1)

            #outputFile.write(separator.join(ipRecord) + separator + "dbIpToLoc" + separator +
            #                 countryEstimation + separator + countryEstimationMatch + separator +
            #                 regionEstimation + separator + regionEstimationMatch + separator +
            #                 cityEstimation + separator + cityEstimationMatch + separator +
            #                 latitudeEstimation + separator + longitudeEstimation + separator + errorEstimation + "\n")
            #print("################################################################################")

    except (OSError, IOError) as error:
        print(error)
    else:
        pass
    finally:
        if outputFile is not None:
            outputFile.close()

if __name__ == "__main__":
    import doctest
    doctest.testmod()