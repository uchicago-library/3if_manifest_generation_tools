from argparse import ArgumentParser
import csv
from pymarc import MARCReader
from os import scandir
from os.path import basename, dirname, split as path_split, join
import re

def find_files(path):
    for n in scandir(path):
        if n.is_dir():
            yield from find_files(n.path)
        elif n.is_file() and n.path.endswith("mrc"):
            yield n.path

def find_files_matching_a_pattern(path, file_string):
    for n in scandir(path):
        if n.is_dir():
            yield from find_files_matching_a_pattern(n.path, file_string)
        elif n.is_file():
            if file_string in n.path:
                yield n.path

if __name__ == "__main__":
    records = []
    csv_records = []
    mdata_files = find_files("Z:\IIIF_Files\HistoricalChicagoMaps1890")
    arguments = ArgumentParser(description="A tool to extract metadata from DLDC maps deposits to LDR")
    arguments.add_argument("path_to_files", help="location of the files", action='store', type=str)
    parsed = arguments.parse_args()
    mdata_files = find_files(parsed.path_to_files)
    for n in mdata_files:
        with open(n, "rb") as read_file:
            reader = MARCReader(read_file)
            for record in reader:
                title = record.title()
                author = record.author()
                publisher = record.publisher()
                pubyear = record.pubyear()
                subjects = '.'.join([x.value() for x in record.subjects()])
                series = [x.value() for x in record.series()]
                identifier = basename(n).split('.')[0]
                i = n.split(parsed.path_to_files)[1].split("\\")[1]
                the_dir = join(parsed.path_to_files, i)
                image_files = find_files_matching_a_pattern(the_dir, identifier)
                relevant_files = [re.sub(r"\\", "/", x.split(parsed.path_to_files)[1])
                                  for x in image_files if x.endswith("tif")]
                relevant_files = ','.join(['/'.join(x.split('/')[1:]) for x in relevant_files])
                rec = [title, author, publisher, pubyear, subjects, ','.join(series), basename(n).split('.')[0], relevant_files, i]
                records.append(rec)

    with open("./metadata_files/chimaps_1890.csv", "w+", encoding="utf-8", newline='') as write_file:
        writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        fields = ['title', 'author', 'publisher', 'pubyear', 'subjects', 'series', 'identifier', "file_locations", "ldr_accession"]
        writer.writerow(fields)
        for record in records:
            writer.writerow(record)

        

