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
import numpy as np
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
    markers = {'dbIpToLoc': '#ff0000',
               'eurekAPI': '#0000cc',
               'geobytes': '#00cc00',
               'ip2LocDb24': '#ffff00',
               'ipInfo': '#66ffff',
               'maxMindGeoIp2Pre': '#339933',
               'neustarWhere': '#663300',
               'skyhookHyperlocal': '#6600cc'}

    for file in os.listdir(path):
        if file.endswith(".dat"):
            file = os.path.join(path, file)

            columns = ["id", "ipAddress", "serverName", "continent", "country", "city", "region", "website",
                       "instituteName", "latitude", "longitude", "comment", "database", "countryEst", "countryEst",
                       "regionEst", "regionEstMatch", "cityEst", "cityEstMatch", "latitudeEst", "longitudeEst",
                       "errorEst"]
            # TODO get max rows
            df = pd.read_csv(file, delimiter=separator, header=None, names=columns)

            df.replace(['-'], 0, inplace=True)

            frames.append(df)

    for i in range(0, 10):
        map = folium.Map(location=[0, 0], zoom_start=8)
        for j in range(0, len(frames) - 1):
            df_position = frames[j].iloc[i]

            test = df_position['latitudeEst']

            folium.Marker([df_position['latitude'], df_position['longitude']],
                          popup=df_position['database'],
                          icon=folium.Icon(color=markers[df_position['database']])).add_to(
                map)

            folium.Marker([df_position['latitudeEst'], df_position['longitudeEst']],
                          popup=df_position['database'] + 'Estimation',
                          icon=folium.Icon(color=markers[df_position['database']]), ).add_to(map)

            visualize(frames[j], path)

        dbFolder = path + '/maps/' + str(i)
        if not os.path.exists(dbFolder):
            os.makedirs(dbFolder)
            map.save(dbFolder + '/' + str(i) + '_' + '. html')


def visualize(df, path):
    # distribution function
    series = df.loc[:, 'errorEst']
    series = series.convert_objects(convert_numeric=True)
    series = series.dropna()

    series.sort_values()

    series[len(series)] = series.iloc[-1]

    cum_dist = np.linspace(0., 1., len(series))
    series_cdf = pd.Series(cum_dist, index=series)

    series_cdf.plot()
    # TODO save to pdf and add median
    # plt.savefig(path + '/graphs/' + df['database'] + '_graphs' + '.pdf')


    # median from error
    # df['errorEst'].median()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
