from matplotlib import pyplot as plt
import numpy as np

def main():


    fin = open("../processed.txt","r")
    
    data = {}

    zones = [i for i in range(10,121,5)]
    
    tt = [i for i in range(10,61,5)]



    skip = ["typeE", "typeS", "provider", "tankThreshold", "zones", "algorithm", "acs","policy"]
    features_column= {}
    
    f = open("../processed.txt","r")

    algoColumn=-1
    tColumn = -1
    acsColumn = -1
    zColumn = -1
    
    features=[]
    for line in f:
        ln = line.strip().split(" ")
        for val in ln: 
            if(val not in skip):
                print
                features_column[val]=int(ln.index(val))    
                features.append(val)       
            else:
                if(val == "algorithm"):
                    algoColumn=int(ln.index(val))          
                elif(val == "tankThreshold"):
                    tColumn=int(ln.index(val))          
                elif(val == "acs"):
                    acsColumn=int(ln.index(val))          
                elif(val == "zones"):
                    zColumn=int(ln.index(val))                              
        break
    f.close()

    print(features_column.keys())
    print(len(features_column))
    acses = [2,4,6]
    for algorithm in ["max_time", "max_parking", "rnd"]:
        data[algorithm]={}
        for val in features_column:
            data[algorithm][val] = [[0 for j in range(0,len(zones)*len(acses))] for k in range(0,len(tt))]

    
    i=0
    for line in fin:
        ln = line.strip().split(" ")
        if(i==0): 
            i=1
            continue
        
        algo = ln[algoColumn]        
        t = int(ln[tColumn])
        acs = int(ln[acsColumn])
        z = int(ln[zColumn])

        y = tt.index(t)
        x = zones.index(z)*len(acses)+acses.index(acs)
        for feature in features_column:
            data[algo][feature][y][x] = float(ln[features_column[feature]])
    
    
    xlabels = []
    for val in zones:
        xlabels.append(str(val)+"_2")
        #xlabels.append(str(val)+"_4")
        #xlabels.append(str(val)+"_6")
    '''
    for algorithm in data:
        for feature in data[algorithm]:
            toplot= np.array(data[algorithm][feature])
            fig, ax = plt.subplots()
            heatmap = ax.pcolor(toplot)
            ax.set_ylim(0,len(tt))
            ax.set_xlim(0,len(zones)*len(acses))
            ax.set_yticks([i+0.5 for i in range(0,len(tt))])
            ax.set_yticklabels(tt)
            ax.set_xticks([i for i in range(0,len(xlabels)*3,3)])
            ax.set_xticklabels(xlabels,rotation=60)
            fulltitle = algorithm + " "+feature
            ax.set_title(fulltitle)
            ax.set_ylabel("TT")
            ax.set_xlabel("Zones_Acs")
            cbar = fig.colorbar(heatmap)        
            plt.tight_layout()            
            plt.savefig("../fig/"+algorithm+"_"+feature+".png")
            plt.close()
    

    print("by feature")
    
    for feature in data[algorithm]:
        k=0
        fig, axes = plt.subplots(len(data), figsize = (10,20))
        for algorithm in data:
            ax = axes[k]
            toplot= np.array(data[algorithm][feature])
            heatmap = ax.pcolor(toplot)
            ax.set_ylim(0,len(tt))
            ax.set_xlim(0,len(zones)*len(acses))
            ax.set_yticks([i+0.5 for i in range(0,len(tt))])
            ax.set_yticklabels(tt)
            ax.set_xticks([i for i in range(0,len(xlabels)*3,3)])
            ax.set_xticklabels(xlabels,rotation=60)
            fulltitle = algorithm + " "+feature
            ax.set_title(fulltitle)
            ax.set_ylabel("TT")
            ax.set_xlabel("Zones_Acs")
            cb1 = fig.colorbar(heatmap, ax=ax)
            #cb1.ax.tick_params(labelsize=20)
            k+=1
        plt.tight_layout()            
        plt.savefig("../fig/"+feature+".png")
        plt.close()'''

    print("by algo")
    for algorithm in data:
        fig, axes = plt.subplots(4,4, figsize=(60, 40))
        k=0
        fig.suptitle(algorithm, fontsize=60)
        for feature in features:
            if(feature=="reroute"): continue
            j=k%4
            i=int(k/4)
            ax = axes[i,j]
            toplot= np.array(data[algorithm][feature])
            heatmap = ax.pcolor(toplot)
            ax.set_ylim(0,len(tt))
            ax.set_xlim(0,len(zones)*len(acses))
            ax.set_yticks([i+0.5 for i in range(0,len(tt))])
            ax.set_yticklabels(tt,fontsize=24)
            ax.set_xticks([i for i in range(0,len(xlabels)*3,3)])
            ax.set_xticklabels(xlabels,rotation=60,fontsize=24)
            fulltitle = feature
            ax.set_title(fulltitle,fontsize=50)
            ax.set_ylabel("TT",fontsize=50)
            ax.set_xlabel("Zones_Acs",fontsize=50)
            cb1 = fig.colorbar(heatmap, ax=ax)
            cb1.ax.tick_params(labelsize=35)
            k+=1
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])            
        plt.savefig("../fig/"+algorithm+".png")
        plt.close()


    return



main()
