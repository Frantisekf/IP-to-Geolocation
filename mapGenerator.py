import doctest
import folium
import csv


class MapGenerator:
    # ctor
    def __init__(self, delimiter, file_path):
        self.file_path = file_path
        self.delimiter = delimiter

    map = folium.Map(location=[0, 0], zoom_start=1)

    # file_path = "/home/ferko/Dropbox/school/Bakalarka/Stefan_zima/Zdrojove Subory/Ziskavanie Geolokacnych Dat/input.dat"


    def generate_html(self):
        with open(self.file_path) as tsv:
            for line in csv.reader(tsv, delimiter=self.delimiter):
                print(line[1])
                id_number = line[0]
                name = line[2]
                ip_address = line[1]
                latitude = line[9]
                longitude = line[10]
                folium.Marker([latitude, longitude], popup=id_number + ": " + ip_address + " - " + name).add_to(map)

    map.save('map.html')


if __name__ == "__main__":
    doctest.main()
