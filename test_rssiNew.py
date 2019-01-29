#Trilateration algorithm: Let transmitters be at points A, B, and C, which have coordinates (xa, ya), (xb, yb), and (xc, yc). 
#Position of the user (x, y) can be obtained by the following Matlab code:
import numpy as np
import matplotlib.pyplot as plt
import time

#add a noise to positions:
epsilon = 0.0001;
noise = epsilon*(np.random.rand());
#AP co-ordinates:
#AP1:(0.3,9.35)
#AP2:(0.28,3.66)
#AP3:(6.68,4.51)
#AP4:(6.64,1.93)
xa=7
xb=5
xc=9
ya=6
yb=1
yc=1
plt.plot([xa, xb, xc],[ya, yb, yc],'bs')
xp = [xa, xb, xc];
yp = [ya, yb, yc];

xa = xp[0]+noise; ya = yp[0]+noise;
xb = xp[1]+noise; yb = yp[1]+noise;
xc = xp[2]+noise; yc = yp[2]+noise;

outerCount=0
estimatedValues=[]

for outerCount in range(9): #To run estimation for overall loop
	print(outerCount)
	ptx=-30 #Average wifi ap received signal at a distance of <1m
	n=2 #Pathloss coefficient
	errorEstimate=0
	fixedClientRmse=0
	errorLoopCount = 1
	if outerCount>0:
		n=n+0.5
	for errorEstimate in range(9): #To run estimation on 1 parameter at a time
		def rssi(**clients):
			print("1")
			if  errorEstimate>0:
				ptx=ptx+1
			for c in clients:
				#print(c)
				print(clients[c])
				rssi = clients[c]
				#Distance from AP1
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
				errorLoopCount+=1
				#RMSE part
				aps=3
				mse=0	
				for i in range(aps):
					dxcorr = pow((pow((xcorr-xp[i]),2)+pow((ycorr-yp[i]),2)),0.5)
					mse+=pow((dxcorr-dmse[i]),2)
					#print(mse/(i+1))
					rmse = pow((mse/aps),0.5)
					if c == 2 or c == 3 or c == 7: #Since clients number 2,3 and 7 are fixed and known
						fixedClientRmse = fixedClientRmse + (rmse/3)
					print("RMSE: ",rmse)
					if (errorLoopCount == 1 and outerCount == 0) or (errorLoopCount == 8 and outerCount == 1):
						plt.plot(xcorr, ycorr, 'ro')
					plt.show()
		errorEstimate = errorEstimate + 1
	time.sleep(1)
	outerCount+=1
#Sample client rssi_val from feed reader	
clients = {
'1':[-43, -44, -30],
'2':[-31, -29, -30],
'3':[-50, -55, -52],
'4':[-61, -63, -59],
'5':[-41, -32, -31],
'6':[-31, -33, -32],
'7':[-38, -32, -38],
'8':[-56, -56, 0],
'9':[-53, -56, -60]
}

rssi(**clients)