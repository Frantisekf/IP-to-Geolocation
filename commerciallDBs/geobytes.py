#!/usr/bin/env python3

import datetime
import urllib.request
import urllib.parse
import json
import csv
from geopy.distance import vincenty

url = "http://getcitydetails.geobytes.com/GetCityDetails"


def check_ips(ipRecords, separator, cut, replace, verbose):

    #   Output file & Separator preparation

    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = "./results/geobytes_" + current_date_and_time + ".dat"
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

    for ipRecord in ipRecords:

        #   Checking for Incorrect input record
        if ipRecord.correct == 0:
            output_file.write(separator.join(
                ipRecord.row) + separator + "geobytes" + separator + "Error in input data in this line\n")
            continue

        parameters = {
            'fqcn': ipRecord.ip
        }

        #   DATA RETRIEVAL

        data = urllib.parse.urlencode(parameters).encode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(request)

        content = response.read().decode('latin-1')
        content_json = json.loads(content)

        #   IF NO DATA RETRIEVED
        country = '-'
        region = '-'
        city = '-'
        latitude = '-'
        longitude = '-'

        # Country Information
        if content_json.get('geobytesinternet'):
            country = content_json.get('geobytesinternet')

        # Region Information
        if content_json.get('geobytesregion'):
            region = content_json.get('geobytesregion')

        # City Information
        if content_json.get('geobytescity'):
            city = content_json.get('geobytescity')

        # Latitude Information
        if content_json.get('geobyteslatitude'):
            latitude = content_json.get('geobyteslatitude')

        # Longitude Information
        if content_json.get('geobyteslongitude'):
            longitude = content_json.get('geobyteslongitude')

        # DEBUG - after retrieval
        # print('Country: ' + country)
        # print('Region: ' + region)
        # print('City: ' + city)
        # print('Latitude: ' + str(latitude))
        # print('Longitude: ' + str(longitude))

        #   DATA MODIFICATION

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

        #   OUTPUT TO FILE

        latitude = str(latitude)
        longitude = str(longitude)
        error = str(error)

        output_file.write(separator.join(ipRecord.row) + separator + "geobytes" + separator + country +
                          separator + country_match + separator + region + separator +
                          region_match + separator + city + separator + city_match +
                          separator + latitude + separator + longitude + separator +
                          error + "\n")

    output_file.close()
