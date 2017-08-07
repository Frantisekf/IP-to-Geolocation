#!/usr/bin/env python3

import datetime
import urllib
import urllib.request
import urllib.parse
import json
from geopy.distance import vincenty

def check_ips(ipRecords, separator, cut, replace, verbose):
    #Output file & Separator preparation

    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = "./results/freegeoip" + current_date_and_time + ".dat"
    output_file = open(filename, "w", encoding="utf-8")



    for ipRecord in ipRecords:
        request = request.get('http://freegeoip.net/json/' + urllib.quote(ipRecord), timeout=62)

        content = request.content
        content_json = json.loads(content)

        #   IF NO DATA RETRIEVED
        country = '-'
        region = '-'
        city = '-'
        latitude = '-'
        longitude = '-'


        if content_json.get('data'):

            #country
            if content_json['data']['civic'].get('countryIso'):
                country = content_json['country']
            #state
            if content_json['data']['civic'].get('state'):
                region = content_json['region_name']
            #city
            if content_json['data']['civic'].get('city'):
                city = content_json['city']

        if content_json['data'].get('location'):


            if content_json['data']['location']:
                latitude = content_json['location']

            if content_json['data']['location'].get('longitude'):
                longitude = content_json['longitude']



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


        #ERROR CALC

        error = '-'

        if latitude != '-' and longitude != '-':
            correct = (float(ipRecord.latitudeCoordinate), float(ipRecord.longitudeCoordinate))
            retrieved = (float(latitude), float(longitude))
            error = vincenty(correct, retrieved).kilometers


        #OUTPUT TO FILE

        latitude = str(latitude)
        longitude = str(longitude)
        error = str(error)

        output_file.write(separator.join(ipRecord.row) + separator + "freegeoip" + separator + country +
                          separator + country_match + separator + region + separator +
                          region_match + separator + city + separator + city_match +
                          separator + latitude + city + separator + city_match +
                          separator + latitude + separator + longitude + separator +
                          error + "\n")



if __name__ == "__main__":
    import doctest
    doctest.testmod()