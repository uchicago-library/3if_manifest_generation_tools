
from .Canvas import Canvas

class Sequence(object):
    def __init__(self, base_id, seq_data, count):
        self.base_id = base_id
        self.id = "http://iiif-manifest.lib.uchicago.edu/" + base_id + "/s" + str(count)
        self.type = "sc:Sequence"
        self.label = ""
        self.canvases = []

    def add_canvas(self, canvas_data):
        count = len(self.canvases)
        c = Canvas(self.base_id, canvas_data, count)
        self.canvases.append(c)

    def validate(self):
        errors = []
        for a_canvas in self.canvases:
            check = a_canvas.validate()
            if not check[0]:
                errors += check[1]
        if errors:
            return (False, errors)
        else:
            return (True,)