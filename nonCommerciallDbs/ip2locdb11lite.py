#!/usr/bin/env python3

import ip2location_lib
import  datetime
from geopy.distance import vincenty


def check_ips(ipRecords, separator, cut, replace, verbose):

    #Output file & Separator preparation

    if separator == 'tab':
        separator = '\t'
    else:
        separator = ' '

    current_date_and_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = "./results/ip2locdb11lite" + current_date_and_time + ".dat"
    output_file = open(filename, "w", encoding="utf-8")


    path = '/home/ferko/Dropbox/school/Bakalarka/Stefan_zima/IP2LOCATION-DB11.CSV'

    ip2locObj = ip2location_lib.IP2Location()

    ip2locObj.open(path)


    for ipRecord in ipRecords:

        record = ip2locObj.get_all(ipRecord)

        if not record.country_long:
            country = record.country_long
        else:
            country = '-'

        if not record.city:
            city = record.city
        else:
            city = '-'

        if not record.region:
            region = record.region
        else:
            region = '-'

        if not record.latitude:
            latitude = record.latitude
        else:
            latitude = '-'

        if not record.longitude:
            longitude = record.longitude
        else:
            longitude = '-'


        #data match

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

        output_file.write(separator.join(ipRecord.row) + separator + "ip2locdb11lite" + separator + country +
                          separator + country_match + separator + region + separator +
                          region_match + separator + city + separator + city_match +
                          separator + latitude + city + separator + city_match +
                          separator + latitude + separator + longitude + separator +
                          error + "\n")

if __name__ == "__main__":
    import doctest
    doctest.testmod()

