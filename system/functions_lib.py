from flask import Response
import json

def response(data=None,code=200,message='Success'):
	res = {"data":data,
    		'meta': {
    			'message': message,
				'code': code
				}
			}
	result = json.dumps(res)
	resp = Response(result, status=code, mimetype='application/json')
	return resp