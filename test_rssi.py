#Trilateration algorithm: Let transmitters are at points A, B, and C, which have coordinates (xa, ya), (xb, yb), and (xc, yc).
#Position of the user (x, y) can be obtained by the following Matlab code:
import numpy as np
import matplotlib.pyplot as plt

#add a noise to positions:
epsilon = 0.0001;
noise = epsilon*(np.random.rand());
#AP co-ordinates:
#AP1:(0.3,9.35)
#AP2:(0.28,3.66)
#AP3:(6.68,4.51)
#AP4:(6.64,1.93)
xa=1
xb=5
xc=9
ya=3
yb=6
yc=3
plt.plot([xa, xb, xc],[ya, yb, yc],'bs')
xp = [xa, xb, xc]
yp = [ya, yb, yc]

xa = xp[0]+noise; ya = yp[0]+noise;
xb = xp[1]+noise; yb = yp[1]+noise;
xc = xp[2]+noise; yc = yp[2]+noise;

ptx=-30.5 #Average wifi ap received signal at a distance of <1m
n=2.5 #Pathloss coefficient
freq = 2.4
def rssi(**clients):
	for c in clients:
		if int(c) == 1:
			rmseTotal = 0
		print(clients[c])
		rssi = clients[c]
		#To take avg if rssi values are missing
		if rssi[0] == 0:
			rssi[0] = (rssi[1]+rssi[2])/2
		elif rssi[1] == 0:
			rssi[1] = (rssi[0]+rssi[2])/2
		elif rssi[2] == 0:
			rssi[2] = (rssi[0]+rssi[1])/2
		#Distance from AP1
		if freq == 5:
			ptx_new = ptx - 6.5
		x1=(ptx-rssi[0])/(10*n)
		da=pow(10,x1)
		#Distance from AP2
		x1=(ptx-rssi[1])/(10*n)
		db=pow(10,x1)
		#Distance from AP3
		x1=(ptx-rssi[2])/(10*n)
		dc=pow(10,x1)
		#Solving simultaneous equations
		va = ((db*db-dc*dc) - (xb*xb-xc*xc) - (yb*yb-yc*yc)) / 2
		vb = ((db*db-da*da) - (xb*xb-xa*xa) - (yb*yb-ya*ya)) / 2
		temp1 = vb*(xc-xb) - va*(xa-xb)
		temp2 = (ya-yb)*(xc-xb) - (yc-yb)*(xa-xb)
		dmse = [da, db, dc]
		#Estimated user position:
		ycorr = temp1 / temp2
		xcorr = (va - ycorr*(yc-yb)) / (xc-xb)
		print("X co-ordinate: ",xcorr)
		print("Y co-ordinate: ",ycorr)

		#RMSE part
		aps=3
		mse=0
		for i in range(aps):
			dxcorr = pow((pow((xcorr-xp[i]),2)+pow((ycorr-yp[i]),2)),0.5)
			mse+=pow((dxcorr-dmse[i]),2)
		rmse = pow((mse/aps),0.5)
		print("RMSE: ",rmse)
		rmseTotal = rmseTotal + rmse
		print("rmseAvg:",rmseTotal/9)
		plt.plot(xcorr, ycorr, 'ro')
	plt.legend(['AP locations','Client locations'])
	plt.show()
#Sample client rssi_val from feed reader
clients = {
'1':[-43, -44, -30],
'2':[-31, -29, -30],
'3':[-50, -55, -52],
'4':[-61, -63, -59],
'5':[-41, -32, -31],
'6':[-31, -33, -32],
'7':[0, -32, -45],
'8':[-56, -56, 0],
'9':[-53, -56, -60]
}

rssi(**clients)
