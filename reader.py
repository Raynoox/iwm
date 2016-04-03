import matplotlib.pyplot as plt
import glob
import csv
import numpy as np
from scipy.interpolate import spline
 
 
def str_to_float(string):
    try:
        string = float(string)
    except ValueError:
        pass
    return string
 
 
 
 
def read_file(filename):
    arr = []
    with open(filename, newline='') as csvfile:
        handler = csv.reader(csvfile, delimiter=',')
        for row in handler:
            arr.append(row) 
    return arr  
 
 
 
 
def prepare_array(arr):
    new_arr = []
    for index, row in enumerate(arr, start=0):
        temp=[]
        temp.append(index)
        for cell in row[1:]:
            temp.append(str_to_float(cell))
        new_arr.append(temp)
    return new_arr
 


def ecg_plot(arr, ax1,signum):
	x, y = [], []
	for row in arr[2:]:
		x.append(row[0])
		print(row[0])
		y.append(row[signum])
	ax1.plot(x,y)
 
def main():
    fig = plt.figure('ECG chart')
    axes = []
    for i in range(1,16):
         ax1 = plt.subplot(16, 1 , i)
         axes.append(ax1)
    for i in range(1,16):
         ecg_plot(prepare_array(read_file('samples.csv')), axes[i-1], i)
    plt.show()
     
 
if __name__ == '__main__':
    main()
    
