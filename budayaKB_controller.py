#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)

Last update: 26 November 2019

Dengan perubahan oleh Radhiansya Zain Antriksa Putra (radhiansya.zain@ui.ac.id)
"""
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template,redirect
#from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()

#inisialisasi custom exception oleh user
class wrongExtension(Exception):
	pass

#merender tampilan default(index.html)
@app.route('/',methods=['GET', 'POST'])
def index():
	if request.method =="GET" or request.method=="POST":
		return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 
# - menolak file jika bukan .csv	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	try:
		if request.method == "GET":
			return render_template("imporBudaya.html")

		elif request.method == "POST":
			f = request.files['file']
			if f.filename.rsplit('.',1)[1] != 'csv':
					raise wrongExtension
			f.save(f.filename)
			global databasefilename
			databasefilename=f.filename
			budayaData.koleksi.clear()
			budayaData.importFromCSV(f.filename)
			n_data = len(budayaData.koleksi)
			#budayaData.exportToCSV(databasefilename)
			return render_template("imporBudaya.html", result=n_data, fname=f.filename)
	except wrongExtension:
		return render_template("imporBudaya.html",error='file_salah')
	except PermissionError:
		return render_template("imporBudaya.html",error='file_dibuka')

# Bagian ini adalah integrasi dari fitur Cari Nama, Cari Tipe, dan Cari Prov dengan nama fitur Cari Budaya
# - Menerima isian form berdasarkan kategori yang dipilih (Nama Budaya, Tipe Budaya, atau Asal Budaya)
# - Melakukan pemrosesan terhadap isian form setelah tombol "Cari" diklik
# - Merender hasil pencarian dalam bentuk tabel
@app.route('/cariBudaya',methods=['GET','POST'])
def find_budaya():
	query=''
	if request.method=='GET':
		return render_template("cariBudaya.html")
	elif request.method=='POST':
		category=request.form['category']
		query=request.form['budaya']
		if query=='':
			query_result=budayaData.cariSemuaNama()
			query_result.sort()
		if category=='name':
			query_category="Nama Budaya"
			query_result=budayaData.cariByNama(query)
			query_result.sort()
		elif category=='type_':
			query_category="Tipe Budaya"
			query_result=budayaData.cariByTipe(query)
			query_result.sort()
		elif category=='origin':
			query_category="Asal Budaya"
			query_result=budayaData.cariByProv(query)
			query_result.sort()
		return render_template('cariBudaya.html',result=query_result,nama=query,search_category=query_category)

#Bagian ini adalah implementasi fitur Tambah Budaya, yaitu:
# - Menerima isian form berupa nama,tipe,asal,dan url budaya
# - Melakukan pemrosesan terhadap isian, jika budaya belum ada maka akan ditambah
# - Memberi perintah kepada html untuk memberitahu hasil pemrosesan (diterima atau tidak)
@app.route('/tambahBudaya',methods=['GET','POST'])
def add_budaya():
	Nama=""
	Tipe=""
	Prov=""
	Url=""
	if request.method=='GET':
		return render_template("tambahBudaya.html")
	elif request.method=='POST':
		Nama=request.form['nama']
		Tipe=request.form['tipe']
		Prov=request.form['prov']
		Url=request.form['url']

	if Nama !='' and Tipe !='' and Prov !='' and Url!='':
		if databasefilename != '':
			budayaData.importFromCSV(databasefilename)
			#budayaData.tambah(Nama,Tipe,Prov,Url)
			if budayaData.tambah(Nama,Tipe,Prov,Url)==True:
				budayaData.exportToCSV(databasefilename)
				return render_template("tambahBudaya.html",name=Nama,command=True)
			else:
				return render_template("tambahBudaya.html",name=Nama,command=False)
		else:
			return redirect("/imporBudaya")
#Bagian ini adalah implementasi dari fitur Hapus Budaya, yaitu:
# - Menerima isian form berupa nama budaya
# - Melakukan pemrosesan berupa pencarian nama budaya
# - Memerintahkan html untuk memberitahu hasil pemrosesan (berhasil dihapus atau tidak ada budayanya)
@app.route('/hapusBudaya',methods=['GET','POST'])
def del_budaya():
	Nama=""
	if request.method=='GET':
		return render_template("hapusBudaya.html")
	elif request.method=='POST':
		Nama=request.form['nama']
	
	if Nama !='':
		if databasefilename != '':
			budayaData.importFromCSV(databasefilename)
			#budayaData.hapus(Nama)
			if budayaData.hapus(Nama) ==True:
				budayaData.exportToCSV(databasefilename)
				return render_template("hapusBudaya.html",name=Nama,command=True)
			else:
				return render_template("hapusBudaya.html",name=Nama,command=False)
		else:
			return redirect("/imporBudaya")
#Bagian ini adalah implementasi dari Update Budaya, yaitu:
# - Menerima isian persis tambah budaya
# - Memvalidasi apakah budaya sudah ada
# - Mengembalikan status perubahan (berhasil diubah atau budaya tidak ditemukan)
@app.route('/ubahBudaya',methods=['GET','POST'])
def edit_budaya():
	Nama=""
	Tipe=""
	Prov=""
	Url=""
	if request.method=='GET':
		return render_template("ubahBudaya.html")
	elif request.method=='POST':
		Nama=request.form['nama']
		Tipe=request.form['tipe']
		Prov=request.form['prov']
		Url=request.form['url']

	if Nama !='' and Tipe !='' and Prov !=''and Url!='':
		if databasefilename != '':
			budayaData.importFromCSV(databasefilename)
			#budayaData.ubah(Nama,Tipe,Prov,Url)
			if budayaData.ubah(Nama,Tipe,Prov,Url)==True:
				budayaData.exportToCSV(databasefilename)
				return render_template("ubahBudaya.html",name=Nama,command=True)
			else:
				return render_template("ubahBudaya.html",name=Nama,command=False)
		else:
			return redirect("/imporBudaya")
#Bagian ini adalah integrasi dari fitur Stat, Stattipe, dan Statprov
# - Stat --> Mencetak jumlah budaya yang ada
# - StatTipe --> Mencetak berdasarkan tipe dan jumlahnya pada tabel yang dicetak
# - StatProv --> Mencetak berdasarkan asal provinsi dan jumlahnya pada tabel yang dicetak
@app.route('/statsBudaya',methods=['GET','POST'])
def stat_budaya():
	if request.method=='GET':
		return render_template("statsBudaya.html")
	elif request.method=='POST':
		category=request.form['category']
		if category=='all':
			query_result=budayaData.stat()
			return render_template('statsBudaya.html',result=False,jumlah=query_result)
		elif category=='tipe':
			query_result=budayaData.statByTipe()
			return render_template('statsBudaya.html',result=True,jumlah=query_result,tipe="Tipe Budaya")
		elif category=='asal':
			query_result=budayaData.statByProv()
			return render_template('statsBudaya.html',result=True,jumlah=query_result, tipe="Asal Budaya")

#Bagian ini akan mengembalikan template Error '404' jika terjadi error 404
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

# run main app
if __name__ == "__main__":
	app.run()