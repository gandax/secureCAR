# coding: utf8



from parseurlog import parseurlog

from modelestep import modelestep

import matplotlib.pyplot as plt

# Code pour afficher Y en fonction de X et Theta en fonction de t a partir du fichier contenant les entrees du modele

data = parseurlog('entries.txt',9)

tabx=[]

taby=[]

tabtheta=[]

tabv=[]

tabt=[]

Te=0.05
k=0

for i in data:
	tabx.append(float(i[3]))
	taby.append(float(i[4]))
	tabtheta.append(float(i[5])*180/3.14)
	if(k==0):
		tabt.append(0.0)
	else:
		tabt.append(float(i[8])+tabt[k-1])
	k+=1

fig = plt.figure()
plt.plot(tabx,taby,'ro')
plt.title("Position of the car")
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.show()
plt.figure()
plt.plot(tabt,tabtheta,'ro')
plt.title("Angle of the car")
plt.xlabel('Theta (degrees)')
plt.ylabel('t (seconds)')
plt.show()
plt.figure()
