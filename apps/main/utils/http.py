from django.http import HttpResponse
from django.utils import simplejson as json


class JsonResponse(HttpResponse):
    def __init__(self, data=None, errors=None, success=True):
      """
      data is a dict, errors a list
      """
      data = data or {}
      errors = errors or []
      data.update({
            'errors': errors,
            'success': len(errors) == 0 and success,
        })
      json_data = json.dumps(data)
      super(JsonResponse, self).__init__(json_data, mimetype='application/json')
