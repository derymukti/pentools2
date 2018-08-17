from functions_lib import *
from flask import request
from functools import wraps
from jose import jwt
from system import secret

def login_require(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		try:
			token = request.headers['authorization']
			res = jwt.decode(token,secret,algorithms=['HS256'])
			if res['status'] != "admin":
				return res['status']
			
			return f(*args, **kwargs)
		except:
			return response(code=403,message="Forbidden")
	return decorated_function

