import os

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QMessageBox

from ui_pages.ui_kayit import *
from veritabani import *


class KayitMainWindow(QWidget):
	def __init__(self, sirket):
		super().__init__()
		self.ui = Ui_KayitMainWindow()
		self.ui.setupUi(self)
		self.kayitKontrol = False
		self.sirket = sirket
		self.ui.btnTamam.clicked.connect(self.KisiEkleKayit)
		self.ui.btnKayitAl.clicked.connect(self.resimKaydet)
		self.ui.btnFotoCek.clicked.connect(self.startCam)
		self.Kontrol = False
		# self.ui.btnFotoCek.setDisabled(True)
		self.ui.btnKayitAl.setDisabled(True)
		self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		self.ui.kontrol.hide()
		self.dictx = dict()
		self.ui.btnFotoCek2.clicked.connect(self.butonResimKayitAl)
		self.dataGonder()
		self.ui.btnFotoCek.setEnabled(False)
		self.ui.btnFotoCek2.setEnabled(False)
		self.show()
		self.ui.lblSayac.hide()
		self.ui.label_7.hide()

	def startCam(self, *args):
		self.ui.btnFotoCek.setDisabled(True)
		self.ui.lineEdit.setEnabled(True)
		self.capture = cv2.VideoCapture(*args)
		self.Kontrol = True
		self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
		self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_frame)
		self.timer.start(1000. / 24)
		self.ui.btnKayitAl.setEnabled(True)

	def update_frame(self):
		self.ret, self.image = self.capture.read()
		self.image = cv2.flip(self.image, 1)
		self.displayImage(self.image)

	def stopWebCam(self):
		self.ui.btnFotoCek.show()
		self.capture.release()
		self.timer.stop()

	def resimKaydet(self):
		if self.ui.lineEdit.text() == "":
			fotoSayisi = 100
		else:
			fotoSayisi = self.ui.lineEdit.text()
		imgCunter = 0
		(width, height) = (150, 100)
		yol = os.getcwd()
		yol += "/dataset/"
		idx = str(self.idx)
		sayi = int(fotoSayisi)
		# print(sayi)
		while True:
			if self.Kontrol:
				if os.path.exists(yol) == False:
					os.mkdir(yol)
				if os.path.exists(yol + idx) == False:
					os.mkdir(yol + idx)

				imgName = yol + idx + "/" + idx + "_{}.jpg".format(imgCunter)

				cv2.imwrite(imgName, self.image)
				imgCunter += 1
				print("{}".format(imgName))
				if imgCunter == (sayi):
					QMessageBox.about(self, "Fotoğraf Çekim", "Tamamlandı")
					self.stopWebCam()
					self.ui.btnKayitAl.setDisabled(True)
					break
			else:
				QMessageBox.warning(self, "Uyarı", "Kamera Kapalı")
				break

	def butonResimKayitAl(self):
		self.ui.label_7.show()
		self.ui.lblSayac.show()
		if self.Kontrol == False:
			imgCunter = 0
			yol = os.getcwd()
			yol += "/dataset/"
			idx2 = str(self.idx)
			cam = cv2.VideoCapture(0)
			while True:
				if os.path.exists(yol) == False:
					os.mkdir(yol)
				if os.path.exists(yol + idx2) == False:
					os.mkdir(yol + idx2)
				ret, frame = cam.read()
				cv2.imshow("test", frame)
				k = cv2.waitKey(1)
				if not ret:
					break
				if k % 256 == 27:
					print("kapandı")

					break
				elif k % 256 == 32:

					img_name = yol + idx2 + "/" + idx2 + "_{}.jpg".format(imgCunter)
					cv2.imwrite(img_name, frame)
					print("{} written!".format(img_name))
					self.ui.lblSayac.setText(str(imgCunter))
					imgCunter += 1
			cam.release()
			cv2.destroyAllWindows()
		else:
			print("Kapalı")

	def displayImage(self, img):
		qFormat = QImage.Format_Indexed8
		if len(img.shape) == 3:
			if img.shape[2] == 4:
				qFormat = QImage.Format_RGBA8888
			else:
				qFormat = QImage.Format_RGB888

		outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qFormat)
		# BGR to RGB
		self.outImage = outImage.rgbSwapped()
		self.ui.label.setPixmap(QPixmap.fromImage(self.outImage))
		self.ui.label.setScaledContents(True)

	def KisiEkleKayit(self):
		from random import randint
		self.idx = randint(1001, 9999)
		isim = self.ui.txtAd.text()
		soyisim = self.ui.txtSoyad.text()
		kurum = self.ui.comboBox_2.currentText()
		durum = self.ui.comboBox_3.currentText()
		tcKimlik = self.ui.txtKimlik.text()
		vesikalik = "fotox"
		yeni = Kisi(isim, soyisim, self.idx, durum, kurum, tcKimlik, vesikalik)
		QMessageBox.about(self, "Uyarı", "Kayıt Tamamlandı")
		QMessageBox.information(self, "Bilgi", "Fotoğraf Çekiniz")
		QMessageBox.warning(self, "Dikkat", "Fotoğraf Sayısına Sadece Rakam Giriniz.")
		self.sirket.kisi_ekle(yeni)
		self.ui.btnFotoCek.setEnabled(True)
		self.ui.btnTamam.setDisabled(True)
		self.ui.txtAd.setDisabled(True)
		self.ui.txtSoyad.setDisabled(True)
		self.ui.txtKimlik.setDisabled(True)
		self.ui.kontrol.setText("True")
		self.dataGonder()
		self.ui.btnFotoCek2.setEnabled(True)

	def dataGonder(self):
		from PIL import Image
		import numpy as np
		from glob import glob
		yol = os.getcwd()
		yol += "/kisiler/"
		self.sirket.baglanti_olustur()
		sorgu = "select * from kisiler"
		self.sirket.cursor.execute(sorgu, )
		al = self.sirket.cursor.fetchall()
		k = {}
		for i in range(len(al)):
			key = al[i][2]
			print(key)
			fileList = glob('kisiler/' + key + '/*.jpg')
			val = [np.array(Image.open(fname)) for fname in fileList]
			k.update({key: val})

	def sirketiGonder(self, sirket):
		self.sirket = sirket
		sirket.kisi_ekle(self.ui)
		self.sirket.baglantiyi_kes()


"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    KayitMainWindow = QtWidgets.QWidget()
    ui = Ui_KayitMainWindow()
    ui.setupUi(KayitMainWindow)
    KayitMainWindow.show()
    sys.exit(app.exec_())"""

"""def Cam(self):
		ret,frame=self.cap.read()
		frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		h,w,channel=frame.shape
		step=channel*w
		qImg=QImage(frame.data,w,h,step,QImage.Format_RGB888)
		self.ui.label.setPixmap(QPixmap.fromImage(qImg))
	
	def controlTimer(self):
		if not self.timer.isActive():
			self.cap=cv2.VideoCapture(0)
			self.timer.start(0)
			self.ui.btnFotoCek.setText("Kamerayı Kapat")
		else:
			self.timer.stop()
			self.cap.release()
			self.ui.btnFotoCek.setText("Kamerayı Aç")"""
