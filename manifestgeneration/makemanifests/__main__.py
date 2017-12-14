from argparse import ArgumentParser
import csv
from os import _exit, listdir
from os.path import exists, join
import re

# def _build_canvas_list(pages, identifier):
#     out = []
#     for page in pages:
#         if '_' in page:
#             page = page.split('_')[1]
#             page = page.lstrip('0')
#         page = str(page).lstrip('0')
#         zfilled = page.zfill(4)
#         a_canvas = {}
#         a_canvas["@id"] = "http://iiif-manifest.lib.uchicago.edu/mvol-0001-0021-0000/canvas/c0",
#         a_canvas["@type"] = "sc:Canvas",
#         a_canvas["height"
#         a_canvas["width"] = 500,
#         a_canvas["label"] = "Page " + page
#         img = {}
#         img["@id"] = "http://iiif-manifest.lib.uchicago.edu/" + identifier + "/annotations/a0",
#         img["@type"] = "oa:Annotation",
#         img["motivation"] = "sc:painting",
#         img["on"] = "http://iif-manifest.lib.uchicago.edu/" + identifier + "/canvas/c0",
#         img["resource"] = {"@id": "http://digcollretriever.lib.uchicago.edu/retriever/" + identifier + "_" + zfilled + "/jpg?jpg_height=1000&jpg_width=500",
#                            "@type": "dctypes:Image",
#                            "format": "image/jpeg",
#                            "height": 1000,
#                            "width": 500
#                           }
#         a_canvas["images"] = [img]
#         out.append(a_canvas)
#     return out

