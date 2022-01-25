import sqlite3 as sql

from functools import wraps
from flask import session,flash,redirect,url_for

connect_db ='PYTHON.PROJECT.db' 

def data_pemain():
  with sql.connect(connect_db) as db:
    qry = 'select * from pemain' 
    result=db.execute(qry)
    return(result)

def data_pasukan():
  with sql.connect(connect_db) as db:
    qry = 'select * from pasukan' 
    result=db.execute(qry)
    return(result)

def data_gaji_pemain():
  with sql.connect(connect_db) as db:
    qry = 'select * from gajii' 
    result=db.execute(qry)
    return(result)


#list_stu_sub_grade()


def result():
  rows=data_pemain()
  rows=data_pasukan()
  rows=data_gaji_pemain()
  for row in rows:
    print (row)
    
def insert_pemain(id_pemain,nama_pemain,umur,no_jersi,posisi,gred_pemain):
  with sql.connect(connect_db) as db:
    qry='insert into pemain (id_pemain,nama_pemain,umur,no_jersi,posisi,gred_pemain) values (?,?,?,?,?,?)' 
    db.execute(qry,(id_pemain,nama_pemain,umur,no_jersi,posisi,gred_pemain))
    
def update_pemain(nama_pemain,umur,no_jersi,posisi,gred_pemain,id_pemain):
  with sql.connect(connect_db) as db:
    qry='update pemain set nama_pemain=?,umur=?,no_jersi=?,posisi=?,gred_pemain=? where id_pemain=?' 
    db.execute(qry, (nama_pemain,umur,no_jersi,posisi,gred_pemain,id_pemain))
    
def find_pemain(id_pemain):
  with sql.connect(connect_db) as db:
    qry = 'select * from pemain where id_pemain=?'
    result=db.execute(qry,(id_pemain,)).fetchone()
    return(result)

def check_pemain(id_pemain):
  with sql.connect(connect_db) as db: 
    qry = 'select id_pemain from pemain where id_pemain=?'
    result=db.execute(qry,(id_pemain,)).fetchone()
    return(result)

def delete_pemain(id_pemain):
  with sql.connect(connect_db) as db:
    qry='delete from pemain where id_pemain=?' 
    db.execute(qry,(id_pemain,))

def insert_gaji(id_pemain,id_pasukan,no_resit_gaji,jum_gaji_ditetapkan,cukai_pemain,imbuhan_mvp,jum_gaji_bersih):
  with sql.connect(connect_db) as db:
    qry='insert into gajii (id_pemain,id_pasukan,no_resit_gaji,jum_gaji_ditetapkan,cukai_pemain,imbuhan_mvp,jum_gaji_bersih) values (?,?,?,?,?,?,?)' 
    db.execute(qry,(id_pemain,id_pasukan,no_resit_gaji,jum_gaji_ditetapkan,cukai_pemain,imbuhan_mvp,jum_gaji_bersih))


# helper function

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
        return f(*args, **kwargs)
    else:
        flash("You need to login first")
        return redirect(url_for('home'))
  return wrap

def checklogin(username,password):
  with sql.connect(connect_db) as db: 
    qry = 'select username,password from users where username=? and password=?'
    result=db.execute(qry,(username,password)).fetchone()
    return(result)