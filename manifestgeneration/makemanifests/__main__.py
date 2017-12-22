from argparse import ArgumentParser
import csv
from os import listdir
from os.path import join, exists
import re

def main():
    arguments = ArgumentParser()
    arguments.add_argument("cho_list_data", type=str, action='store')
    arguments.add_argument("data_root", action='store', type=str, default="Z:\IIIF_Files")
    parsed_args = arguments.parse_args()

    try:
        with open(parsed_args.cho_list_data, "r", encoding="utf-8") as read_file:
            fields = ["Title",
                      "Date",
                      "Identification",
                      "Description",
                      "Notes",
                      "num JPEG files",
                      "num JPEG spec matches",
                      "num TIFF files",
                      "num TIFF spec matches",
                      "num POS files",
                      "num POS spec matches",
                      "num ALTO files",
                      "num ALTO spec matches",
                      "spec_type"
                     ]
            reader = csv.DictReader(read_file, fieldnames=fields,
                                    delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_ALL)
            for row in reader:
                identifier = row["Identification"]
                prelimb_page_filename_spec = re.compile(r"^(\d{8})$")
                limb_page_filename_spec = r"^(" + identifier + r"[_]\d{4})$"                   
                limb_page_filename_spec = re.compile(limb_page_filename_spec)
                spec_type = row["spec_type"]
                id_parts = row["Identification"].split('-')
                if spec_type == 'post-limb':
                    page_dir = join(parsed_args.data_root, *id_parts, 'TIFF')                   
                    pages = [join(*id_parts, limb_page_filename_spec.match(x.split('.')[0]).group(1))
                             for x in listdir(page_dir) if limb_page_filename_spec.match(x.split('.')[0])]
                elif spec_type == 'pre-limb':
                    page_dir = join(parsed_args.data_root, *id_parts, 'tif')
                    pages = [join(*id_parts, prelimb_page_filename_spec.match(x.split('.')[0]).group(1)) for x in listdir(page_dir)]
                else:
                    page_dir = None
                    pages = []
                for page in pages:
                    print(page)

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
