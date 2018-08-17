from system import app
from system.library import *
my_loader = jinja2.ChoiceLoader([app.jinja_loader,jinja2.FileSystemLoader(['modules'])])
app.jinja_loader = my_loader







@app.errorhandler(404)
def page_not_found(e):
	return response(code=404,message="Endpoint not Found")

@app.errorhandler(405)
def page_not_found(e):
	return response(code=405,message="Method not allowed")

@app.errorhandler(502)
def page_not_found(e):
	return response(code=502,message="Internal Server Error")
