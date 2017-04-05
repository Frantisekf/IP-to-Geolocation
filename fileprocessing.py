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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

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

    # read .dat files to dataframes
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

    # generate folium map and graph report
    for i in range(0, 10):
        map = folium.Map(location=[0, 0], zoom_start=1)
        figures = []
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
            figures.clear()
            plt.close()

        dbFolder = path + '/maps/' + str(i)
        if not os.path.exists(dbFolder):
            os.makedirs(dbFolder)
            map.save(dbFolder + '/' + str(i) + '_' + '.html')

        save_to_pdf(clean_figs)
        get_table(frames)


# Calculates CDF
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

    # Figure plot
    fig = plt.figure(figsize=(7, 5))
    series_cdf.plot()
    ax = plt.subplot(111)

    # Graph properties
    plt.xlabel('Vincenty distance error')
    plt.title(str(df.loc[1, 'database']).upper() + ' CDF').set_weight('bold')
    plt.legend(df['database'], loc='best')
    ax.spines['top'].set_visible(False)
    ax.spines["right"].set_visible(False)

    return fig


def get_table(frames):
    table = pd.DataFrame(columns=['Database', 'Median', 'Quantile'], index=range(len(frames)))
    i = 0
    for frame in frames:
        err_row = frame.loc[:, 'errorEst']
        table.loc[i].Database = str(frame.loc[1, 'database'])
        table.loc[i].Median = round(err_row.median(), 2)
        table.loc[i].Quantile = round(err_row.quantile(.1), 2)
        i += 1

    with open("table.tex", 'w') as file:
        file.write(table.to_latex(bold_rows=True))


def save_to_pdf(figures):
    with PdfPages('Graph_result.pdf') as pdf:
        for fig in figures:
            pdf.savefig(fig)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
