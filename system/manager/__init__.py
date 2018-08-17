from flask_script import Manager, Command, Server
from system import app, running, db
import create_module

managers = Manager(app, usage="Pentools CLI", with_default_commands=False)

managers.add_command('create:module', create_module.Create())
managers.add_command('run', running)

@managers.command
def test():
	""" Testing script """
	print "nop"

@managers.command
def init_db():
	""" To migrate db after create module """
	db.create_all()
	print "Pentools ==> Initialing_database success"
	
