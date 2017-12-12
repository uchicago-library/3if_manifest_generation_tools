import csv
from os import scandir, listdir
from os.path import exists, join
import re
from xml.etree import ElementTree as ET

def _find_issues(path):
    for a_thing in scandir(path):
        if a_thing.is_dir():
            matchable = re.compile(r"mvol[\\]0007[\\]\d{4}[\\]\d{4}$").search(a_thing.path)
            if matchable: 
                yield a_thing.path
            yield from _find_issues(a_thing.path)
        else:
            pass


if __name__ == "__main__":
    scanned_files = _find_issues("Z:\IIIF_Files\mvol\\0007")
    records = []
    for n in scanned_files:
        dir = n
        contents = listdir(n)
        the_id = '-'.join(n.split("Z:\IIIF_Files\\")[1].split("\\"))
        dc_file_name = the_id + ".dc.xml"
        dc_file_path = join(n, dc_file_name)
        if exists(dc_file_path):
            xml = ET.parse(dc_file_path).getroot()
            title = xml.find("title").text
            date = xml.find("date").text
            description = xml.find("description").text
            dc_id = xml.find("identifier").text
            record = [title, date, dc_id, description]
            records.append(record)

    with open("./metadata_files/mvol-0007.csv", "w+", encoding="utf-8") as write_file:
        a_writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        a_writer.writerow(["Title", "Date", "Identification", "Description"])
        for row in records:
            a_writer.writerow(row)
