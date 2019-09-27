from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

"""
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True, help = "path to directory of images")
ap.add_argument("-o", "--output", type=str, required=True, help = "path to output image")
ap.add_argument("-c", "--crop", type=int, default=0, help = "wheter to crop.out largest rectangular region")

args = vars(ap.parse_args())

"""

class Stitch:
	def __init__(self, crop):
		self.crop = crop

	def solve (paths):

		print ("[INFO] reading paths...")
		imagePaths = sorted(list(paths.list_images(args["images"])))
		images = []	


		print ("[INFO] loading images...")
		for imagePath in imagePaths:
			image = cv2.imread(imagePath)
			images.append(image)

			# инициализация OpenCVшного ститчера и склейка (без обрезки)
			print ("[INFO] stitching images...")
			stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
			(status, stitched) = stitcher.stitch(images)

			# если статус равен 0, OpenCV успешно завершил работу
			if status == 0:
				#проверяем, нужно ли обрезать фотографи.
				if args["crop"] > 0:
					# создаем 10пиксельную границу, окружающую изображение
					print("[INFO] cropping image...")
					stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))

					# переводим склееное изображение в серый цвет для
					# трешолдинга так, что пиксели, большие чем 0 = 255
					# все остальные остаются 0
					gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
					thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
					cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
					cnts = imutils.grab_contours(cnts)
					c = max(cnts, key=cv2.contourArea)

					# выделение памяти на маску, которая будет содержать в себе 
					# конечную фотографию
					mask = np.zeros(thresh.shape, dtype = "uint8")
					(x,y,w,h) = cv2.boundingRect(c)
					cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)

					# создаем две копии маски: одну для минимальной прямоуг. площади
					# вторую для подсчета кол-ва пикселей, которые надо удалить
					minRect = mask.copy()
					sub = mask.copy()

					# пока есть ненулевые пиксели, мы их убираем
					while cv2.countNonZero(sub) > 0:
						minRect=cv2.erode(minRect, None)
						sub = cv2.subtract(minRect, thresh)

					# находим контур минимального прямоуг. и выделяем из начальной фотографии его
					cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
					cnts = imutils.grab_contours(cnts)
					c = max(cnts, key=cv2.contourArea)
					(x,y,w,h) = cv2.boundingRect(c)
					stitched = stitched[y:y + h, x:x + w]


				cv2.imwrite(args["output"], stitched)

				cv2.imshow("Stitched", stitched)
				cv2.waitKey(0)
			else:
				print ("[INFO] image stitching failed! ({})".format(status))