def main():
    arguments = ArgumentParser()
    arguments.add_argument("cho_list_data", type=str, action='store')
    arguments.add_argument("data_root", action='store', type=str, default="Z:\IIIF_Files")
    parsed_args = arguments.parse_args()
    try:
        fields = []
        records = []
        missing_records = []
        on_disk_mvols = []
        validity_records = []
        with open(parsed_args.cho_list_data, "r", encoding="utf-8") as read_file:
            reader = csv.reader(read_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            count = 0
        
            for row in reader:
                date_as_entered = row[1]
                identifier = row[2]
                title = row[0]
                description = row[3]
                wrong_pattern_match = re.compile("(\d{1,2})[/](\d{1,2})[/](\d{4})").match(date_as_entered)
                range_pattern_match = re.compile("(\d{4}.*)[/](\d{4}.*)").match(date_as_entered)

                if wrong_pattern_match:
                    day = wrong_pattern_match.group(1).zfill(2)
                    month = wrong_pattern_match.group(2).zfill(2)
                    year = wrong_pattern_match.group(3)
                    valid_date = "{}-{}-{}".format(year, month, day)
                    date = valid_date
                elif range_pattern_match:
                    min_num = range_pattern_match.group(1)
                    max_num = range_pattern_match.group(2)
                    date1 = min_num
                    date2 = max_num
                    date = "{},{}".format(date1,date2)
                else:
                    date = date_as_entered
                content_path = join(parsed_args.data_root, *identifier.split('-'))
                if count > 0:
                    prelimb_page_filename_spec = re.compile("^\d{8}$")
                    limb_page_filename_spec = r"^" + identifier + r"[_]\d{4}$"                   
                    limb_page_filename_spec = re.compile(limb_page_filename_spec)
                    print(limb_page_filename_spec)
                    print(prelimb_page_filename_spec)
                    if not exists(content_path):
                        missing_record = [title, date, identifier, description]
                        missing_records.append(missing_record)
                    else:
                        record_row = row
                        record_row_headers = ["Title", "Date", "Identification", "Description",
                                              "num JPEG files", "num JPEG spec matches",
                                              "num TIFF files", "num TIFF spec matches",
                                              "num POS files", "num POS spec matches",
                                              "num ALTO files", "num ALTO spec matches",
                                              "spec_type",
                                             ]
                        content_path_base_contents = listdir(content_path)
                        valid_contents1 = ['ALTO', 'TIFF', 'JPEG', identifier+'.pdf',
                                           identifier+'.struct.txt', identifier+'.dc.xml']
                        valid_contents2 = ['jpg', 'xml', 'tif', identifier+'.pdf', 
                                           identifier+'.txt', identifier+'.dc.xml']
                        check_option1 = set(valid_contents1) - set(content_path_base_contents)
                        check_option2 = set(valid_contents2) - set(content_path_base_contents)
                        if not check_option1 and check_option2:
                            check_type = "post-limb"
                            alto_file_contents = listdir(join(content_path, 'ALTO'))
                            jpeg_file_contents = listdir(join(content_path, 'JPEG'))
                            tiff_file_contents = listdir(join(content_path, 'TIFF'))
                            num_alto_files = len(alto_file_contents)
                            num_jpeg_files = len(jpeg_file_contents)
                            num_tiff_files = len(tiff_file_contents)
                            tif_spec_matches = [limb_page_filename_spec.match(x.split('.')[0])
                                                for x in tiff_file_contents]
                            jpg_spec_matches = [limb_page_filename_spec.match(x.split('.')[0])
                                                for x in jpeg_file_contents]
                            alto_spec_matches = [limb_page_filename_spec.match(x.split('.')[0])
                                                 for x in alto_file_contents]
                            num_tif_spec_matches = len(tif_spec_matches) 
                            num_jpeg_spec_matches = len(jpg_spec_matches) 
                            num_alto_spec_matches = len(alto_spec_matches) 
                            record_row += [
                                num_jpeg_files,
                                num_jpeg_spec_matches,
                                num_tiff_files,
                                num_tif_spec_matches,
                                0,
                                0,
                                num_alto_files,
                                num_alto_spec_matches,
                                check_type,

                            ]
                        elif not check_option2 and check_option1:
                            check_type = "pre-limb"
                            pos_file_contents = listdir(join(content_path, 'pos'))
                            jpg_file_contents =listdir(join(content_path, 'jpg'))
                            tif_file_contents =listdir(join(content_path, 'tif'))
                            num_pos_files = len(pos_file_contents)
                            num_jpg_files = len(jpg_file_contents)
                            num_tif_files = len(tif_file_contents)

                            tif_spec_matches = [prelimb_page_filename_spec.match(x.split('.')[0])
                                                for x in tif_file_contents]
                            jpg_spec_matches = [prelimb_page_filename_spec.match(x.split('.')[0])
                                                for x in jpg_file_contents]
                            pos_spec_matches = [prelimb_page_filename_spec.match(x.split('.')[0])
                                                for x in pos_file_contents]
                            num_tif_spec_matches = len(tif_spec_matches) 
                            num_jpg_spec_matches = len(jpg_spec_matches) 
                            num_pos_spec_matches = len(pos_spec_matches)                            
                            record_row += [
                                num_jpg_files,
                                num_jpg_spec_matches,
                                num_tif_files,
                                num_tif_spec_matches,
                                num_pos_files,
                                num_pos_spec_matches,
                                0,
                                0,
                                check_type,
                            ]
                        else:
                            check_type = "undeterminable"
                        on_disk_mvols.append(record_row)
                        print(record_row_headers)
                        print(record_row)
                else:
                    fields = row
                count += 1
        with open("metadata_files/missing_mvol_issues.csv", "w+", encoding="utf-8") as write_file:
            writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["Title", "Date", "Identification", "Description"])
            for row in missing_records:
                writer.writerow(row)
        with open("metadata_files/ondisk_mvol_issues_report.csv", "w+", encoding="utf-8") as write_file:
            writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["Identification", "Valid", "Valdiation Type"])
            for row in on_disk_mvols:
                writer.writerow(row)

            # identifier = n.split("mvol")[1]
            # identifier = identifier.split("\\")
            # identifier[0] = "mvol"
            # print(identifier)
            # series = identifier[0] + '-' + identifier[1]
            # series_info = METADATA[series]
            # issue = identifier[-1].lstrip('0')
            # if issue == "":
            #     issue = "0"
            # identifier = "-".join(identifier)
            # outp = {}
            # outp["@context"] = "http://iiif.io/api/presentation/2/context.json"
            # outp["@id"] = "http://iiif-manifest.lib.uchicago.edu/manifest.json"
            # outp["@type"] = "sc:Manifest"
            # outp["label"] = series_info["title"] + " Issue " + issue
            # outp["description"] = series_info["description"]
            # outp["metadata"] = [] 
            # outp["metadata"].append({"label": "Title", "value": series_info["title"]})
            # outp["metadata"].append({"label": "Date", "value": ""})
            # outp["metadata"].append({"label": "Identifier", "value": identifier})
            # outp["license"] =  "http://campub.lib.uchicago.edu/rights/"
            # seq = {}
            # seq["@id"] = "http://iiif-manifest.lib.uchicago.edu/" + identifier + "/sequence/s0",
            # seq["@type"] = "sc:Sequence",
            # seq["label"]  = ""
            # seq["rendering"]  = {
            #     "@id": "http://digcollretriever.lib.uchicago.edu/retriever/" + identifier + "/pdf",
            #     "format": "application/pdf",
            #     "label": "Download as PDF"
            # }
            # seq["viewingHint"] = "paged"
            # seq["canvases"] = []
            # try:
            #     n_path = join(n, "tif")
            #     pages = listdir(n_path)
            # except:
            #     n_path = join(n, "TIFF")
            #     pages = listdir(n_path)
            # pages = [x.split(".tif")[0] for x in pages]
            # np = []
            # for p in pages:
            #     if '_' in p:
            #         p = p.split('_')[1]
            #     else:
            #         p = p
            #     p = int(p.lstrip('0'))
            #     np.append(p)
            # canvases = _build_canvas_list(pages, identifier)
            # seq["canvas"] = canvases
            # outp["sequences"] = seq
            # json_file_name = identifier + ".json"
            # json_file_path = "Z:\\IIIF_Manifests\\" + json_file_name
            # with open(json_file_path, "w", encoding="utf-8") as write_file:
            #     json.dump(outp, write_file, indent=4)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
