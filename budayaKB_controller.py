from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template,redirect
#from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()


#merender tampilan default(index.html)
@app.route('/',methods=['GET','POST'])
def index():
	return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("imporBudaya.html")

	elif request.method == "POST":
		f = request.files['file']
		f.save(f.filename)
		global databasefilename
		databasefilename=f.filename
		budayaData.importFromCSV(f.filename)
		n_data = len(budayaData.koleksi)
		budayaData.exportToCSV(databasefilename)
		return render_template("imporBudaya.html", result=n_data, fname=f.filename)

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

#
# - 
# - 
# - 
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
#
# - 
# - 
# - 
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
#
# - 
# - 
# - 
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
#
# - 
# - 
# - 
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

# run main app
if __name__ == "__main__":
	app.run()