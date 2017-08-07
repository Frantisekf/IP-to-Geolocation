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
<<<<<<< HEAD

import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
=======
import pandas as pd
import folium
import mapgenerator

# class IncorrectInputLine(Exception): pass

# _IP_RECORD = collections.namedtuple("_IP_RECORD", "id ip dns countryCoordinate regionCoordinate cityCoordinate \
#                                    unknown_parameter_1 unknown_parameter_2 latitudeCoordinate longitudeCoordinate \
#                                    row correct")
>>>>>>> parent of 82047a2... folium map generation fully implemented +  some minor code changes and reformatting

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


<<<<<<< HEAD
<<<<<<< HEAD
=======
# creates a df from output csv for each DB and prints folium map
>>>>>>> parent of 4c030c8... get_table function added + minor changes
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

            df = pd.read_csv(file, delimiter=separator, header=None, names=columns)
            row_count = df['id'].count()
            df.replace(['-'], 0, inplace=True)

            frames.append(df)

<<<<<<< HEAD
    # generate folium map and graph report
    for i in range(0, row_count):
=======
    for i in range(0, 10):
>>>>>>> parent of 4c030c8... get_table function added + minor changes
        map = folium.Map(location=[0, 0], zoom_start=1)
        figures = []
        figs = np.array([])
        for j in range(0, len(frames) - 1):
            df_idx = frames[j].iloc[i]
            original = folium.RegularPolygonMarker(location=[df_idx['latitude'], df_idx['longitude']],
                                                   popup=df_idx['database'] + ': ' + str(df_idx['latitude']) + '; '
                                                         + str(df_idx['longitude']),
                                                   fill_color=markers[df_idx['database']]).add_to(map)
            estimate = folium.RegularPolygonMarker(location=[df_idx['latitudeEst'], df_idx['longitudeEst']],
                                                   popup=df_idx['database'] + 'Estimation: '
                                                         + str(df_idx['latitudeEst']) + '; '
                                                         + str(df_idx['longitudeEst']) + '\nError: '
                                                         + str(df_idx['errorEst']),
                                                   fill_color=markers[df_idx['database']]).add_to(map)
            # folium.PolyLine([original.location, estimate.location], color='red', weight=1.5,
            # opacity=1).add_to(map)
            figures.append(plot_cdf(frames[j]))
            clean_figs = [x for x in figures if x is not None]

            plt.close()

        dbFolder = path + '/maps/' + str(i)
        if not os.path.exists(dbFolder):
            os.makedirs(dbFolder)
            map.save(dbFolder + '/' + str(i) + '_' + '.html')
<<<<<<< HEAD
    figures.clear()
    save_to_pdf(clean_figs)
    get_table(frames)
=======
    save_to_pdf(clean_figs)

>>>>>>> parent of 4c030c8... get_table function added + minor changes

# Calculates CDF, quantile
def plot_cdf(df):
    series = df.loc[:, 'errorEst']
    pd.to_numeric(series)
    # series = series.convert_objects(convert_numeric=True) deprecated
    series = series[series > 0]

    # Check is series is empty
    if len(series) == 0:
        return

    # CDF calculation
    series.sort_values()
    series[len(series)] = series.iloc[-1]
    cum_dist = np.linspace(0., 1., len(series))
    series_cdf = pd.Series(cum_dist, index=series)

    # Quantile calculation
    quantile = series.quantile(.1)

    # Median calculation
    median = df['errorEst'].median()

    # Figure plot
    fig = plt.figure(figsize=(7, 5))
    series_cdf.plot()
    ax = plt.subplot(111)

    # Graph properties
    plt.xlabel('Vincenty distance error')
    plt.title(str(df.loc[1, 'database']).upper() + ' CDF').set_weight('bold')
    plt.legend(df['database'] + '\n' + 'Median: ' + str(round(median, 2)) + ' Quantile: ' + str(round(quantile, 2)),
               loc='best')
    ax.spines['top'].set_visible(False)
    ax.spines["right"].set_visible(False)

    return fig


<<<<<<< HEAD
def get_table(frames):
    table = pd.DataFrame(
        columns=['Database', 'Median', 'Quantile', 'Tertiles', 'Quartiles', 'Quintiles', 'Octiles', 'StandardDeviation',
                 'Mean'],
        index=range(len(frames)))
    i = 0
    for frame in frames:
        err_row = frame.loc[:, 'errorEst']
        pd.to_numeric(err_row)
        table.loc[i].Database = str(frame.loc[1, 'database'])
        table.loc[i].Median = round(err_row.median(), 2)
        table.loc[i].Quantile = round(err_row.quantile(.1), 2)
        table.loc[i].Tertiles = round(err_row.quantile(.3), 2)
        table.loc[i].Quartiles = round(err_row.quantile(.4), 2)
        table.loc[i].Quintiles = round(err_row.quantile(.5), 2)
        table.loc[i].Octiles = round(err_row.quantile(.8), 2)
        table.loc[i].StandardDeviation = pd.Series(err_row).std()
        table.loc[i].Mean = pd.Series(err_row).mean()
        i += 1

    with open('table.tex', 'w') as file:
        file.write(table.to_latex(bold_rows=True) + '\n')
=======
# TODO graph from tables
# def plot_identity(frames):

# check every table add to counters
# plot graph

# TODO make table of quantile output
# def make_table(df):
>>>>>>> parent of 4c030c8... get_table function added + minor changes


def save_to_pdf(figures):
    with PdfPages('Graph_result.pdf') as pdf:
        for fig in figures:
            pdf.savefig(fig)
=======
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


>>>>>>> parent of 82047a2... folium map generation fully implemented +  some minor code changes and reformatting


if __name__ == "__main__":
    import doctest

    doctest.testmod()
