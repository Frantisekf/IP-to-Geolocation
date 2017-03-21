#!/usr/bin/env python3
"""
This module provides functionality for pre-processing input file for Geo IP location
It will create list of IP records which needs to be checked.

>>> getiprecords(file)
[]
"""

import collections
import csv
import os

import folium
import pandas as pd

_IP_RECORD = collections.namedtuple("_IP_RECORD", "id ip dns continent countryCoordinate regionCoordinate cityCoordinate \
    unknown_parameter_1 unknown_parameter_2 latitudeCoordinate longitudeCoordinate dns_correction \
    row correct")


def get_ip_records(filename, input_separator):
    """ This function process input file lines and returns list of _IP_RECORD named tuples for IP addresses to be
        processed
    :param input_file: Input file name to be used
    :param separator: delimiter of records in file
    :return: List of _IP_RECORD tuples
    """
    ip_records = []

    # Opening Input File
    try:

        input_file = open(filename, "r", encoding="utf-8")

        if input_separator == "tab":
            reader = csv.reader(input_file, delimiter='\t')
            for row in reader:
                if len(row) != 12:
                    # if len(row) != 10:
                    # print("INPUT FILE: Incorrect line record!", file=sys.stderr)
                    # ip_records = None
                    ip_records.append(_IP_RECORD("", "", "", "", "", "", "", "", "", "", "", "", row, 0))
                # print("ROW: ", row, file=sys.stderr)
                # break
                else:
                    ip_records.append(_IP_RECORD(*(tuple(row) + (row, 1))))

        if input_separator == "space":
            reader = csv.reader(input_file, delimiter=' ')
            for row in reader:
                if len(row) != 12:
                    # if len(row) != 10:
                    # print("INPUT FILE: Incorrect line record!", file=sys.stderr)
                    # ip_records = None
                    ip_records.append(_IP_RECORD("", "", "", "", "", "", "", "", "", "", "", "", row, 0))
                # print("ROW: ", row, file=sys.stderr)
                # break
                else:
                    ip_records.append(_IP_RECORD(*(tuple(row) + (row, 1))))

                    # for ip_record in ip_records:
                    #    print(ip_record)
                    #
                    # exit(0)

    except TypeError as error:
        print(error)

    except (OSError, IOError) as error:
        print(error)

    finally:
        if input_file is not None:
            input_file.close()

    return ip_records


# creates a df from output csv for each DB and prints folium map
def process_output(path, separator):
    frames = []

    for file in os.listdir(path):
        if file.endswith(".dat"):
            file = os.path.join(path, file)

            columns = ["id", "ipAddress", "serverName", "continent", "country", "city", "region", "website",
                       "instituteName", "latitude", "longitude", "comment", "database", "countryEst", "countryEst",
                       "regionEst", "regionEstMatch", "cityEst", "cityEstMatch", "latitudeEst", "longitudeEst",
                       "errorEst"]
            # TODO get max rows
            df = pd.read_csv(file, delimiter=separator, header=None, names=columns)
            frames.append(df)

    # TODO color each db
    for i in range(0, 10):
        map = folium.Map(location=[0, 0], zoom_start=8)
        for j in range(0, len(frames) - 1):
            position = frames[j].iloc[i]

            original = folium.Marker([position['latitude'], position['longitude']], popup=position['database']).add_to(
                map)

            if not isinstance(position['latitudeEst'], (int, float)):
                break
            estimate = folium.Marker([position['latitudeEst'], position['longitudeEst']],
                                     popup=position['database'] + 'Estimation').add_to(map)

        dbFolder = path + '/maps/' + str(i)
        if not os.path.exists(dbFolder):
            os.makedirs(dbFolder)
            map.save(dbFolder + '/' + str(i) + '_' + '.html')


def mapDraw(df, path):
    for index, row in df.iterrows():
        map = folium.Map(location=[row['latitude'], row['longitude']], zoom_start=8)
        # add markers
        original = folium.Marker([row['latitude'], row['longitude']], popup=row['serverName'] + ": " +
                                                                            str(row['latitude']) + ';' + str(
            row['longitude']) + 'Error: ' + str(
            row['errorEst'])).add_to(map)
        estimate = folium.Marker([row['latitudeEst'], row['longitudeEst']],
                                 popup=row['serverName'] + ": " +
                                       str(row['latitudeEst']) + ';' + str(
                                     row['longitudeEst']) + 'Error: ' + str(row['errorEst'])).add_to(map)
        # add lines
        points = [original.location, estimate.location]
        folium.PolyLine(locations=points, color="red", weight=2.5, opacity=1).add_to(map)
        # save map

        dbFolder = path + '/maps/' + str(row['database'])
        if not os.path.exists(dbFolder):
            os.makedirs(dbFolder)

        map.save(dbFolder + '/' + str(row['id']) + '_' + '.html')


# TODO map layers with dbs checkboxes




if __name__ == "__main__":
    import doctest

    doctest.testmod()
