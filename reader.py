import matplotlib.pyplot as plt
import matplotlib.lines as lines
import glob
import csv
import numpy as np
from scipy.interpolate import spline
 
YLABEL_LIST = ['i', 'ii', 'iii', 'avr', 'avl','avf','v1','v2','v3','v4','v5','v6','vx','vy','vz']

final_list=[]

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
	print("Tworze wykres numer %d" % signum)
	for row in arr[2:]:
		x.append(row[0])
		#print(row[0])
		y.append(row[signum])
	if(signum==1):
		find_QRS(y)
	ax1.plot(x,y)

def ecg_plot_info(axes):
    #ax1.set_xlabel('Rozegranych gier (x1000)')
    #ax1.set_ylabel('Odsetek wygranych gier [%]')
    #ax1.set_xlim([0,500000 / 1000])
    #ax1.set_ylim([60, 100])
    #ax1.legend(loc=4, fontsize='medium')
    #ax1.grid() 
 
    #ax2.set_xlabel('Pokolenie')
    #ax2.set_xlim([0, 500000 / 1000])
    #ax2.set_ylim([60, 100])
    #ax2.set_xticks([0,100,200,300,400,500])
    #ax2.set_xticklabels(['0','40','80','120','160','200']);
    line = []
    for i in final_list:
        #print(i)
        line.append((i,1.5))
        line.append((i,-1))
    (xs, ys) = zip(*line)
    #print(xs)
    for i in range(0,15):
        axes[i].set_yticks([])
        axes[i].set_xticks([])
        axes[i].set_xlim([0,10000])
        axes[i].set_ylabel(YLABEL_LIST[i])
        for j in range(0,len(xs)-1,2):
               axes[i].add_line(lines.Line2D(xs[j:j+2], ys[j:j+2], linewidth=1, color = 'red'))
        #axes[i].grid()
    axes[14].set_xlabel('Czas [ms]')
    axes[14].set_xticks([0,2000,4000,6000,8000,10000])

def find_QRS(y):
         iter = list(range(0,10001,250))
         maxlist=[]
         xlist=[]
         v2=[]
         for i in range(0,len(iter)-1):
             # print(max(y[iter[i]:iter[i+1]]))
              maxlist.append(max(y[iter[i]:iter[i+1]]))
              v = y[iter[i]:iter[i+1]].index(max(y[iter[i]:iter[i+1]]))
              v2.append( int(v) + int(iter[i]))

              #print(int(v),int(iter[i]),v2)
         vmax = max(y)
         for licz, i in enumerate(maxlist):
              if(vmax*0.5 < i):
                      #final_list.append(y[iter[licz]:iter[licz+1]].index(i))
                      final_list.append(v2[licz])

def main():
    fig = plt.figure('ECG chart')
    axes = []
    for i in range(1,16):
         ax1 = plt.subplot(16, 1 , i)
         axes.append(ax1)
    for i in range(1,16):
         ecg_plot(prepare_array(read_file('samples.csv')), axes[i-1], i)
    ecg_plot_info(axes)
    fig.subplots_adjust(hspace = 0.0, left = 0.05, right = 0.95, top = 0.95, bottom = 0.05)
    plt.show()
     
 
if __name__ == '__main__':
    main()
    
