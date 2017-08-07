#!/usr/bin/env python3
import datetime
import json
import urllib
import urllib.request
from geopy.distance import vincenty
import geocoder


def check_ips(ipRecords, separator, cut, replace, verbose):
    api_key = 'a22537003320ff43a5120079e3362c67aa6c9a13'

    # output file preparation & separator

    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = "./results/ip2city_" + current_date_and_time + ".dat"
    output_file = open(filename, "w", encoding="utf-8")

    for ipRecord in ipRecords:
        request = request.get('http://api.db-ip.com/addrinfo?' + api_key + '&addr=' + urllib.quote(ipRecord),
                              timeout=62)

        # check if IP response is 200

        # parse content
        content = request.content
        content = json.loads(content)

        #   IF NO DATA RETRIEVED
        country = '-'
        region = '-'
        city = '-'
        latitude = '-'
        longitude = '-'

        g = geocoder.osm(content['city'] + separator + content['stateprov'] + separator + content['country'])
        g = g.json

        # check lat/long through geocoder
        if g['statuscode'] == 200:
            # content['latitude'] = unicode(g['latitude'])
            # content['longitude'] = unicode(g['longitude'])

            # country
            if content['data']['civic'].get('countryIso'):
                country = content['country']
            # state
            if content['data']['civic'].get('state'):
                region = content['region_name']
            # city
            if content['data']['civic'].get('city'):
                city = content['city']

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

        # ERROR CALC
        error = '-'

        if latitude != '-' and longitude != '-':
            correct = (float(ipRecord.latitudeCoordinate), float(ipRecord.longitudeCoordinate))
            retrieved = (float(latitude), float(longitude))
            error = vincenty(correct, retrieved).kilometers

        # OUTPUT TO FILE

        latitude = str(latitude)
        longitude = str(longitude)
        error = str(error)

        output_file.write(separator.join(ipRecord.row) + separator + "dpip2city" + separator + country +
                      separator + country_match + separator + region + separator +
                      region_match + separator + city + separator + city_match +
                      separator + latitude + city + separator + city_match +
                      separator + latitude + separator + longitude + separator +
                      error + "\n")

if __name__ == "__main__":
    import doctest
    doctest.testmod()