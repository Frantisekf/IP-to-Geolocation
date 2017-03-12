#!/usr/bin/env python3


import datetime
from urllib import request

import geoip2.database
from geopy.distance import vincenty


def check_ips(ipRecords, separator, cut, replace, verbose):
    # Output file & Separator preparation

    database_filepath = ''

    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = "./results/maxMindGeolite2city_" + current_date_and_time + ".dat"
    output_file = open(filename, "w", encoding="utf-8")

    reader = geoip2.database.Reader(database_filepath)

    #   IF NO DATA RETRIEVED
    country = '-'
    region = '-'
    city = '-'
    latitude = '-'
    longitude = '-'

    for ipRecord in ipRecords:

        response = reader.city(ipRecord)
        res = request.city(ipRecord)
        content = {}

        content['ip'] = res.traits.ip_address

        if not res.country:
            content['country_code'] = '-'
        else:
            content['country_code'] = res.country.iso_code
            country = content['country_code']
        if not res.subdivisions:
            content['region'] = res.subdivisions[0].names['en']
            region = content['region']
        if not res.city.names:
            content['city'] = '-'
        else:
            content['city'] = res.city.names['en']
            city = content['city']

        if res.location:
            content['latitude'] = res.location.latitude
            content['longitude'] = res.location.longitude

            latitude = content['latitude']
            longitude = content['longitude']

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

        latitude = str(latitude)
        longitude = str(longitude)
        error = str(error)

        output_file.write(separator.join(ipRecord.row) + separator + "freegeoip" + separator + country +
                          separator + country_match + separator + region + separator +
                          region_match + separator + city + separator + city_match +
                          separator + latitude + city + separator + city_match +
                          separator + latitude + separator + longitude + separator +
                          error + "\n")

        reader.close()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
