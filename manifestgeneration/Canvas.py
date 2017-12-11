
from .Image import Image

class Canvas(object):
    def __init__(self, base_id, canvas_data, count):
        self.base_id = base_id
        self.id = "http://iiif-manifest.lib.uchicago.edu/" + base_id + "/canvas/c" + str(count)
        self.images = []
        self.type = "sc:Canvas"

    def add_image(self, img_data):
        count = len(self.images)
        i = Image(self.base_id, img_data, count)
        self.images.append(i)

    def validate(self):
        errors = []
        for img in self.images:
            check = img.validate()
            if not check:
                errors.append("Image {} is not valid".format(str(img)))
        if errors:
            return (False, errors)
        else:
            return (True,)