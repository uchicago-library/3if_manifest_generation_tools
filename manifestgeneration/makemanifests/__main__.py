from argparse import ArgumentParser
from os import _exit, scandir, listdir
from os.path import exists, join
import json
import re
import string

def _find_issues(path):
    for a_thing in scandir(path):
        if a_thing.is_dir():
            matchable = re.compile(r"mvol[\\]\d{4}[\\]\d{4}[\\]\d{4}$").search(a_thing.path)
            if matchable: 
                yield a_thing.path
            yield from _find_issues(a_thing.path)
        else:
            pass

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
    parsed_args = arguments.parse_args()
    try:
        of = 
        fields = []
        records = []
        with open(parsed.cho_list_data, "r", encoding="utf-8") as read_file:
            reader = csv.reader(read_file, delimiter=',', quoting='"', quotechar=csv.QUOTE_ALL)
            count = 0
            for row in reader:
                if count > 0:
                    records.append(row)
                else:
                    fields = row
                count += 1

        for n_item in scanned_files:
            print(n_item)
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
