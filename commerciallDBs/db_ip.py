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
        filename = "./results/dbIpToLoc_" + current_date_and_time + ".dat"
        outputFile = open(filename, "w", encoding="utf-8")

        url = "https://www.db-ip.com/"

        for ipRecord in ipRecords:

            #   Checking for Incorrect input record
            if ipRecord.correct == 0:
                outputFile.write(separator.join(
                    ipRecord.row) + separator + "dbIpToLoc" + separator + "Error in input data in this line\n")
                continue

            values = {'address': str(ipRecord.ip).strip()}
            data = urllib.parse.urlencode(values)
            headers = {'User-Agent': 'Mozilla/5.0'}
            data = data.encode('utf-8')

            request = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(request)
            responseData = response.read().decode(response.headers.get_content_charset())

            if re.search(r'you have exceeded the daily query limit', responseData):
                outputFile.write(separator.join(
                    ipRecord.row) + separator + "dbIpToLoc" + separator + "Maximum free requests reached!\n")
                continue

            countryEstimation = "-"
            regionEstimation = "-"
            cityEstimation = "-"
            latitudeEstimation = "-"
            longitudeEstimation = "-"
            errorEstimation = "-"

            countryEstimationMatch = "UNK"
            regionEstimationMatch = "UNK"
            cityEstimationMatch = "UNK"

            ipInfoList = re.findall(r'<th.*>([\w\s\\/]+)</th><td>(.*)</td>', responseData)

            for ipInfo in ipInfoList:
                if ipInfo[0] == "Country":
                    countryEstimation = (re.search(r'^[\w-]+(\s+[\w-]+)*', ipInfo[1]))
                    countryEstimation = countryEstimation.group().lstrip(' ').rstrip(' ')

                    ########################## CUT & REPLACE ############################

                    #   REPLACE

                    if replace != '':
                        replace_file = open(replace, "r", encoding='utf-8')
                        reader = csv.reader(replace_file, delimiter='\t')
                        for row in reader:
                            # print(row[0], ' will by replaced by ', row[1])
                            if row[0] in countryEstimation:
                                previous = countryEstimation
                                countryEstimation = countryEstimation.replace(row[0], row[1]).strip(' ')
                                if verbose:
                                    # print('Previous: ', len(previous))
                                    # print('Current: ', len(countryEstimation))
                                    print('ROW: ',
                                          separator.join(ipRecord.row),
                                          ', FIELD: COUNTRY, OPERATION: REPLACE , BEFORE:',
                                          previous,
                                          'AFTER: ' + countryEstimation)
                        replace_file.close()

                    # CUT

                    if cut != '':
                        cut_file = open(cut, "r", encoding='utf-8')
                        # reader = csv.reader(cut_file, delimiter=' ')
                        for row in cut_file:
                            row = row.strip()
                            # print('|' + row + '| will by replaced by ', '<empty>')
                            if row in countryEstimation:
                                previous = countryEstimation
                                countryEstimation = countryEstimation.replace(row, '').strip()
                                if verbose:
                                    print('ROW: ',
                                          separator.join(ipRecord.row),
                                          ', FIELD: COUNTRY, OPERATION: CUT, BEFORE:',
                                          previous,
                                          'AFTER: ', countryEstimation)
                        cut_file.close()
                    #####################################################################

                    if countryEstimation == ipRecord.countryCoordinate:
                        countryEstimationMatch = "YES"
                    else:
                        countryEstimationMatch = "NO"

                if ipInfo[0] == "State / Region":
                    regionEstimation = (re.search(r'^[\w-]+(\s+[\w-]+)*', ipInfo[1]))
                    regionEstimation = regionEstimation.group().lstrip(' ').rstrip(' ')
                    regionEstimation = str(regionEstimation)

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
                                    print('ROW: ',
                                          separator.join(ipRecord.row),
                                          ', FIELD: REGION, OPERATION: REPLACE, BEFORE:',
                                          previous,
                                          'AFTER: ', regionEstimation)
                        replace_file.close()
                    # CUT

                    if cut != '':
                        cut_file = open(cut, "r", encoding='utf-8')
                        # reader = csv.reader(cut_file, delimiter=' ')
                        for row in cut_file:
                            row = row.strip()
                            # print('|' + row + '| will by replaced by ', '<empty>')
                            # print(row[0], ' will by replaced by ', '<empty>')
                            if row in regionEstimation:
                                previous = regionEstimation
                                regionEstimation = regionEstimation.replace(row, '').strip()
                                if verbose:
                                    print('ROW: ',
                                          separator.join(ipRecord.row),
                                          ', FIELD: REGION, OPERATION: CUT, BEFORE:',
                                          previous,
                                          'AFTER: ', regionEstimation)
                        cut_file.close()
                    #####################################################################

                    if regionEstimation == ipRecord.regionCoordinate.strip('"'):
                        regionEstimationMatch = "YES"
                    else:
                        regionEstimationMatch = "NO"

                if ipInfo[0] == "City":
                    cityEstimation = (re.search(r'^[\w-]+(\s+[\w-]+)*', ipInfo[1]))
                    cityEstimation = cityEstimation.group().lstrip(' ').rstrip(' ')

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
                                    print('ROW: ',
                                          separator.join(ipRecord.row),
                                          ', FIELD: CITY, OPERATION: REPLACE, BEFORE:',
                                          previous,
                                          'AFTER: ', cityEstimation)
                        replace_file.close()
                    # CUT

                    if cut != '':
                        cut_file = open(cut, "r", encoding='utf-8')
                        # reader = csv.reader(cut_file, delimiter=' ')
                        for row in cut_file:
                            row = row.strip()
                            # print('|' + row + '| will by replaced by ', '<empty>')
                            # print(row[0], ' will by replaced by ', '<empty>')
                            if row in cityEstimation:
                                previous = cityEstimation
                                cityEstimation = cityEstimation.replace(row, '').strip()
                                if verbose:
                                    print('ROW: ',
                                          separator.join(ipRecord.row),
                                          ', FIELD: CITY, OPERATION: CUT, BEFORE:',
                                          previous,
                                          'AFTER: ', cityEstimation)
                        cut_file.close()
                    #####################################################################

                    if cityEstimation == ipRecord.cityCoordinate.strip('"'):
                        cityEstimationMatch = "YES"
                    else:
                        cityEstimationMatch = "NO"

                if ipInfo[0] == "Coordinates":
                    Coordinates = (re.search(r'^\s*([-+\d\.]+), ([-+\d\.]+)', ipInfo[1]))
                    latitudeEstimation = float(Coordinates.group(1))
                    longitudeEstimation = float(Coordinates.group(2))

            if str(latitudeEstimation) != "-" and str(longitudeEstimation) != "-":
                inputCoordinates = (float(ipRecord.latitudeCoordinate), float(ipRecord.longitudeCoordinate))
                dbipCoordinates = (latitudeEstimation, longitudeEstimation)

                errorEstimation = vincenty(inputCoordinates, dbipCoordinates).kilometers
                errorEstimation = str(errorEstimation)

                latitudeEstimation = str(latitudeEstimation)
                longitudeEstimation = str(longitudeEstimation)

            outputFile.write(separator.join(ipRecord.row) + separator + "dbIpToLoc" + separator + countryEstimation +
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
