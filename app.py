from datetime import date, datetime
from os import stat
from MySQLdb import STRING
from flask import Flask, render_template, request, redirect, sessions, url_for, flash,session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from flask import Flask,flash


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'klinik'
mysql = MySQL(app)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('includes/login/index.html')

@app.route('/proseslogin', methods=["POST"])
def proseslogin():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM user WHERE username=%s",(username,))
    data = cur.fetchone()
    cur.close()

    if len(data) > 0:
        if bcrypt.hashpw(password, data['password'].encode('utf-8')) == data['password'].encode('utf-8'):
            session['id'] = data['id']
            session['dokter_id'] = data['dokter_id']
            session['username'] = data['username']
            session['level'] = data['level']
            return redirect(url_for('dashboard'))
        else:
            flash("Password Yang Anda Masukan Salah", "Password")
            # return "Error Password Doesnt Match"
            return render_template('includes/login/index.html')
    else:
        return render_template('includes/login/index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    dokter = session['dokter_id']
    tanggal = datetime.now()
    tanggal.strftime("%Y-%m-%d")
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(id) FROM dokter")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(id) FROM user WHERE level='Petugas'")
    petugas = cur.fetchall()
    cur.execute("SELECT COUNT(id) FROM berobat")
    pasien = cur.fetchall()
    cur.execute("SELECT COUNT(id) FROM pasien")
    pdones = cur.fetchall()
    cur.execute("SELECT COUNT(id) FROM pendaftaran")
    jumlah_pas = cur.fetchall()
    cur.execute("SELECT COUNT(id) FROM berobat WHERE dokter_id=%s",[dokter])
    pasien_dokter = cur.fetchall()
    cur.execute("SELECT COUNT(id) FROM pasien WHERE dokter_id=%s",[dokter])
    done_dokter = cur.fetchall()
    cur.close()
    return render_template('includes/dashboard.html', dokter=data,petugast=petugas,pasient=pasien,pdonest=pdones, pasien=jumlah_pas,pasdok=pasien_dokter,dondok=done_dokter)

# Controller Dokter

@app.route('/dokter')
def dokter():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dokter")
    data = cur.fetchall()
    cur.execute("SELECT * FROM dokter WHERE akun_dokter = '0' ")
    modal = cur.fetchall()
    cur.close()
    return render_template('includes/mn_dokter.html', dokters=data, modals=modal)

@app.route('/simpan', methods=["POST"])
def simpan():
    nama = request.form['nama']
    jadwal = request.form['jadwal']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO dokter (nama,jadwal) VALUES (%s,%s)", (nama,jadwal))
    mysql.connection.commit()
    return redirect(url_for('dokter'))

@app.route('/akundokter', methods=["POST"])
def akundokter():
    id_dokter = request.form['id_dokter']
    username = request.form['username']
    show_pwd = request.form['password']
    password = request.form['password'].encode('utf-8')
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    level = 'Dokter'
    akun = '1'
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user (dokter_id,username,password,show_pwd,level) VALUES (%s,%s,%s,%s,%s)", (id_dokter,username,hash_password,show_pwd,level))
    cur.execute("UPDATE dokter SET akun_dokter=%s WHERE id=%s", (akun,id_dokter))
    mysql.connection.commit()
    return redirect(url_for('dokter'))

