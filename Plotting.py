import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def Plot_gantt(C,P,OR,pos,filename):
    def rect(C,P,OR):
        x=C-P
        y=0.3+0.4*(1-OR)-0.15
        return ((x,y),P,0.3,0)
    
    def lab_pos(C,P,OR):
        x=C-P/2 -2
        y=0.3+0.4*(1-OR)-0.015
        return x,y
    
    if pos is None:
        pos=range(int(len(C)/3))

    gen_OR = {(i, j): (0 if i == 0 else (1 if i == 1 else OR[j])) for j in OR for i in range(3)}
    colors=['#ACECF7','#BE95C4','#C7F0A3']
    OF=max(C.values())

    fig,ax=plt.subplots(figsize=((int(len(C)/3)+3)*2,6))

    ax.set_xlim(0,OF+10)
    ax.set_ylim(0,1)

    ax.set_xlabel("Time [min]",fontsize=20)
    ax.set_title("Schedule Gantt Chart",fontsize=25)

    ax.set_xticks(np.arange(0, OF+10, 10 if OF<1000 else 25))
    ax.set_yticks([0.3, 0.7])
    ax.set_yticklabels(["OR", "AOP"],fontsize=20)

    #ax.grid(True,alpha=0.2)

    legend_handles = [patches.Patch(color=colors[0], label='Anesthesia'),
                      patches.Patch(color=colors[1], label='Surgery'),
                      patches.Patch(color=colors[2], label='Awakening')]
    ax.legend(handles=legend_handles,loc='lower right')

    for i,j in C:
        ax.add_patch(patches.Rectangle(*rect(C[i,j],P[i,j],gen_OR[i,j]),facecolor=colors[i],edgecolor='black'))
        ax.axvline(x=C[i,j]-P[i,j], color='black', linestyle='--',linewidth=0.1)
        ax.axvline(x=C[i,j], color='black', linestyle='--',linewidth=0.1)
        ax.text(*lab_pos(C[i,j],P[i,j],gen_OR[i,j]),f'{pos.index(j)}')

    fullpath=os.path.join('Gantt',filename)
    plt.savefig(fullpath)
    plt.close()
