from ui_pages.data_yeni import *
from PyQt5.QtWidgets import QWidget,QTableWidgetItem
import sqlite3
import csv


class DataMainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.ui=Ui_Frame()
		self.ui.setupUi(self)
		self.loadData()
		icon=QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("resimler/indir.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
		self.ui.btnDownload.setIcon(icon)
		self.ui.btnDownload.clicked.connect(self.exportCsv)
		self.show()
	
	def loadData(self):
		sorgu="select * from kisiler"
		self.dbBaglan()
		result=self.cursor.execute(sorgu)
		self.ui.tableWidget.setRowCount(0)
		self.ui.tableWidget.setColumnCount(7)
		for rwNumber,rwData in enumerate(result):
			self.ui.tableWidget.insertRow(rwNumber)
			for clNumber,data in enumerate(rwData):
				self.ui.tableWidget.setItem(rwNumber,clNumber,QTableWidgetItem(str(data)))
		self.dbBaglantiKes()
	
	def dbBaglan(self):
		self.baglanti=sqlite3.connect("sirket.db")
		self.cursor=self.baglanti.cursor()
	
	def dbBaglantiKes(self):
		self.baglanti.close()
	
	def exportCsv(self):
		self.dbBaglan()
		data = self.cursor.execute("select * from kisiler")
		dosya=open("dosya.csv","w")
		dosya.write(",İsim,Soyisim,id,durum,kurum,kimlik,vesikalik \n")
		for rwData in enumerate(data):
			veri=str(rwData)
			veri=veri.strip()
			veri=veri.replace("(","")
			veri=veri.replace(")","")
			veri=veri.replace(" ","")
			veri=veri.replace("'","")
			print(veri)
			dosya.write(str(veri))
			dosya.write("\n")
		
		dosya.close()

