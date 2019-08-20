import sqlite3

from PyQt5.QtWidgets import QTableWidgetItem


class Kisi():
	
	def __init__(self,isim,soyisim,id="",durum="",kurum="",tcKimlik="",vesikalik=""):
		
		self.isim=isim
		self.soyisim=soyisim
		self.id=id
		self.durum=durum
		self.kurum=kurum
		self.tcKimlik=tcKimlik
		self.vesikalik=vesikalik
	
	def __str__(self):
		return "Kişi İsmi: {}\nSoyisim: {}\nID: {}\nDurum: {}\nKurum: {}\nTC Kimlik :{}\nVesikalık: {}".format(
			self.isim,self.soyisim,self.id,self.durum,self.kurum,self.tcKimlik,self.vesikalik)


class Sirket():
	
	def __init__(self):
		
		self.baglanti_olustur()
	
	def baglanti_olustur(self):
		self.baglanti=sqlite3.connect("sirket.db")
		self.cursor=self.baglanti.cursor()
		sorgu1="Create Table If not exists kayitlar (id TEXT,izinDurumu TEXT,girisCikis TEXT, ad TEXT,Soyad TEXT, tarih TEXT,saat TEXT)"
		sorgu2="Create Table If not exists kisiler (isim TEXT,soyisim TEXT,id TEXT,durum TEXT,kurum TEXT,tcKimlik TEXT,vesikalik TEXT)"
		self.cursor.execute(sorgu1)
		self.cursor.execute(sorgu2)
		self.baglanti.commit()
	
	def baglantiyi_kes(self):
		self.baglanti.close()
	
	"""def kisileri_goster(self):

		sorgu="Select * From kisiler"

		self.cursor.execute(sorgu)

		kisiler=self.cursor.fetchall()

		if (len(kisiler) == 0):
			print("Kütüphanede kitap bulunmuyor...")
		else:
			for i in kisiler:
				kisi=Kisi(i[0],i[1],i[2],i[3],i[4],i[5],[6])
				print(kisi)
				print("******************")"""
	
	def kisileri_goster(self,ui):
		self.baglanti_olustur()
		sorgu="select * from kisiler "
		self.gelen2 = ui
		veriler=self.cursor.execute(sorgu)
		for rwNumber,rwData in enumerate(veriler):
			ui.tableWidget.insertRow(rwNumber)
			for clNumber,data in enumerate(rwData):
				ui.tableWidget.setItem(rwNumber,clNumber,QTableWidgetItem(str(data)))
		self.baglantiyi_kes()
	
	def kisi_sorgula(self,id):
		
		self.baglanti_olustur()
		sorgu="Select * From kisiler where id = (?)"
		
		self.cursor.execute(sorgu,(id,))
		
		kisiler=self.cursor.fetchall()
		
		if (len(kisiler) == 0):
			print("Böyle bir kisi bulunmuyor.....")
		else:
			kisi=Kisi(kisiler[0][0],kisiler[0][1],kisiler[0][2],kisiler[0][3],kisiler[0][4],kisiler[0][5],kisiler[0][6])
			
			return kisi
		self.baglantiyi_kes()
	def kisi_ekle(self,kisi):
		self.baglanti_olustur()
		kontrol = "select * from kisiler"
		self.cursor.execute(kontrol,)
		x = self.cursor.fetchall()
		
		sorgu="Insert into kisiler Values(?,?,?,?,?,?,?)"
		
		self.cursor.execute(sorgu,(kisi.isim,kisi.soyisim,kisi.id,kisi.durum,kisi.kurum,kisi.tcKimlik,kisi.vesikalik))
		self.baglanti.commit()
		self.baglantiyi_kes()
	def kisi_sil(self,isim):
		self.baglanti_olustur()
		sorgu="Delete From kisiler where isim = ?"
		
		self.cursor.execute(sorgu,(isim,))
		
		self.baglanti.commit()
		self.baglantiyi_kes()
	def kayitlariGoster(self,ui):
		self.baglanti_olustur()
		self.gelen=ui
		sorgu="select * from kayitlar order by tarih desc , saat desc "
		veri=self.cursor.execute(sorgu)
		for rwNumber,rwData in enumerate(veri):
			ui.tableWidget.insertRow(rwNumber)
			for clNumber,data in enumerate(rwData):
				ui.tableWidget.setItem(rwNumber,clNumber,QTableWidgetItem(str(data)))
		self.baglantiyi_kes()
	
	def tableClear(self,ui):
		#self.gelen.tableWidget.clearContents()
		self.baglanti_olustur()
		for i in reversed(range(self.gelen.tableWidget.rowCount())):
			self.gelen.tableWidget.removeRow(i)
		self.baglantiyi_kes()

	def kisiTemizle(self,ui):
		self.baglanti_olustur()
		for i in reversed(range(self.gelen2.tableWidget.rowCount())):
			self.gelen2.tableWidget.removeRow(i)
		self.baglantiyi_kes()
	
	def yazdir(self):
		self.cursor.execute("select * from kisiler")
		[print(row) for row in self.cursor.fetchall()]
	
	def kayitEkle(self,id,durum,girisCikis,isim,soyisim,tarih,saat):
		self.baglanti_olustur()
		sorgu="insert into kayitlar VALUES (?,?,?,?,?,?,?)"
		self.cursor.execute(sorgu,(id,durum,girisCikis,isim,soyisim,tarih,saat))
		self.baglanti.commit()
		
		self.gelen.tableWidget.update()
		self.baglantiyi_kes()
		
	def updatex(self,ad,soyad,durum,kurum,id):
		

		self.baglanti_olustur()
		adx=ad
		soyadx=soyad
		idx=id
		durumx=durum
		kurumx=kurum
		sorgu2 ="update kisiler set isim=?,soyisim=?,durum=?,kurum=? where id=?"
		self.cursor.execute(sorgu2,(adx,soyadx,durumx,kurumx,idx))
		self.baglanti.commit()
		self.baglantiyi_kes()
		


"""
	k = Kisi(kisi)
		sorgu = "update kisiler set isim=?,soyisim=?,id=?,durum=?,kurum=?  where id =? "
		self.cursor.execute(sorgu,(kisi.isim,kisi.soyisim,kisi.id,kisi.durum,kisi.kurum))
		self.baglanti.commit()
		print("------------")
		"""
