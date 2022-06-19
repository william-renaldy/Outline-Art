import cv2
import os
from datetime import datetime

def capture(dir):

	for cam_port in range(-1,10000):
		cam = cv2.VideoCapture(cam_port)
		result, image = cam.read()
		if result:
			break
	print(cam_port)
	
	if result:

		with open("numbering.txt","r") as n:
			number=int("".join(n.read()))

		number+=1

		with open("numbering.txt","w") as n:
			n.write(str(number))

		temp=os.path.join(dir,"Images")
		date=datetime.now().strftime("%Y%m%d")
		name="Capture_{}_{}.png".format(date,number)

		source=os.path.join(temp,name)

		cv2.imwrite(source, image)

		return (source,name,temp,result)

	else:
		return (None,None,None,False)