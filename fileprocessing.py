#!/usr/bin/env python3
"""
This module provides functionality for pre-processing input file for Geo IP location
It will create list of IP records which needs to be checked.

>>> getiprecords(file)
[]
"""

import collections
import csv
import sys

# class IncorrectInputLine(Exception): pass

#_IP_RECORD = collections.namedtuple("_IP_RECORD", "id ip dns countryCoordinate regionCoordinate cityCoordinate \
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
                #if len(row) != 10:
                    #print("INPUT FILE: Incorrect line record!", file=sys.stderr)
                    #ip_records = None
                    ip_records.append(_IP_RECORD("", "", "", "", "", "", "", "", "", "", "", "", row, 0))
                    #print("ROW: ", row, file=sys.stderr)
                    #break
                else:
                    ip_records.append(_IP_RECORD(*(tuple(row) + (row, 1))))

        if input_separator == "space":
            reader = csv.reader(input_file, delimiter=' ')
            for row in reader:
                if len(row) != 12:
                #if len(row) != 10:
                    #print("INPUT FILE: Incorrect line record!", file=sys.stderr)
                    #ip_records = None
                    ip_records.append(_IP_RECORD("", "", "", "", "", "", "", "", "", "", "", "", row, 0))
                    #print("ROW: ", row, file=sys.stderr)
                    #break
                else:
                    ip_records.append(_IP_RECORD(*(tuple(row) + (row, 1))))

        #for ip_record in ip_records:
        #    print(ip_record)
        #
        #exit(0)

    except TypeError as error:
        print(error)

    except (OSError, IOError) as error:
        print(error)

    finally:
        if input_file is not None:
            input_file.close()

    return ip_records

if __name__ == "__main__":
    import doctest
    doctest.testmod()
