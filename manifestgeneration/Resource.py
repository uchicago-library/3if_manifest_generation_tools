import requests

class Resource(object):
    def __init__(self,  base_id, resource_datat):
        self.base_id = base_id
        self.the_id = ""
        self.format = ""
        self.type = ""
        self.height = ""
        self.width = ""


    def validate(self):
        errors = []
        req = requests.get(self.the_id)
        if req.status_code == 200:
            pass
        else:
            return (False, ["{} cannot be resolved".format(self.the_id)])

    def __str__(self):
        return "<Resource: {} ({})>".format(self.the_id, self.format)