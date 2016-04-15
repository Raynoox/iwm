import matplotlib.pyplot as plt
import matplotlib.lines as lines
import glob
import csv
import numpy as np
from scipy.interpolate import spline
from matplotlib.widgets import Button
YLABEL_LIST = ['i', 'ii', 'iii', 'avr', 'avl','avf','v1','v2','v3','v4','v5','v6','vx','vy','vz']

final_list=[]
ylen = 0
Y = [] ## Y glownego wykresu
X = [] ## X glownego wykresu?
Fs = 1000
#Ts = 1/Fs ## tutaj chyba dlugosc sygnalu w sek? (to 10) not sure though
k = 0
T = 0
frq = []
FFTaxes = [[] for i in range(13)]
axes = []
class Index(object):
    ind = 0
    fftax = []
    def next(self, event):
        self.ind += 1
        global axes
        for i in range(1,13):
                axes[i-1].cla()
               # print(len(frq), len(self.fftax[i-1]))
                axes[i-1].plot(frq,self.fftax[i-1])
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        for i in range(1,13):
                axes[i-1].cla()
                axes[i-1].plot(X[i-1],Y[i-1])
       # ydata = np.sin(2*np.pi*freqs[i]*t)
     #   l.set_ydata(ydata)
        plt.draw()
    def update_fft(self, fftaxes):
        print("Update")
        print(fftaxes)
        self.fftax = fftaxes
        #print(fftax)

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
	global X
	global Y
	X.append(x)
	Y.append(y)
	if(signum==1):
		find_QRS(y)
	ax1.plot(X[signum-1],Y[signum-1])
	fftax = np.fft.fft(y)/ylen
	fftax = fftax[0:int(ylen/2)]
	global FFTaxes
	FFTaxes[signum-1] = fftax
	#FFTaxes.append(fftax)
	print(len(fftax))

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
    for i in range(0,12):
        axes[i].set_yticks([])
        axes[i].set_xticks([])
        axes[i].set_xlim([0,ylen])
        axes[i].set_ylabel(YLABEL_LIST[i])
        for j in range(0,len(xs)-1,2):
               axes[i].add_line(lines.Line2D(xs[j:j+2], ys[j:j+2], linewidth=1, color = 'red'))
        #axes[i].grid()
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
def calculate_bpm():
	sum = 0
	for index,i in enumerate(final_list[1:]):
		sum = sum + (final_list[index+1]-final_list[index])
	sum = sum/len(final_list)
	return sum;
def main():
    fig = plt.figure('ECG chart')
    global axes
    for i in range(1,13):
         ax1 = plt.subplot(13, 1 , i)
         axes.append(ax1)
    
    for i in range(1,13):
         fft = []
         ecg_plot(prepare_array(read_file('samples1.csv')), axes[i-1],i)
    ecg_plot_info(axes)
    fig.subplots_adjust(hspace = 0.1, left = 0.05, right = 0.95, top = 0.95, bottom = 0.05)
    print("Uderzenia na sekunde: ")
    print(60000/calculate_bpm())
    callback = Index()
    callback.update_fft(FFTaxes)
    axprev = plt.axes([0.7, 0.01, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.01, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)
    bnext.on_clicked(callback.next)
    plt.show()
     
 
if __name__ == '__main__':
    main()
    
