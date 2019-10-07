from pymavlink import mavutil
import json
import array
from PIL import Image

path = "DronePhotos"
filename="2018-07-31-16-03-24.tlog"

mlog = mavutil.mavlink_connection(filename)

print ("readed")

data = []

while True:
	m = mlog.recv_match()
	if m is not None:
		f = m.to_dict()
		if f["mavpackettype"] == 'CAMERA_FEEDBACK':
			data.append(f)
			print(f)
	else: break
print ("data captured")




