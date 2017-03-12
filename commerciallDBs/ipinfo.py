#!/usr/bin/env python3
"""
This module provides functionality for pre-processing input file for Geo IP location
It will create list of IP records which needs to be checked.

>>> checkIPs(ipRecords, separator)
[]
"""

import csv
import datetime
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from geopy.distance import vincenty


def check_ips(ipRecords, separator, cut, replace, verbose):
    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    # Get Current Time and Date for Filename
    current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

    #   Opening Input File
    try:
        filename = "./results/ipInfo_" + current_date_and_time + ".dat"
        outputFile = open(filename, "w", encoding="utf-8")

        for ipRecord in ipRecords:

            #   Checking for Incorrect input record
            if ipRecord.correct == 0:
                outputFile.write(separator.join(
                    ipRecord.row) + separator + "ipInfo" + separator + "Error in input data in this line\n")
                continue

            url = "https://ipinfo.io/" + ipRecord.ip + "/json?token=iplocation.net"

            response = urllib.request.urlopen(url)
            responseData = response.read().decode('utf-8')

            countryEstimation = re.search(r'"country"\s*:\s*"(.*?)"', responseData, re.DOTALL)
            regionEstimation = re.search(r'"region"\s*:\s*"(.*?)",?', responseData, re.DOTALL)
            cityEstimation = re.search(r'"city"\s*:\s*"(.*?)",?', responseData, re.DOTALL)
            locationEstimation = re.search(r'"loc"\s*:\s*"([\d.-]+),([\d.-]+)"', responseData, re.DOTALL)
            if locationEstimation is not None:
                latitudeEstimation = locationEstimation.group(1)
                longitudeEstimation = locationEstimation.group(2)
            else:
                latitudeEstimation = None
                longitudeEstimation = None

            # print("Contry: ", countryEstimation.group(1))
            # print("Region: ", regionEstimation.group(1), " Len: ", len(regionEstimation.group(1)))
            # print("City: ", cityEstimation.group(1))
            # print("Latitude: ", latitudeEstimation)
            # print("Longitude: ", longitudeEstimation)

            errorEstimation = "-"

            countryEstimationMatch = "UNK"
            regionEstimationMatch = "UNK"
            cityEstimationMatch = "UNK"

            if countryEstimation is not None and len(countryEstimation.group(1)) != 0:
                countryEstimation = str(countryEstimation.group(1))
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
                    # reader = csv.reader(cut_file, delimiter=' ')
                    for row in cut_file:
                        row = row.rstrip()
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
                if countryEstimation == ipRecord.countryCoordinate.strip('"'):
                    countryEstimationMatch = "YES"
                else:
                    countryEstimationMatch = "NO"
            else:
                countryEstimation = "-"

            if regionEstimation is not None and len(regionEstimation.group(1)) != 0:
                regionEstimation = str(regionEstimation.group(1))
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
                    # reader = csv.reader(cut_file, delimiter=' ')
                    for row in cut_file:
                        row = row.rstrip()
                        # print(row[0], ' will by replaced by ', '<empty>')
                        if row in regionEstimation:
                            previous = regionEstimation
                            regionEstimation = regionEstimation.replace(row, '').strip()
                            if verbose:
                                print('ROW: ', separator.join(ipRecord.row), ', FIELD: REGION, OPERATION: CUT, BEFORE:',
                                      previous, 'AFTER: ', regionEstimation)
                    cut_file.close()
                    #####################################################################
                if regionEstimation == ipRecord.regionCoordinate.strip('"'):
                    regionEstimationMatch = "YES"
                else:
                    regionEstimationMatch = "NO"
            else:
                regionEstimation = "-"

            if cityEstimation is not None and len(cityEstimation.group(1)) != 0:
                cityEstimation = str(cityEstimation.group(1))
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
                    # reader = csv.reader(cut_file, delimiter=' ')
                    for row in cut_file:
                        row = row.rstrip()
                        # print(row[0], ' will by replaced by ', '<empty>')
                        if row in cityEstimation:
                            previous = cityEstimation
                            cityEstimation = cityEstimation.replace(row, '').strip()
                            if verbose:
                                print('ROW: ', separator.join(ipRecord.row), ', FIELD: CITY, OPERATION: CUT, BEFORE:',
                                      previous, 'AFTER: ', cityEstimation)
                    cut_file.close()
                    #####################################################################
                if cityEstimation == ipRecord.cityCoordinate.strip('"'):
                    cityEstimationMatch = "YES"
                else:
                    cityEstimationMatch = "NO"
            else:
                cityEstimation = "-"

            if latitudeEstimation is not None and len(latitudeEstimation) != 0:
                latitudeEstimation = float(latitudeEstimation)
            else:
                latitudeEstimation = "-"

            if longitudeEstimation is not None and len(longitudeEstimation) != 0:
                longitudeEstimation = float(longitudeEstimation)
            else:
                longitudeEstimation = "-"

            if str(latitudeEstimation) != "-" and str(longitudeEstimation) != "-":
                inputCoordinates = (float(ipRecord.latitudeCoordinate), float(ipRecord.longitudeCoordinate))
                dbipCoordinates = (latitudeEstimation, longitudeEstimation)

                errorEstimation = vincenty(inputCoordinates, dbipCoordinates).kilometers
                errorEstimation = str(errorEstimation)

                latitudeEstimation = str(latitudeEstimation)
                longitudeEstimation = str(longitudeEstimation)

            outputFile.write(separator.join(ipRecord.row) + separator + "ipInfo" + separator + countryEstimation +
                             separator + countryEstimationMatch + separator + regionEstimation + separator +
                             regionEstimationMatch + separator + cityEstimation + separator + cityEstimationMatch +
                             separator + latitudeEstimation + separator + longitudeEstimation + separator +
                             errorEstimation + "\n")

            time.sleep(1)

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
