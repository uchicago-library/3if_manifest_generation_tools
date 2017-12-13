
import csv

if __name__ == "__main__":
    csvs_with_ids = ["./metadata_files/mvol-0001.csv",
                     "./metadata_files/mvol-0002.csv",
                     "./metadata_files/mvol-0004.csv",
                     "./metadata_files/mvol-0005.csv",
                     "./metadata_files/mvol-0006.csv",
                     "./metadata_files/mvol-0007.csv",
                     "./metadata_files/mvol-0075.csv",
                     "./metadata_files/mvol-0445.csv",
                     "./metadata_files/mvol-0500.csv",
                     "./metadata_files/mvol-0501.csv",
                     "./metadata_files/mvol-0502.csv",
                     "./metadata_files/mvol-0503.csv",
                     "./metadata_files/mvol-0504.csv",
                     "./metadata_files/mvol-0506.csv",
                     "./metadata_files/mvol-0510.csv",
                    ]
    records = []
    for n_filepath in csvs_with_ids:
        with open(n_filepath, "r", encoding="utf-8") as read_file:
            reader = csv.reader(read_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            count = 0
            for row in reader:
                if count > 0:
                    if len(row) > 4:
                        records.append(row)
                    else:
                        row = [x.strip() for x in row]
                        row.append("")
                        records.append(row)
                else:
                    pass
                count += 1
    with open("./metadata_files/mvols.csv", "w+", encoding="utf-8") as write_file:
        csv_writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(["Title", "Date", "Identification", "Description", "Notes"])
        for record in records:
            csv_writer.writerow(record)
