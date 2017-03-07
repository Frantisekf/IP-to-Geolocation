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
import pandas as pd
import folium
import mapgenerator

# class IncorrectInputLine(Exception): pass

# _IP_RECORD = collections.namedtuple("_IP_RECORD", "id ip dns countryCoordinate regionCoordinate cityCoordinate \
#                                    unknown_parameter_1 unknown_parameter_2 latitudeCoordinate longitudeCoordinate \
#                                    row correct")

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


def process_output(input_path, output_path, input_separator, output_separator):
    for fname in os.listdir(output_path):
        if fname.endswith('.dat'):
            try:
                open(fname, 'w').readlines()
            except FileNotFoundError:
                print("No file found in the directory!")
            else:
                # df from input csv
                input_df = pd.read_csv(input_path, delimiter=input_separator, header=None,
                                       names=["id", "ip_address", "server_name", "continent", "country", "city",
                                              "region", "website", "institute_name", "latitude", "longitude",
                                              "comment"])

                # df from output csv for each DB
                output_df = pd.read_csv(fname, delimiter=output_separator, header=None,
                                        names=["name_result", "country_result", "country match_result",
                                               "region_result", "region_match_result",
                                               "city_result", "city_match_result", "latitude_result",
                                               "longitude_result",
                                               "error"])

                # joined dataframes input & output
                dfs = input_df.join(output_df)
                for index, row in dfs.iterrows():
                    if row['latitude'] != row['latitude_result'] and row['longitude'] != row['longitude_result']:
                        map = folium.Map(location=[row['latitude'], row['longitude']], zoom_start=1)
                        # folium markers
                        folium.Marker([row['latitude'], row['longitude']],
                                      popup=row['server_name'] + ": " + row['ip_address'])
                        folium.Marker([row['latitude_result'], row['longitude_result']],
                                      popup=row['server_name'] + ": " + row['latitude_result'] + row[
                                          'longitude_result'])
                        # drawing lines
                        folium.PolyLine(locations=[row['latitude'], row['longitude'],
                                                   [row['latitude_result'], row['longitude_result']]], color="red",
                                        weight=2.5, opacity=1).add_to(map)
                        map.save('./results/maps/' + row['id'] + '.html')
            break

        break




if __name__ == "__main__":
    import doctest

    doctest.testmod()
