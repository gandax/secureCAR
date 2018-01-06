#coding : utf8
import numpy as np

def parseurlog2(filename,n):

	
	file = open(filename,'r')
	count = 0
	for line in file:
	   count += 1
	print(count)
	file.close()
	file = open(filename,'r')
	data = [[""]*n for i in range(count)]

	i=0
        
	for line in file:
		
		j=0
		
		for char in line:
			if char != '#':
				data[i][j] = data[i][j] + char
			else:
				j += 1
			if (j == n):
				break
			
                i+=1
			
		
	file.close()
	return data
