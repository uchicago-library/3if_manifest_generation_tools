
from .Resource import Resource

class Image(object):
    def __init__(self, base_id, img_data, count):
        self.base_id = base_id
        self.the_id = "http://iiif-manifest.lib.uchicago.edu/" + base_id + "/annotations/a" + str(count)
        self.type = "oa:Annotation"
        self.motivation = "sc:Painting"
        self.resources = []

    def add_resource(self, resource_data):
        count = len(self.resources)
        r = Resource(self.base_id, resource_data)
        self.resources.append(resource_data)

    def validate(self):
        errors = []
        for resource in self.resources:
            check = resource.validate()
            if not check[0]:
                errors += check[1]
        if errors:
            return (False, errors)
        else:
            return (True,)
