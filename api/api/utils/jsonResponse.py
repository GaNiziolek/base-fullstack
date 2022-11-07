import json

class jsonResponse(object):
    def __init__(self, x):
        self.x = x
    
    def __json__(self, request):
        return json.dumps(
            self.x, 
            indent=4, 
            sort_keys=True, 
            default=str
        )
