
from .Sequence import Sequence

class Manifest(object):
    def __init__(self, manifest_data): 
        self.sequences = []
        self.label = ""
        self.base_id = ""
        self.context = "http://iiif.io/api/presentation/2/context.json"
        self.id = "http://iiif-manifest.lib.uchicago.edu/manifest.json"
        self.type = "sc:Manifest"

    def add_sequence(self, seq_data):
        count = len(self.sequences)
        s = Sequence(self.base_id, seq_data, count)

    def validate(self):
        errors = []
        for seq in self.sequences:
            check = seq.validate()
            if not check[0]:
                errors += check[1]
        if errors:
            return (False, errors)
        else:
            return (True,)
