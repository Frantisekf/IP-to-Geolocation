#!/usr/bin/env python3

import csv
import datetime
import json
import time
import urllib.parse
import urllib.request

from geopy.distance import vincenty

############### KEY ###########################
key = 'SAK535233J496335F36Z'  # AUTH KEY!#
###############################################

url = 'http://api.eurekapi.com/iplocation/v1.8/locateip'


def check_ips(ipRecords, separator, cut, replace, verbose):
    #   Output file & Separator preparation

    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = "./results/eurekAPI_" + current_date_and_time + ".dat"
    output_file = open(filename, "w", encoding="utf-8")

    #   Local Function for CUT & REPLACE operations
    def operation(optype, string, file, input_record):

        # DEBUG
        # print('Type: ' + optype)
        # print('String: ' + string)
        # print('File: ' + file)

        if optype == 'replace':
            replace_dict = open(file, 'r', encoding='utf-8')
            reader = csv.reader(replace_dict, delimiter='\t')
            for record in reader:
                if record[0] in string:
                    old = string
                    string = string.replace(record[0], record[1]).strip()
                    if verbose:
                        print('ROW: ' + ' '.join(input_record.row) + ', FIELD: CITY, OPERATION: REPLACE, BEFORE:'
                              + old + ' AFTER: ' + string)

            replace_dict.close()

        if optype == 'cut':
            cut_dict = open(file, 'r', encoding='utf-8')
            for record in cut_dict:
                record = record.strip()
                if record in string:
                    old = string
                    string = string.replace(record, '').strip()
                    if verbose:
                        print('ROW: ' + ' '.join(input_record.row) + ', FIELD: CITY, OPERATION: CUT, BEFORE:'
                              + old + ' AFTER: ' + string)
            cut_dict.close()

        return string

    # TEST
    # parameters = {
    #     'key': 'SAKRUG98WDQ6S73M884Z',
    #     'ip': '90.178.223.231',
    #     'format': 'JSON'
    # }

    for ipRecord in ipRecords:

        #   Checking for Incorrect input record
        if ipRecord.correct == 0:
            output_file.write(separator.join(
                ipRecord.row) + separator + "eurekAPI" + separator + "Error in input data in this line\n")
            continue

        parameters = {
            'key': key,  # AUTHENTICATION KEY
            'ip': ipRecord.ip,
            'format': 'JSON'
        }

        #   DATA RETRIEVAL

        data = urllib.parse.urlencode(parameters).encode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(request)

        #   Status Code
        http_status_code = response.getcode()

        if http_status_code == 429:
            output_file.write(separator.join(ipRecord.row) + separator + "eurekAPI"
                              + separator + "queries/minute limit exceeded || License has Expired !\n")
            continue

        content = response.read().decode(response.headers.get_content_charset())
        content_json = json.loads(content)

        #   IF NO DATA RETRIEVED
        country = '-'
        region = '-'
        city = '-'
        latitude = '-'
        longitude = '-'

        if content_json.get('geolocation_data'):

            # Country Information
            if content_json['geolocation_data'].get('country_code_iso3166alpha2'):
                country = content_json['geolocation_data'].get('country_code_iso3166alpha2')

            # Region Information
            if content_json['geolocation_data'].get('region_name'):
                region = content_json['geolocation_data'].get('region_name')

            # City Information
            if content_json['geolocation_data'].get('city'):
                city = content_json['geolocation_data'].get('city')

            # Latitude Information
            if content_json['geolocation_data'].get('latitude'):
                latitude = content_json['geolocation_data'].get('latitude')

            # Longitude Information
            if content_json['geolocation_data'].get('longitude'):
                longitude = content_json['geolocation_data'].get('longitude')

                # DEBUG - after retrieval
                # print('Country: ' + country)
                # print('Region: ' + region)
                # print('City: ' + city)
                # print('Latitude: ' + str(latitude))
                # print('Longitude: ' + str(longitude))

        # DATA MODIFICATION

        if replace:
            if country != '-':
                country = operation('replace', country, replace, ipRecord)
            if region != '-':
                region = operation('replace', region, replace, ipRecord)
            if city != '-':
                city = operation('replace', city, replace, ipRecord)

        if cut:
            if country != '-':
                country = operation('cut', country, cut, ipRecord)
            if region != '-':
                region = operation('cut', region, cut, ipRecord)
            if city != '-':
                city = operation('cut', city, cut, ipRecord)

        # DEBUG - after CUT & REPLACE
        # print('Country: ' + country)
        # print('Region: ' + region)
        # print('City: ' + city)
        # print('Latitude: ' + str(latitude))
        # print('Longitude: ' + str(longitude))

        #   DATA COMPARISON

        country_match = 'UNK'
        region_match = 'UNK'
        city_match = 'UNK'

        if country != '-':
            if country == ipRecord.countryCoordinate.strip('"'):
                country_match = 'YES'
            else:
                country_match = 'NO'

        if region != '-':
            if region == ipRecord.regionCoordinate.strip('"'):
                region_match = 'YES'
            else:
                region_match = 'NO'

        if city != '-':
            if city == ipRecord.cityCoordinate.strip('"'):
                city_match = 'YES'
            else:
                city_match = 'NO'

        # ERROR CALCULATION

        error = '-'

        if latitude != '-' and longitude != '-':
            correct = (float(ipRecord.latitudeCoordinate), float(ipRecord.longitudeCoordinate))
            retrieved = (float(latitude), float(longitude))
            error = vincenty(correct, retrieved).kilometers

        # OUTPUT TO FILE

        latitude = str(latitude)
        longitude = str(longitude)
        error = str(error)

        output_file.write(separator.join(ipRecord.row) + separator + "eurekAPI" + separator + country +
                          separator + country_match + separator + region + separator + region_match + separator +
                          city + separator + city_match + separator + latitude + separator + longitude + separator +
                          error + "\n")

        time.sleep(2)

    output_file.close()
