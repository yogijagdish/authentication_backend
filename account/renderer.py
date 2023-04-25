from rest_framework import renderers
import json

## important for frontend as it hepls to seprate whether the response send by backend is errror or valid data
class ErrorRenderes(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'error':data})
        else:
            response = json.dumps(data)
        return response
