#coding: utf8



from parseurlog2 import parseurlog2

from modelestep import modelestep

import matplotlib.pyplot as plt



data = parseurlog2('entries.txt',9)
print(data)

tabx=[]

taby=[]

tabtheta=[]

tabv=[]



for i in data:

	output =modelestep(float(i[0]),float(i[1]),float(i[2]),float(i[3]),float(i[4]),float(i[5]),float(i[6]),float(i[7]),float(i[8]))