@app.route('/update', methods=["POST"])
def update():
    nama = request.form['nama']
    jadwal = request.form['jadwal']
    id = request.form['id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE dokter SET nama=%s, jadwal=%s WHERE id=%s", (nama,jadwal,id))
    mysql.connection.commit()
    return redirect(url_for('dokter'))

@app.route('/hapus/<string:id>', methods=["GET"])
def hapus(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM dokter WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('dokter'))

# Controller Pasien

@app.route('/pasien')
def pasien():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pendaftaran")
    data = cur.fetchall()
    cur.execute("SELECT * FROM pendaftaran")
    nam_pasien = cur.fetchall()
    cur.execute("SELECT * FROM pendaftaran WHERE keterangan='0'")
    namanya_pasien = cur.fetchall()
    cur.execute("SELECT * FROM dokter")
    tam = cur.fetchall()
    cur.close()
    return render_template('includes/daftar_pasien.html', pasien=data, pasiens=nam_pasien, dokter = tam, namanya=namanya_pasien)

@app.route('/simpanpasien', methods=["POST"])
def simpanpasien():
    nama = request.form['nama']
    tempat = request.form['tempat']
    tanggal = request.form['tanggal']
    jenkel = request.form['jenkel']
    status = request.form['status']
    profesi = request.form['profesi']
    alamat = request.form['alamat']
    ket = '0'
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO pendaftaran (nama,tl,tg_lahir,jk,status,profesi,alamat,keterangan) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (nama,tempat,tanggal,jenkel, status,profesi,alamat,ket))
    mysql.connection.commit()
    return redirect(url_for('pasien'))

