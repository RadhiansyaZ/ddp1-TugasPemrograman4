import csv, uuid

def export_file(kamus):
    """This function is used to export the datas to a .csv file"""

    filename = 'TP4-DESTROYER' + ".csv"
    try:
        with open(filename, mode='w', newline='') as csv_write:
            line_write = csv.DictWriter(csv_write, fieldnames=["NAMA", "TIPE", "PROV", "LINK"])
            count = 0
            for nama in kamus:
                line_write.writerow({'NAMA':nama,'TIPE':kamus[nama]['TIPE'],'PROV':kamus[nama]['PROV'], 'LINK':kamus[nama]['LINK']})
                count += 1
        print(f"Terekspor {count} baris\n")
    except PermissionError:
        print(f"""File csv dengan nama "{filename}" sedang dibuka. Harap tutup file terlebih dahulu. Silahkan coba lagi.\n""")

def tambah(kamus, keyword):
    """This function is used to add more culture to the data"""

    tmbh = keyword.split(";;;")
    if len(tmbh) == 4:
        if tmbh[0] in kamus:
            pass
        else:
            kamus[tmbh[0]] = {'TIPE':tmbh[1].title(), 'PROV':tmbh[2].title(), 'LINK':tmbh[3]}

kamus = {}

for i in range(1000000):
    keyword = f"{uuid.uuid4()};;;{uuid.uuid4()};;;{uuid.uuid4()};;;{uuid.uuid4()}"
    tambah(kamus, keyword)

export_file(kamus)
