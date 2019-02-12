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
#plt.plot([xa, xb, xc],[ya, yb, yc],'bs')
xp = [xa, xb, xc]
yp = [ya, yb, yc]

xa = xp[0]+noise; ya = yp[0]+noise;
xb = xp[1]+noise; yb = yp[1]+noise;
xc = xp[2]+noise; yc = yp[2]+noise;

#Fixed client locations:
xFixed = [6,6,8]
yFixed = [1,5,1]

noLevels=10
outerCount=0
estimatedValues=[]
n=2 #Pathloss coefficient
minFixedError=[]
errorComp = 0
ptxOpt = -30
nOpt = 1.5
rmseFinal = []
distanceError = []
nPlot=[]
pPlot=[]
while outerCount < noLevels: #To run estimation for overall loop
	ptx=-30 #Average wifi ap received signal at a distance of <1m
	errorEstimate=0
	fixedClientRmse=0
	if outerCount>0:
		n=n+0.25
	print("----outerCount",outerCount,"n,ptx:",n,ptx)
	nPlot.append(n)
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

	while errorEstimate < noLevels: #To run estimation on 1 parameter at a time

		if  errorEstimate > 0:
			ptx=ptx-0.5
		#print("->errorEstimate",errorEstimate,"n,ptx:",n,ptx)
		pPlot.append(ptx)
		fixedClientError = 0
		for c in clients:
			j=0 #Used for fixedClientDistance
			#print(c)
			#print(clients[c])
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
			#print("X co-ordinate: ",xcorr)
			#print("Y co-ordinate: ",ycorr)

			#print(c)
			#RMSE part
			aps=3
			mse=0
			for i in range(aps):
				dxcorr = pow((pow((xcorr-xp[i]),2)+pow((ycorr-yp[i]),2)),0.5)
				mse+=pow((dxcorr-dmse[i]),2)
				#print(mse/(i+1))
				#print(type(xcorr),type(xFixed[j]))
			if int(c) == 1:# or int(c) == 4 or int(c) == 8: #Since clients number 2,3 and 7 are fixed and known
				#Calculate error for fixed clients
				#print(c,"from if")
				fixedClientDistance = pow((pow((xcorr-xFixed[j]),2)+pow((ycorr-yFixed[j]),2)),0.5)
				j+=1
				fixedClientError = fixedClientError + (fixedClientDistance/3)
				print("fixedClientDistance",fixedClientDistance)
				print("fixedClientError",fixedClientError)
				#minFixedError.append(fixedClientError)
			rmse = pow((mse/aps),0.5)
			#print("RMSE: ",rmse)
			if int(c) == 1:
				rmseTotal = 0
			rmseTotal = rmseTotal + rmse
		rmseFinal.append(rmseTotal/9)
		print("rmseFinal:",rmseFinal)
		#if (errorEstimate == 1 and outerCount == 0) or (errorEstimate == noLevels and outerCount == noLevels):
			#plt.plot(xcorr, ycorr, 'ro')
		#plt.show()
		print("final-fixedClientError out",fixedClientError)
		distanceError.append(fixedClientError)
		print("errorComp out",errorComp)
		if errorComp == 0:
			errorComp = fixedClientError
		if errorComp > fixedClientError:
			errorComp = fixedClientError
			ptxOpt = ptx
			nOpt = n
			print("---final-errorComp",errorComp,"on ptxOpt,nOpt",nOpt,ptxOpt)
		#print("errorEstimate",errorEstimate)
		errorEstimate = errorEstimate+1
	#time.sleep(5)
	outerCount = outerCount+1

print("Ptx Opt: ",ptxOpt)
print("n Opt: ",nOpt)
plt.plot(rmseFinal)
plt.plot(distanceError)
plt.show()