@app.route('/editpasien', methods=["POST"])
def editpasien():
    nama = request.form['nama']
    tempat = request.form['tempat']
    tanggal = request.form['tanggal']
    jenkel = request.form['jenkel']
    status = request.form['status']
    profesi = request.form['profesi']
    alamat = request.form['alamat']
    ket = ''
    id = request.form['id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE pendaftaran SET nama=%s, tl=%s, tg_lahir=%s, jk=%s, status=%s, profesi=%s, alamat=%s, keterangan=%s WHERE id=%s", (nama,tempat,tanggal,jenkel,status,profesi,alamat,ket,id))
    mysql.connection.commit()
    return redirect(url_for('pasien'))

@app.route('/hapuspasien/<string:id>', methods=["GET"])
def hapuspasien(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pendaftaran WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('pasien'))

#Controller Berobat
@app.route('/berobat')
def berobat():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM berobat JOIN pendaftaran ON berobat.pendaftaran_id=pendaftaran.id JOIN dokter ON berobat.dokter_id=dokter.id")
    data = cur.fetchall()
    cur.close()
    return render_template('includes/berobat.html', pasien=data)

@app.route('/hapusberobat/<string:id>', methods=["GET"])
def hapusberobat(id):
    cur = mysql.connection.cursor()
    ket = '0'
    cur.execute("SELECT pendaftaran_id FROM berobat WHERE id = %s",[id])
    data = cur.fetchone()
    cur.execute("UPDATE pendaftaran SET keterangan=%s WHERE id=%s", (ket,data))
    cur.execute("DELETE FROM berobat WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('berobat'))

@app.route('/simpanberobat', methods=["POST"])
def simpanberobat():
    nama = request.form['nama']
    dokter = request.form['dokter']
    keluhan = request.form['keluhan']
    ket = '1'
    tanggal = datetime.now()
    tanggal.strftime("%Y-%m-%d %H:%M:%S")
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO berobat (pendaftaran_id,dokter_id,waktu_daftar,keluhan) VALUES (%s,%s,%s,%s)", (nama,dokter,tanggal,keluhan))
    cur.execute("UPDATE pendaftaran SET keterangan=%s WHERE id=%s", (ket,nama))
    mysql.connection.commit()
    return redirect(url_for('berobat'))

#Controller User

@app.route('/user')
def user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    data = cur.fetchall()
    cur.close()
    return render_template('includes/mn_user.html', user=data)

@app.route('/simpanuser', methods=["POST"])
def simpanuser():
    id_dokter = '0'
    username = request.form['username']
    show_password = request.form['password']
    password = request.form['password'].encode('utf-8')
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    level = request.form['level']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user (dokter_id,username,password,show_pwd,level) VALUES (%s,%s,%s,%s,%s)", (id_dokter,username,hash_password,show_password,level))
    mysql.connection.commit()
    return redirect(url_for('user'))

@app.route('/edituser', methods=["POST"])
def edituser():
    username = request.form['username']
    show_pwd = request.form['password']
    password = request.form['password'].encode('utf-8')
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    level = request.form['level']
    id = request.form['id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE user SET username=%s, password=%s, show_pwd=%s, level=%s WHERE id=%s", (username,password,show_pwd,level,id))
    mysql.connection.commit()
    return redirect(url_for('user'))

@app.route('/hapususer/<string:id>', methods=["GET"])
def hapususer(id):
    akun = '0'
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user WHERE id=%s", (id,))
    # cur.execute("UPDATE dokter SET akun_dokter=%s WHERE id=%s", (akun,id))
    mysql.connection.commit()
    return redirect(url_for('user'))

#Controller Rekam Medis
@app.route('/medis')
def medis():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pasien JOIN pendaftaran ON pasien.pendaftaran_id=pendaftaran.id JOIN dokter ON pasien.dokter_id=dokter.id")
    data = cur.fetchall()
    # cur.execute("SELECT * FROM dokter JOIN pasien ON pasien.dokter_id=dokter.id ")
    # tam = cur.fetchall()
    # cur.execute("SELECT * FROM pendaftaran JOIN pasien ON pasien.pendaftaran_id=pendaftaran.id ")
    # nam_pasien = cur.fetchall()
    # idpasien = request.form['idpasien']
    # cur.execute("SELECT * FROM pendaftaran JOIN pasien ON pasien.pendaftaran_id=pendaftaran.id WHERE pasien.id=idpasien")
    # modalnama = cur.fetchall()
    cur.execute("SELECT * FROM pendaftaran WHERE keterangan = '0'")
    pasien = cur.fetchall()
    cur.execute("SELECT * FROM dokter")
    dokter = cur.fetchall()
    cur.close()
    return render_template('includes/rek_medis.html', user=data,dokters=dokter,pasiens=pasien)

@app.route('/simpanmedis', methods=["POST"])
def simpanmedis():
    nama = request.form['nama']
    dokter = request.form['dokter']
    diagnosa = request.form['diagnosa']
    resep = request.form['resep']
    tanggal = request.form['tanggal']
    status = '0'
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO pasien (pendaftaran_id,dokter_id,diagnosa,resep,tanggal) VALUES (%s,%s,%s,%s,%s)", (nama,dokter,diagnosa,resep,tanggal))
    cur.execute("UPDATE pendaftaran SET keterangan=%s WHERE id=%s", (status,nama,))
    mysql.connection.commit()
    return redirect(url_for('medis'))

@app.route('/editmedis', methods=["POST"])
def editmedis():
    nama = request.form['nama']
    dokter = request.form['dokter']
    diagnosa = request.form['diagnosa']
    resep = request.form['resep']
    tanggal = request.form['tanggal']
    id = request.form['id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE pasien SET pendaftaran_id=%s, dokter_id=%s, diagnosa=%s, resep=%s, tanggal=%s WHERE id=%s", (nama,dokter,diagnosa,resep,tanggal,id))
    mysql.connection.commit()
    return redirect(url_for('medis'))

@app.route('/hapusmedis/<string:id>', methods=["GET"])
def hapusmedis(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pasien WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('medis'))

# Controller Diagnosa
@app.route('/diagnosa')
def diagnosa():
    dokter = session['dokter_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM berobat JOIN pendaftaran ON berobat.pendaftaran_id=pendaftaran.id WHERE berobat.dokter_id = %s",[dokter])
    data = cur.fetchall()
    cur.close()
    return render_template('includes/diagnosa.html', pasien=data)

@app.route('/simpandiagnosa', methods=["POST"])
def simpandiagnosa():
    nama = request.form['nama']
    dokter = request.form['dokter']
    diagnosa = request.form['diagnosa']
    resep = request.form['resep']
    id = request.form['id']
    tanggal = datetime.now()
    tanggal.strftime("%Y-%m-%d %H:%M:%S")
    status = '0'
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO pasien (pendaftaran_id,dokter_id,diagnosa,resep,tanggal) VALUES (%s,%s,%s,%s,%s)", (nama,dokter,diagnosa,resep,tanggal))
    cur.execute("UPDATE pendaftaran SET keterangan=%s WHERE id=%s", (status,nama,))
    cur.execute("DELETE FROM berobat WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('diagnosa'))

if __name__ == '__main__':
    app.run(debug=True)