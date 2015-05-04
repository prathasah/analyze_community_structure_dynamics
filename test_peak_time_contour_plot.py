import re 
import os
import numpy as np
import zipfile
import matplotlib.pyplot as plt
import epidemic_calculations as ec
from pylab import *

#################################################################################
# Code to plot contour plot of peak epidemic size results. x axis: Q values, y axis: T values, z = peak epidemic size. 
# Three subplots for three degree distribution type
#################################################################################

#replace with the link to folder where zip files of epidemic results are located
os.chdir("/home/pratha/Dropbox/SB_Lab_Pratha/Henry_file/Epidemic_results")
##########################################################################################

Qrange=np.arange(0.0, 0.9, 0.1)
Trange= np.arange(0.1, 0.35, 0.05)
sigma = 0.2
count=0
average_epi_size={}
error={}
levels = np.arange(0, 150, 10)
norm = cm.colors.Normalize(vmax= 150, vmin= 0)
cmap = cm.seismic

##add graphtype over here
graphtype=["poisson"]
#########################################################
for graph in graphtype:
    print ("graph="),graph
    plt.clf()
    Z = np.zeros((len(Trange), len(Qrange)))
    col = -1 
    for Q in Qrange:
    	col+=1
    	row = -1
        for T in Trange:
        	row+=1
		total_peak_time=[]
		zf=zipfile.ZipFile("Epidemic_"+graph+"N10000_Q"+str(Q)+"_T_"+str(T)+"_sigma_"+str(sigma)+".zip", "r")
		
        	for filecount in xrange (1):
        		file1="INF_"+graph+"n10000_m10_d10_Q"+str(Q)+"T_"+str(T)+"_iter"+str(filecount)+".txt"
		    	f1=(zf.open(file1))
			lines=f1.readlines()
			x=0
			infected_list={}
			for line in lines:
				data=re.split(',', line)[1:]
				data[0]=data[0][2:]
				data[-1]=data[-1][:-2]
				infected_list[x]=[int(num) for num in data]
				x+=1
            		total_peak_time.append([ec.most_common(infected_list[x]) for x in xrange(500) if ec.is_epidemic(infected_list[x])==True])
        
        	peak_list=[x for sublist in total_peak_time for x in sublist]
        	#print peak_list
        	if len(peak_list)==0:peak_list=[0] 
		Z[row][col]= np.mean(peak_list) #mean of all the epidemic size above the epidemic criteria
		print Q, T, np.mean(peak_list)

    #################################   
    print Z
    CS = plt.contourf(Qrange, Trange, Z, levels, cmap=plt.cm.get_cmap(cmap, len(levels)-1))
    plt.title("Peak time, graph = "+graph)
    plt.xlabel("Modularity, Q")
    plt.ylabel("Transmissibility, T")
    cbar = plt.colorbar(CS)
    #cbar.add_lines(CS)
    #plt.xlim([0,0.9])
    #plt.ylim([0.1,0.35])
    
    plt.savefig("peak_time_graph_"+graph+".png")
    plt.show()

        
        
