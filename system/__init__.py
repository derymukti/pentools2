from flask import Flask
from flask_script import Server
import sys , json, MySQLdb, redis
from datetime import datetime, timedelta
from flask_session import Session

app = Flask(__name__)

try:
	with open('config.json') as data:
		data_json = json.loads(data.read())
		db_host = data_json['db']['db_host']
		db_user = data_json['db']['db_user']
		db_pass = data_json['db']['db_pass']
		db_name = data_json['db']['db_name']
		host = data_json['host']
		port = data_json['port']
		debug = data_json['debug']
		secret = data_json['secret']
		
except Exception as err:
	print err	

SESSION_TYPE = 'redis'
SESSION_REDIS = redis.Redis(host="localhost",port=6379,db=0)
app.config.from_object(__name__)
Session(app)

expired = data_json['token_expired']
token_expired = datetime.now() + timedelta(hours=expired)
now = datetime.now()
f = '%Y-%m-%d'
today = now.strftime(f)

class DB:
  conn = None

  def connect(self):
    self.conn = MySQLdb.connect(db_host,db_user,db_pass,db_name)
    self.conn.autocommit(True)
  def query(self, sql):
    try:
      cursor = self.conn.cursor()
      cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute(sql)
      
    return cursor
  def close(self):
    self.conn.close()


db = DB()

running = Server(host=host,port=port,use_debugger=debug,use_reloader=True)
import manager

