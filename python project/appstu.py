import sqlite3 as sql
#from flask_login import user_loaded_from_header
from modelstu import *
#from user_authentication import *
from flask import Flask,render_template,request,redirect,jsonify

# create the application object
app = Flask(__name__)

#only 3 files - controller, model, view(html files)
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('loginnew.html')
    else:
        return render_template('home.html')
 
@app.route('/login', methods=['POST'])
def dologin():
    if checklogin(request.form['username'],request.form['password']):
        session['logged_in'] = True
        return render_template('home.html')
    else:
        flash('wrong password!')
        return render_template('loginnew.html',message='Invalid Username or Password!')
        # return redirect('/')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

@app.route('/data_pemains')
def data_pemains():
    rows=data_pemain()
    return render_template('list_student.html', rows=rows)

@app.route('/data_pasukans')
def data_pasukans():
    rows=data_pasukan()
    return render_template('list_subject.html', rows=rows)

@app.route('/data_gaji_pemains')
def data_gaji_pemains():
    rows=data_gaji_pemain()
    return render_template('list_stu_grade.html', rows=rows)

@app.route('/new')
def new():
    #make and blank array of five elements
    row=[''] * 6
    status ='0' #insert operation
    return render_template('form.html', row=row, status=status)

@app.route('/update',methods=['GET','POST'])
def  insert_update():
    id_pemain = request.form['id_pemain']
    nama_pemain = request.form['nama_pemain']
    umur = request.form['umur']
    no_jersi = request.form['no_jersi']
    posisi = request.form['posisi']
    gred_pemain = request.form['gred_pemain']
      
    if request.method=='POST' and request.form['status']=='0':                            
        row=['']*6
        row[0] = id_pemain
        row[1] = nama_pemain
        row[2] = umur
        row[3] = no_jersi
        row[4] = posisi
        row[5] = gred_pemain

        if id_pemain == '' or nama_pemain == '' or no_jersi == '':
            msg = '';
            if id_pemain == '':
                msg += 'id_pemain' if len(msg)==0 else ',id_pemain'
            if name == '':
                msg += 'nama_pemain' if len(msg)==0 else ',nama_pemain'
            if password == '':
                msg += 'no_jersi' if len(msg)==0 else ',no_jersi'
            msg = msg + ' cannot be empty!';
            return render_template('form.html',message=msg,status='0',row=row)
        else:
            if check_pemain(id_pemain):
                row[0] = ''
                flash('ID pemain already exist!')                
                return render_template('form.html',message='ID Pemain '+ id_pemain +' already exist!',status='0',row=row)

            else:        
                insert_pemain(id_pemain,nama_pemain,umur,no_jersi,posisi,gred_pemain)        
                return redirect('/data_pemains') 
             
          
    if request.method=="POST" and request.form['status']=='1':
        update_pemain(nama_pemain,umur,no_jersi,posisi,gred_pemain,id_pemain)
        return redirect('/data_pemains')
    

@app.route('/edit/<id_pemain>')
def edit(id_pemain): 
    row=find_pemain(id_pemain)
    status='1'
    return render_template('form.html',row=row,status=status)

@app.route('/delete/<id_pemain>')
def delete(id_pemain):  
     delete_pemain(id_pemain)
     return redirect('/data_pemains')

@app.route('/find_pemain',methods=['GET','POST'])
def find():
    if request.method=="POST":
        id_pemain=request.form['id_pemain']
        row=find_pemain(id_pemain)
        return render_template('form2.html',row=row)
    else:   
        return render_template('form1.html')

#new data table grade
@app.route('/new_gaji')
def newg():
    # Make and blank array of six elements
    row=['']*7
    status='0'
    return render_template('frm_stu_grade.html',row=row,status=status)

@app.route('/inupdategred',methods=['GET','POST'])
def  insert_updateg():
    id_pemain = request.form['id_pemain']
    id_pasukan = request.form['id_pasukan']
    no_resit_gaji = request.form['no_resit_gaji']
    jum_gaji_ditetapkan = request.form['jum_gaji_ditetapkan']
    cukai_pemain = request.form['cukai_pemain']
    imbuhan_mvp = request.form['imbuhan_mvp']
    jum_gaji_bersih = request.form['jum_gaji_bersih']
    
    

    if request.method=="POST" and request.form['status']=='0':
        insert_gaji(id_pemain,id_pasukan,no_resit_gaji,jum_gaji_ditetapkan,cukai_pemain,imbuhan_mvp,jum_gaji_bersih)
        return redirect('/data_gaji_pemains')


    
    #if request.method=="POST" and request.form['status']=='1':
        
        #update_grade(id,nomatrik,kod_subjek,markah,gred,mata_nilai)
        #return redirect('/list_grade')

# start the server using the run() method
if __name__ == "__main__":
     app.secret_key = "!mzo53678912489"
     app.run(debug=True,host='0.0.0.0', port=5000)
    