
if __name__ == "__main__":
    csvs_with_ids = ["./metadata_files/mvol-0001.csv",
                     "./metadata_files/mvol-0002.csv",
                     "./metadata_files/mvol-0004.csv",
                     "./metadata_files/mvol-0005.csv",
                     "./metadata_files/mvol-0006.csv",
                     "./metadata_files/mvol-0007.csv",
                     "./metadata_filesmvol-0075.csv",
                     "./metadata_files/mvol-0445.csv",
                     "./metadata_files/mvol-0500.csv",
                     "./metadata_files/mvol-0501.csv",
                     "./metadata_files/mvol-0502.csv",
                     "./metadata_files/mvol-0503.csv",
                     "./metadata_files/mvol-0504.csv",
                     "./metadata_files/mvol-0506.csv",
                     "./metadata_files/mvol-0510.csv",
    no_csv_ids = "mvol-0007"
    records = []
    for n_filepath in csvs_with_ids:
        with open(open(n_filepath, "r", encoding="utf-8")) as read_file:
            reader = csv.reader(read_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            count = 0
            for row in reader:
                if count > 0:
                    records.append(row)
                else:
                    pass
                count += 1