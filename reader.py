import matplotlib.pyplot as plt
import matplotlib.lines as lines
import glob
import csv
import pywt
import numpy as np
import scipy.io as spio
from scipy.interpolate import spline
from matplotlib.widgets import Button
YLABEL_LIST = ['i', 'ii', 'iii', 'avr', 'avl','avf','v1','v2','v3','v4','v5','v6','vx','vy','vz']
titles = ['ECG signal','FFT','Wavelet Transform Approx','Wavelet Transform detail coef']
final_list=[]
WT_times = 1 ## ile razy przepuscic wavelet transofrm >=1
mV = 1.0
ylen = 0
axes_xlim = [10000,50,0,0] ## to 10000 to ilosc sekund, trzeba byloby zmienac na ylen
Y = []
X = []
Fs = 1000
k = 0
T = 0
frq = []
FFTaxes = [[] for i in range(13)] ##tablica z wartosciami Y fft
WTaxesA = [[] for i in range(13)] ## -||- wt approx.
WTaxesD = [[] for i in range(13)] ## -||- wt detail coef
axes = []
class Index(object):
    ind = 0
    allAxesValuesY = []
    allAxesValuesX = []
    fftax = []
    plot_number = 0
    def __init__(self):
        self.allAxesValues = []
        self.fftax = []
        self.plot_number = 4 ## ile chce sie wykresów
        self.allAxesValuesY = [[] for i in range(self.plot_number)]
        self.allAxesValuesX = [[] for i in range(self.plot_number)]
    def next(self, event):
        self.ind += 1
        for i in range(0,12):
                global axes
                axes[i].cla()
                axes[i].plot(self.allAxesValuesX[self.ind%self.plot_number][i],self.allAxesValuesY[self.ind%self.plot_number][i]) ## zamiast 1 pozniej ind
                axes[i].set_xlim(0,axes_xlim[self.ind%self.plot_number]) ## zeby ladniej wygladalo, powyzej 40 jest prosta linia
        plt.title(titles[self.ind%self.plot_number])
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        plt.title(titles[self.ind%self.plot_number])
        for i in range(0,12):
                global axes
                axes[i].cla()
                axes[i].plot(self.allAxesValuesX[self.ind%self.plot_number][i],self.allAxesValuesY[self.ind%self.plot_number][i])
                axes[i].set_xlim(0,axes_xlim[self.ind%self.plot_number])
        plt.draw()
    def update_genY(self, ax, plotId):
        self.allAxesValuesY[plotId].append(ax)
    def update_genX(self, ax, plotId):
        self.allAxesValuesX[plotId].append(ax)
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
 


def ecg_plot(data, ax1,signum):
	x, y = [], []
	print("Tworze wykres numer %d" % signum)
	#for row in arr[2:]:
	#	x.append(row[0])
	#	y.append(row[signum])
	x, y =[], []
	for index, cell in enumerate(data[signum-1]):
		x.append(index)
		y.append(float(cell)/mV)
		
	global X
	global Y
	X.append(x)
	Y.append(y)
	if(signum==1):
		find_QRS(y)
	ax1.plot(X[signum-1],Y[signum-1])
	fftax = np.fft.fft(y)/ylen
	fftax = fftax[0:int(ylen/2)]

	(wtaxA, wtaxD) = pywt.dwt((y),'db1') ##wt approximation + detail coefficients cokolwiek to znaczy
	if(WT_times > 1):
		for i in range(WT_times-1):
			(wtaxA,wtaxD) = pywt.dwt((wtaxA),'db1')

	global FFTaxes
	global WTaxesA
	global WTaxesD
	FFTaxes[signum-1] = fftax
	WTaxesA[signum-1] = wtaxA
	WTaxesD[signum-1] = wtaxD


def ecg_plot_info(axes):
    line = []
    for i in final_list:
        line.append((i,1.5))
        line.append((i,-1))
    (xs, ys) = zip(*line)
    for i in range(0,12):
        axes[i].set_yticks([])
        axes[i].set_xticks([])
        axes[i].set_xlim([0,ylen])
        axes[i].set_ylabel(YLABEL_LIST[i])
        for j in range(0,len(xs)-1,2):
               axes[i].add_line(lines.Line2D(xs[j:j+2], ys[j:j+2], linewidth=1, color = 'red'))
    axes[11].set_xlabel('Czas [ms]')
    axes[11].set_xticks(np.linspace(0,10000, 11))

def find_QRS(y):
         iter = list(range(0,len(y)+1,250))
         ### GLOBAL VARIABLES - mozna przeniesc gdzies indziej po wczytaniu z pliku
         global ylen
         ylen = len(y)
         global k
         k = np.arange(ylen)
         global T
         T = ylen/Fs
         global frq
         frq = k/T
         frq = frq[0:int(ylen/2)]
         ###
         maxlist=[]
         xlist=[]
         v2=[]
         for i in range(0,len(iter)-1):
              maxlist.append(max(y[iter[i]:iter[i+1]]))
              v = y[iter[i]:iter[i+1]].index(max(y[iter[i]:iter[i+1]]))
              v2.append( int(v) + int(iter[i]))
         vmax = max(y)
         for licz, i in enumerate(maxlist):
              if(vmax*0.5 < i):
                      final_list.append(v2[licz])
def calculate_bpm():
	sum = 0
	for index,i in enumerate(final_list[1:]):
		sum = sum + (final_list[index+1]-final_list[index])
	sum = sum/len(final_list)
	return sum;
def main():
    for i in range(-10,10):
         print(i,i%4)
    fig = plt.figure('ECG chart')
    callback = Index()
    data = spio.loadmat('s0026lrem_short.mat')
    data = data['val']
    print(data, len(data))
    print(len(data[1]))
    global axes
    for i in range(1,13):
         ax1 = plt.subplot(13, 1 , i)
         axes.append(ax1)
    


    for i in range(1,13):
         fft = []
         global axes_xlim
         #ecg_plot(data, prepare_array(read_file('samples1_long.csv')), axes[i-1],i)
         ecg_plot(data, axes[i-1],i)
         callback.update_genY(Y[i-1],0)
         print(len(Y[i-1]))
         callback.update_genX(X[i-1],0)
         axes_xlim[0] = ylen

         callback.update_genY(FFTaxes[i-1],1)
         callback.update_genX(frq,1)
         
         callback.update_genY(WTaxesA[i-1],2)
         callback.update_genX(range(0,len(WTaxesA[i-1])),2)
         axes_xlim[2] = len(WTaxesA[i-1])

         callback.update_genY(WTaxesD[i-1],3)
         callback.update_genX(range(0,len(WTaxesD[i-1])),3)
         axes_xlim[3]= len(WTaxesD[i-1])



    ecg_plot_info(axes)
    fig.subplots_adjust(hspace = 0.1, left = 0.05, right = 0.95, top = 0.95, bottom = 0.05)
    print("Uderzenia na sekunde: ")
    print(60000/calculate_bpm())

    axprev = plt.axes([0.7, 0.01, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.01, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)
    bnext.on_clicked(callback.next)
    plt.show()
     
 
if __name__ == '__main__':
    main()
    
