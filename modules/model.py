from system import db,secret, token_expired, today, now
from basicauth import decode
import sys, os, decimal, time, md5, json
from jose import jwt
from system.functions_lib import *
from basicauth import decode
from flask import session, jsonify
from datetime import datetime

def insert(table,data_post,data="Success"):
    try:
        columns = ', '.join(data_post.keys())
        values = '", "'.join(str(v) for v in data_post.values())
        placeholders = ', '.join('?' * len(data_post))
        sql = 'INSERT INTO %s (%s) VALUES ("%s")' % (table,columns, str(values))
        cur = db.query(sql)
        try:
            res=cur.lastrowid
        except:
            res = "success"
        print "insert success"
        cur.close()
        return res
    except:
        print "insert error"
        return "err"
    
def select_json(table='',column='*',where='1',value='1',limit='10',order='id',sortir='DESC'):
    try:
        value_isi = value.split()
        if value_isi[0]=="like":
            sql = "SELECT %s FROM %s WHERE %s='%s' AND %s like '%s%%' order by %s %s LIMIT %s" % (column,table,where,value_isi[1],value_isi[2],value_isi[3],order,sortir,limit)
        elif value_isi[0]=="and":
            sql = "SELECT %s FROM %s WHERE %s='%s' AND %s='%s' order by %s %s LIMIT %s" % (column,table,where,value_isi[1],value_isi[2],value_isi[3],order,sortir,limit)
        else:
            sql = "SELECT %s FROM %s WHERE %s='%s' order by %s %s LIMIT %s" % (column,table,where,value,order,sortir,limit)
        #print sql
        cur = db.query(sql)
        columns = cur.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cur.fetchall()]
        cur.close()
        if result == []:
            # data = {"data":result,"meta":{"code":404,"status":"Data Not Found"}}
            return response(data=result,code=404,message="Data Not Found")
        else:
            try:
                data = json.dumps(result,default=decimal_default)
            
                data = json.loads(data)
                return response(data=data,code=200,message="Success")
            except:
                data = json.dumps(result,default=datetime_handler)
            
                data = json.loads(data)
                return response(data=data,code=200,message="Success")
        #db.commit()
        
       # cur.close()
        print "cursor closed select_json"
        return jsonify(data)
        #db.close()

    except Exception as e:
        #cur.close()
        #print "cursor closed select_json failed"
        return response(code=501,message=e)
    
    #db.close()
def update(table,data_post,data={"status":"Success"}):
    
    try:
        columns = ', '.join(data_post.keys())
        values = '", "'.join(data_post.values())
        placeholders = ', '.join('?' * len(data_post))
        sql = 'REPLACE INTO %s (%s) VALUES ("%s")' % (table,columns, str(values))
        cur = db.query(sql)
       # db.commit()
       # cur.close()     
        cur.close()
        time.sleep(0.1)
        print sql

        res=data
        
        print "cursor closed update"
        return response(data=res,code=200,message="Update Success")
        
        
    except :
        #cur.close()
        print "cursor closed update failed"
        return jsonify(data_post)
    #db.close()
   
def one_update(table=None,where=None,where_value=None,setcol=None,set_value=None,and_where=None,and_where_value=None):
    
    try:
        if and_where:
            sql = 'UPDATE `%s` SET `%s`="%s" WHERE `%s`=%s AND `%s`=%s;' % (table,setcol,set_value,where,where_value,and_where,and_where_value)
        else:
            sql = 'UPDATE `%s` SET `%s`="%s" WHERE `%s`=%s;' % (table,setcol,set_value,where,where_value)
        print sql
        cur = db.query(sql)

        cur.close()
        time.sleep(0.1)
        print "success update one"
        return "success"
    except:
       
        print "failed update one"
        return "failed"




def create_token(data,status):
    username, password = decode(data)
    password = md5.new(password + secret).hexdigest()
    ses = md5.new(username+password).hexdigest()
    
    try:
        res = jwt.decode(session.get(ses),secret,algorithms=['HS256'])
        data = {"token":session.get(ses)}
        return response(data=data,code=200,message="Token Not Expired")

    except jwt.ExpiredSignatureError:
        del session[ses]
        
        if(status=='user'):
            
            sql = "SELECT id,username FROM users WHERE username='%s' AND password='%s'" % (username,password)
            cur = db.query(sql)
            res = cur.fetchone()
            cur.close()
            result = {
                "id":res[0],
                "username":res[1],
                "status":"user",
                "exp": token_expired
                }
        elif(status=='admin'):
            sql = "SELECT id,username FROM admins WHERE username='%s' AND password='%s'" % (username,password)
            cur = db.query(sql)
            res = cur.fetchone()
            cur.close()
            result = {
                "id":res[0],
                "username":res[1],
                "status":"admin",
                "exp": token_expired
                }

        print 'processing create token'
        token = jwt.encode(result, secret, algorithm='HS256')
        session[ses] = token
        print "token refreshed"
        
        data = {"token":token}
      
        print "cursor closed token login refresh"
        
        time.sleep(0.1)
        return response(data=data,code=200,message="Token Refreshed")

        
    except:
        
        try:
            
            if(status=='user'):
            
                sql = "SELECT id,username FROM users WHERE username='%s' AND password='%s'" % (username,password)
                cur = db.query(sql)
                res = cur.fetchone()
                cur.close()
                result = {
                    "id":res[0],
                    "username":res[1],
                    "status":"user",
                    "exp": token_expired
                    }
            elif(status=='admin'):
                sql = "SELECT id,username FROM admins WHERE username='%s' AND password='%s'" % (username,password)
                cur = db.query(sql)
                res = cur.fetchone()
                cur.close()
                result = {
                    "id":res[0],
                    "username":res[1],
                    "status":"admin",
                    "exp": token_expired
                    }

            print 'processing create token'
            token = jwt.encode(result, secret, algorithm='HS256')
            session[ses] = token
            print "token created"
            #db.commit()
            data = {"token":token}
           # cur.close()
            print "cursor closed token login login"
            
            time.sleep(0.1)
            return response(data=data,code=200,message="Login Success")
            #cur.close()
            #db.close()

        except:
            #cur.close()
            #print "cursor closed token login failed"
            return response(code=403,message="Login Failed")
            

def response(data=None,code=200,message='Success'):
    res = {"data":data,'meta': {'message': message, 'code': code}}
    res = json.dumps(res)
    resp = Response(res, status=code, mimetype='application/json')
    return resp


def cek_token(token):
    try:
        res = jwt.decode(token,secret,algorithms=['HS256'])
        if(res['status']=="admin"):
            return True

    except jwt.ExpiredSignatureError:
        return False
    except:
        return False
    else:
        return False



def select_one(table=None,column=None,where=None,where_value=None):
   
    try:
        if where:
            sql= """SELECT %s FROM %s WHERE %s='%s' """ % (column,table,where,where_value)
        else:
            sql= """SELECT %s FROM %s""" % (column,table)
        cur = db.query(sql)
        data = cur.fetchone()
        cur.close()
        time.sleep(0.1)
        print "cursor closed select_one"
        print sql
        return data[0]
        #cur.close()
        #db.close()
        
    except:
        #cur.close()
        #print "cursor closed select_one failed"
        return response(data=None,code=500,message="Error")
    
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise decimal_default(x)