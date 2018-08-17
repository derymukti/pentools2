from flask_script import Manager, Command, Option
import sys, os
from termcolor import colored

class Create(Command):
	
	help_args = ('-h', '--help')
	help = "Create Module"
	option_list = (
        Option('--name', '-n', dest='name'),
    )
	def create_folder(self,name):
		directory = 'modules/'+name
		if not os.path.exists(directory):
			os.makedirs(directory)
		if not os.path.exists(directory+'/views'):
			os.makedirs(directory+'/views')
		if not os.path.exists(directory+'/controller'):
			os.makedirs(directory+'/controller')
		# if not os.path.exists(directory+'/model'):
		# 	os.makedirs(directory+'/model')

		try:
			with open(directory+'/__init__.py','w') as f:
				f.write(' ')
				f.close()
		except Exception as err:
			print err

		print "Pentools ==> "+directory+" ::::>> Created"
		print "Pentools ==> "+directory+"/views ::::>> Created"
		print "Pentools ==> "+directory+"/controller ::::>> Created"
		print "Pentools ==> "+directory+"/model ::::>> Created"
		print "Pentools ==> ", colored("modules/"+name+"/model/__init__.py","red")
		print colored("		edit this model file before run init_db","red")
		print "Pentools ==> read github.com/derymukti/pentools2"
		return directory
	def create_template(self, name):
		try:
			with open('modules/'+name+'/views/index.html','w') as f:
				f.write('/'+name)
				f.close()
		except Exception as err:
			print err

	def add_to_route(self,name):
		try:
			with open('modules/router.py','r') as f:
				f.seek(0)
				data = f.readlines()
				a = len(data) - 1
				f.close()
				add_module = "\n\nfrom "+name+".controller import "+name+"\n"
				register_module = "app.register_blueprint("+name+")\n"
				d = open('modules/router.py','w')
				data.insert(6,add_module)
				data.insert(7,register_module)
				d.writelines(data)
				d.close()
		except Exception as err:
			print err

		self.create_template(name)

	def create_controller(self,name):
		directory = self.create_folder(name)
		self.add_to_route(name)
		# self.create_model(name)
		try:
			with open(directory+'/controller/__init__.py', 'w') as f:
				f.write("from system.library import * \n")
				f.write("from system import db,secret\n")
				f.write("from modules import model\n")
				f.write("import md5\n")
				f.write("from system.middleware import *\n\n")
				f.write(name+" = Blueprint('"+name+"', __name__, \n")
				f.write("				template_folder='"+directory+"' , url_prefix='/"+name+"')\n")
				f.write("@"+name+".route('/', defaults={'page': 'index'})\n")
				f.write("@"+name+".route('/<page>') \n")
				f.write("def show(page): \n")
				f.write("	try: \n")
				f.write("		return render_template('"+name+"/views/%s.html' % page) \n")
				f.write("	except TemplateNotFound: \n")
				f.write("		abort(404)\n\n")
				f.write("@"+name+".route('/login',methods=['POST'])\n")
				f.write("def login():\n")
				f.write("	if request.method == 'POST':\n")
				f.write("		data = request.headers['authorization']\n")
				f.write("		return model.create_token(data,'"+name+"')\n")
				f.write("@"+name+".route('/insert_something',methods=['POST'])\n")
				f.write("@login_require\n")
				f.write("def insert_something():\n")
				f.write("	data = request.get_json()\n")
				f.write("	if(model.insert('"+name+"',data) is not 'err'):\n")
				f.write("		return response(data=data,code=201)\n")
				f.write("	else:\n")
				f.write("		return response(code=400,message='Failed')\n")
				f.write("@"+name+".route('/update_something',methods=['POST'])\n")
				f.write("@login_require\n")
				f.write("def update_something():\n")
				f.write("	data = request.get_json()\n")
				f.write("	if(model.update('"+name+"',data) is not 'err'):\n")
				f.write("		return response(data=data,code=200)\n")
				f.write("	else:\n")
				f.write("		return response(code=400,message='Failed')\n")
				f.write("@"+name+".route('/list_something',methods=['GET'])\n")
				f.write("@login_require\n")
				f.write("def list_something():\n")
				f.write("	limit = 50\n")
				f.write("	if request.args:\n")
				f.write("		limit = request.args['limit']\n")
				f.write("	return model.select_json(table='"+name+"',limit=limit)\n")				
				f.close()
		except Exception as err:
			print err

	def run(self, name):
		self.create_controller(name)
			
	