# -*- coding: utf-8 -*-
# import  PyQt5 modüller
import datetime
import glob
import os

import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication
import kayit
from data import *
from kisiler import *
from ui_pages.ui_main import *
from veritabani import Sirket
import time

# Kaynak Dosya Yollarını Belirlemek için Bunlar 0 - 1 -2 -3 -4 diye gidebilir kameralara bağlı olarak
source1 = 0  # "videolar/video1.mp4"  # 0
source2 = 0  # "videolar/video1.mp4"
source3 = 0  # "videolar/video1.mp4"  # 6
source4 = 0  # "videolar/video1.mp4"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class MainWindow(QWidget):
	# class constructor
	def __init__(self):
		# QWidget Yani Pencereyi oluşturduğumuz kısım
		super().__init__()
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		# Data Yüklemesi
		self.sirket = Sirket()
		self.sirket.kayitlariGoster(self.ui)
		# create a timer kamerayı açmak için lazım olan timer fonksiyonları
		# self.timer = QTimer()
		self.timer2 = QTimer()
		# self.timer3 = QTimer()
		# self.timer4 = QTimer()
		# set timer timeout callback function
		self.camKontrol = False
		# self.timer.timeout.connect(self.viewCam)
		self.timer2.timeout.connect(self.viewCam2)
		# self.timer3.timeout.connect(self.viewCam3)
		# self.timer4.timeout.connect(self.viewCam4)
		# butonlara basıldığında yapması gereken işlemlerin olduğu kısım
		self.ui.control_bt.clicked.connect(self.controlTimer)
		# self.ui.control_bt_2.clicked.connect(self.duzelt)
		self.ui.btnKisiler.clicked.connect(self.kisilerWindow)
		self.ui.btnKayit.clicked.connect(self.dataWindow)
		self.ui.btnKisiEkle.clicked.connect(self.kayitWindow)
		self.gonder = None
		self.ui.image_label.setText("Kamera 1")
		self.last_img_fname = "0"
		self.kontrolList = list()
		self.tt_opencvDnn = 0
		self.frame_count = 0
		self.modelFile = "models/opencv_face_detector_uint8.pb"
		self.configFile = "models/opencv_face_detector.pbtxt"
		self.net = cv2.dnn.readNetFromTensorflow(self.modelFile, self.configFile)
		self.label = None
		self.fpsDnn = None
		self.iconKontrol = False
		self.icon = QtGui.QIcon()

	def viewCam(self):
		# # read image in BGR format
		# ret,image=self.cap.read()
		# # convert image to RGB format
		# image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		# # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		# # get image infos
		# height,width,channel=image.shape
		# step=channel*width
		# # create QImage from image
		# qImg=QImage(image.data,width,height,step,QImage.Format_RGB888)
		# # show image in img_label
		# self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
		# self.ui.image_label.setScaledContents(True)
		global id
		imreaddir = "kisiler/"

		imdirs = sorted(glob.glob(imreaddir + "/" + '*.jpg'))

		updated_img_fname = imdirs[-1].split(os.path.sep)[-1][:-4]

		if updated_img_fname != self.last_img_fname:
			image = cv2.imread(imdirs[-1])
			got_image = False
		if updated_img_fname != self.last_img_fname:
			got_image = False
			while not got_image:
				try:
					image = cv2.imread(imdirs[-1])
					image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
					got_image = True
				except:
					got_image = False

			height, width, channel = image.shape
			step = channel * width
			qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
			self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
			self.ui.image_label.setScaledContents(True)
			imnamedata = updated_img_fname.split("_")
			if len(imnamedata) > 1:
				id = imnamedata[1]
			# TODO: add entered guy id to list
			# print(str(id))
			self.last_img_fname = updated_img_fname
		# print(self.last_img_fname)
		self.kisi1BilgiGetir(kisiID=id)

	def dosyaOlustur(self):
		with open("dataset/__train__", "w") as f:
			f.write("")

	def getir(self):
		try:
			veri = self.gonder.ui.kontrol.text()
			self.renkDegis(veri)
		except AttributeError:
			# TO DO veri
			pass

	# Kisiler Penceresi
	def kisi1BilgiGetir(self, kisiID):
		self.tarih = datetime.datetime.now()
		self.saat = datetime.datetime.now()
		print(self.saat)
		isim = kisiID
		kisi = self.sirket.kisi_sorgula(isim)
		adSoyad = kisi.isim + " " + kisi.soyisim
		self.ui.lbl_AdSoyad.setText(adSoyad)
		self.ui.lblCikis.hide()
		tarih = str(datetime.datetime.strftime(self.tarih, '%x'))
		saat = str(datetime.datetime.strftime(self.saat, '%X'))
		if (kisi.durum == "izinli"):
			pass
		else:
			pass
		self.ui.lbl_ID.setText(kisi.id)
		giris = "Giriş"
		if isim not in self.kontrolList:
			self.sirket.kayitEkle(kisi.id, kisi.durum, giris, kisi.isim, kisi.soyisim, tarih, saat)
			self.sirket.tableClear(self.ui)
			self.sirket.kayitlariGoster(self.ui)
			self.kontrolList.append(isim)
		else:

			yol = "kisiler/"
			x = self.last_img_fname
			x += ".jpg"
			# print(yol+x)
			fotograf = cv2.imread(yol + x, 1)
			faces = face_cascade.detectMultiScale(cv2.cvtColor(fotograf, cv2.COLOR_BGR2GRAY), 1.3, 5)
			for (x, y, w, h) in faces:
				roi_gray = faces[y:y + h, x:x + w]
				roi_color = fotograf[y:y + h, x:x + w]
			fotograf = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)
			h, w, c = fotograf.shape
			step = c * w
			fotografx = QImage(fotograf.data, w, h, step, QImage.Format_RGB888)
			self.ui.lblProfilFoto.setPixmap(QPixmap.fromImage(fotografx))
			self.ui.lblProfilFoto.setScaledContents(True)

	def kisilerWindow(self):
		self.kisiler = KisilerMainWindow()
		self.kisiler.sirketiGonder(self.sirket)

	def kayitWindow(self):
		self.gonder = kayit.KayitMainWindow(self.sirket)
		if self.camKontrol:
			self.timer.stop()
			self.cap.release()

	def dataWindow(self):
		self.dataPy = DataMainWindow()

	# view camera 1

	# view camera 2
	def viewCam2(self):
		# read image in BGR format
		t = time.time()
		ret, image = self.cap2.read()

		outOpencvDnn, bboxes = self.detectFaceOpenCVDnn(self.net, image)

		# convert image to RGB format
		# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		outOpencvDnn = cv2.cvtColor(outOpencvDnn, cv2.COLOR_BGR2RGB)
		# get image infos
		height, width, channel = outOpencvDnn.shape
		step = channel * width

		# create QImage from image
		# qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
		qImg = QImage(outOpencvDnn.data, width, height, step, QImage.Format_RGB888)
		# show image in img_label
		self.frame_count += 1
		self.tt_opencvDnn += time.time() - t
		self.fpsDnn = self.frame_count / self.tt_opencvDnn
		self.fpsDnn = int(self.fpsDnn)
		self.label = "FPS : {}".format(self.fpsDnn)
		print(self.fpsDnn)
		self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
		self.ui.image_label.setScaledContents(True)

	def detectFaceOpenCVDnn(self, net, frame):

		conf_threshold = 0.5
		frameOpencvDnn = frame.copy()

		frameHeight = frameOpencvDnn.shape[0]
		frameWidth = frameOpencvDnn.shape[1]
		blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

		net.setInput(blob)
		detections = net.forward()
		bboxes = []
		for i in range(detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > conf_threshold:
				x1 = int(detections[0, 0, i, 3] * frameWidth)
				y1 = int(detections[0, 0, i, 4] * frameHeight)
				x2 = int(detections[0, 0, i, 5] * frameWidth)
				y2 = int(detections[0, 0, i, 6] * frameHeight)
				bboxes.append([x1, y1, x2, y2])
				cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
		return frameOpencvDnn, bboxes

	# view camera 3
	def viewCam3(self):
		# read image in BGR format
		ret, image = self.cap3.read()
		# convert image to RGB format
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		# get image infos
		height, width, channel = image.shape
		step = channel * width
		# create QImage from image
		qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
		# show image in img_label
		self.ui.image_label_3.setPixmap(QPixmap.fromImage(qImg))
		self.ui.image_label_3.setScaledContents(True)

	# view camera 4
	def viewCam4(self):
		# read image in BGR format
		ret, image = self.cap4.read()
		# convert image to RGB format
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		# get image infos
		height, width, channel = image.shape
		step = channel * width
		# create QImage from image
		qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
		# show image in img_label
		self.ui.image_label_4.setPixmap(QPixmap.fromImage(qImg))
		self.ui.image_label_4.setScaledContents(True)

	# start/stop timer
	def controlTimer(self):
		# if timer is stopped
		if not (self.timer2.isActive()):
			# create video capture
			self.cap2 = cv2.VideoCapture(source2)

			self.timer2.start()

			self.camKontrol = True

			self.iconDegis()
			self.iconKontrol = True
			self.getir()
		# if timer is started
		else:
			self.timer2.stop()
			self.cap2.release()
			self.iconDegis()
			self.iconKontrol = False


	# veri aktarımı için çok da gerekli değil
	def renkDegis(self, kontrol):
		durumx = kontrol
		self.durum = durumx
		if self.durum == "True":
			self.ui.control_bt_2.setStyleSheet("background-color: rgb(52, 101, 164);")
			durumx = "False"

	def iconDegis(self):
		if self.iconKontrol == False:
			self.icon.addPixmap(QtGui.QPixmap("resimler/stop.png"))
			self.ui.control_bt.setIcon(self.icon)
			self.ui.control_bt.setIconSize(QtCore.QSize(80, 80))
		else:
			self.icon.addPixmap(QtGui.QPixmap("resimler/start.png"))
			self.ui.control_bt.setIcon(self.icon)
			self.ui.control_bt.setIconSize(QtCore.QSize(80, 80))

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	sys.exit(app.exec_())
