#!/usr/bin/env python3

import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('FILE', help='Database file to process')
parser.add_argument('-p', help="Process fields or no", dest='perform', choices=['yes', 'no'])
arguments = parser.parse_args()

(database, timestamp) = arguments.FILE.split('_')

#   Opening files for database, replace and cut
database_file = open(arguments.FILE, 'r', encoding='utf-8')

replace_dict = None
cut_dict = None

if arguments.perform == "yes":
    replace_dict = open('replace.txt', 'w', encoding='utf-8')
    cut_dict = open('cut.txt', 'w', encoding='utf-8')

country_no = 0
country_yes = 0
region_no = 0
region_yes = 0
city_no = 0
city_yes = 0

country_rules = 0
region_rules = 0
city_rules = 0

pairs = dict()


def print_pairs(pairs):
    for key in pairs.keys():
        print("<" + key + "> : " + str(pairs[key]))


def operation(op, fh, old, new):
    if op == 'r':
        my_string = ''
        c = input('Would like to create string to be replaced ? y/n ')
        if c == 'y':
            replace = input('Enter new string: ')
        else:
            replace = new
        c = input('Would you like to replace by origin ? y/n ')
        if c == 'y':
            replacement = old
        else:
            replacement = input('Enter new string: ')
        fh.write(replace + "\t" + replacement + "\n")
        return

    if op == 'c':
        my_string = input('What do you want to cut: ')
        fh.write(my_string + "\n")
        return


database_output = csv.reader(database_file, delimiter="\t")
for record in database_output:

    if record[13] == 'Maximum free requests reached!':
        continue

    # Country
    if record[14] == 'NO':
        country_no += 1

        if arguments.perform == 'yes':
            if pairs.get(record[13]) is None:
                print("-" * 80)
                print("old:<" + record[4] + ">\nnew:<" + record[13] + ">\n")
                choice = input("Do you want to create Replace rule ? y/n ")
                if choice == 'y':
                    operation('r', replace_dict, record[4], record[13])
                    country_rules += 1
                choice = input("Do you want to create Cut rule ? y/n ")
                if choice == 'y':
                    operation('c', cut_dict, record[4], record[13])
                    country_rules += 1
                pairs[record[13]] = []
                pairs[record[13]].append(record[4])
                # print_pairs(pairs)
            else:
                if not (record[4] in pairs[record[13]]):
                    print("-" * 80)
                    print("old:<" + record[4] + ">\nnew:<" + record[13] + ">\n")
                    choice = input("Do you want to create Replace rule ? y/n ")
                    if choice == 'y':
                        operation('r', replace_dict, record[4], record[13])
                        country_rules += 1
                    choice = input("Do you want to create Cut rule ? y/n ")
                    if choice == 'y':
                        operation('c', cut_dict, record[4], record[13])
                        country_rules += 1
                    pairs[record[13]].append(record[4])
                    # print_pairs(pairs)
    else:
        if record[14] != 'UNK':
            country_yes += 1

    # Region
    if record[16] == 'NO':
        region_no += 1

        if arguments.perform == 'yes':
            if pairs.get(record[15]) is None:
                print("-" * 80)
                print("old:<" + record[5] + ">\nnew:<" + record[15] + ">\n")
                choice = input("Do you want to create Replace rule ? y/n ")
                if choice == 'y':
                    operation('r', replace_dict, record[5], record[15])
                    region_rules += 1
                choice = input("Do you want to create Cut rule ? y/n ")
                if choice == 'y':
                    operation('c', cut_dict, record[5], record[15])
                    region_rules += 1
                pairs[record[15]] = []
                pairs[record[15]].append(record[5])
                # print_pairs(pairs)
            else:
                if not (record[5] in pairs[record[15]]):
                    print("-" * 80)
                    print("old:<" + record[5] + ">\nnew:<" + record[15] + ">\n")
                    choice = input("Do you want to create Replace rule ? y/n ")
                    if choice == 'y':
                        operation('r', replace_dict, record[5], record[15])
                        region_rules += 1
                    choice = input("Do you want to create Cut rule ? y/n ")
                    if choice == 'y':
                        operation('c', cut_dict, record[5], record[15])
                        region_rules += 1
                    pairs[record[15]].append(record[5])
                    # print_pairs(pairs)
    else:
        if record[16] != 'UNK':
            region_yes += 1

    # City
    if record[18] == 'NO':
        city_no += 1

        if arguments.perform == 'yes':
            if pairs.get(record[17]) is None:
                print("-" * 80)
                print("old:<" + record[6] + ">\nnew:<" + record[17] + ">\n")
                choice = input("Do you want to create Replace rule ? y/n ")
                if choice == 'y':
                    operation('r', replace_dict, record[6], record[17])
                    city_rules += 1
                choice = input("Do you want to create Cut rule ? y/n ")
                if choice == 'y':
                    operation('c', cut_dict, record[6], record[17])
                    city_rules += 1
                pairs[record[17]] = []
                pairs[record[17]].append(record[6])
                # print_pairs(pairs)
            else:
                if not (record[6] in pairs[record[17]]):
                    print("-" * 80)
                    print("old:<" + record[6] + ">\nnew:<" + record[17] + ">\n")
                    choice = input("Do you want to create Replace rule ? y/n ")
                    if choice == 'y':
                        operation('r', replace_dict, record[6], record[17])
                        city_rules += 1
                    choice = input("Do you want to create Cut rule ? y/n ")
                    if choice == 'y':
                        operation('c', cut_dict, record[6], record[17])
                        city_rules += 1
                    pairs[record[17]].append(record[6])
                    # print_pairs(pairs)
    else:
        if record[18] != 'UNK':
            city_yes += 1

database_file.close()

if arguments.perform == "yes":
    replace_dict.close()
    cut_dict.close()

report_name = database + '_report_' + timestamp
report = open(report_name, "w")

report.write("Report:\n")
report.write("Country Level: " + str(country_yes) + " (YES) " + str(country_no) + " (NO) \n")
report.write("Country Rules: " + str(country_rules) + "\n")
report.write("Region Level: " + str(region_yes) + " (YES) " + str(region_no) + " (NO) \n")
report.write("Region Rules: " + str(region_rules) + "\n")
report.write("City Level: " + str(city_yes) + " (YES) " + str(city_no) + " (NO) \n")
report.write("City Rules " + str(city_rules))

report.close()
