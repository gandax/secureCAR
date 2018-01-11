# coding: utf8



from parseurlog import parseurlog

from modelestep import modelestep

import matplotlib.pyplot as plt



data = parseurlog('entries.txt',9)

tabx=[]

taby=[]

tabtheta=[]

tabv=[]

tabt=[]

Te=0.05
k=0

for i in data:

	output =modelestep(float(i[0]),float(i[1]),float(i[2]),float(i[3]),float(i[4]),float(i[5]),float(i[6]),float(i[7]),float(i[8]))
	tabx.append(output[0])
	taby.append(output[1])
	tabtheta.append(output[2]*180/3.14)
	tabv.append(output[3])
	tabt.append(Te*(k))
	k+=1
print tabtheta
plt.figure()
plt.plot(tabx,taby,'ro')
plt.title("Y en fonction de X")
plt.show()
plt.figure()
plt.plot(tabt,tabtheta,'ro')
plt.title("Theta en fonction de T")
plt.show()
plt.figure()

