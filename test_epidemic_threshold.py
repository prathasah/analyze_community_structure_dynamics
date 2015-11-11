import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import os
import re 
##############################################################################
Qrange=[0.88]
betarange = [0.0222]
Trange = [0.1]
sigma = 0.2
graph="geometric"
num_modules =100
bins=range(0,10000, 50)
#################################################################################
os.chdir("/home/pratha/Dropbox (Bansal Lab)/SBLab_Community_structure_dynamics/Community_Structure_Dynamics/analyze_epidemic_results/Epidemic_results_6July_2015")
##########################################################################################
##############################################################################
for Q in Qrange:
    for T in Trange:
        print ("t="), T
        zf=zipfile.ZipFile("Epidemic_"+graph+"N10000_m"+str(num_modules)+"_Q"+str(Q)+"_T_"+str(T)+"_sigma_"+str(sigma)+".zip", "r")
	total_epi_size=[]
        for filecount in xrange(50):    
            print Q, T, filecount
            file1="INF_"+graph+"n10000_m"+str(num_modules)+"_d10_Q"+str(Q)+"T_"+str(T)+"_iter"+str(filecount)+".txt"
            f1=(zf.open(file1))
            ############################
	    lines=f1.readlines()
	    x=0
	    infected_list={}
	    for line in lines:
		data=re.split(',', line)[1:]
		data[0]=data[0][2:]
		data[-1]=data[-1][:-2]
		infected_list[x]=[int(num) for num in data]
		x+=1
	    ############################	    
	    for x in xrange(500): total_epi_size.append(len([num for num in infected_list[x] if num>0]))
 
        plt.hist(total_epi_size,bins, normed=True)
        plt.ylim([0, 0.001])
        plt.axvline(x=100, color="k", linestyle="--")
        plt.xlim([0,5000])
        plt.title("Frequency distribution, "+str(graph)+" graphs, m="+str(num_modules)+" Q= "+str(Q)+ ", T= "+str(T))
        plt.xlabel('Epidemic size')
        plt.ylabel('Frequency')
        filname="Frequency distribution, "+str(graph)+" graphs, m="+str(num_modules)+" , Q= "+str(Q)+ ", T= "+str(T)+".png"
        plt.savefig(filname)
        plt.clf()
    
                
