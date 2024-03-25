from Package_scheduling import *
from Plotting import Plot_gantt

P=Read_patients('Prova_pazienti_irrealistica.txt')
N_patients=int(len(P)/3)

pos=None
#pos=[0, 12, 2, 7, 11, 9, 13, 5, 10, 14, 3, 8, 6, 4, 1]
#P=Impose_schedule_to_case1(P,pos)

C=Empty_schedule(P)
OR={}

#Solving

C[3-1,N_patients-1]=0
C[2-1,N_patients-1]=-P[3-1,N_patients-1]
C[1-1,N_patients-1]=-(P[3-1,N_patients-1]+P[2-1,N_patients-1])
OR[N_patients-1]=1
C_OR=C[1-1,N_patients-1]
C_AOP=C[1-1,N_patients-1]-P[1-1,N_patients-1]
supp=1000

for i in range(N_patients-2,-1,-1):
    one=P[3-1,i]<=supp-C[1-1,i+1]
    two=P[2-1,i]>=P[1-1,i+1]
    three=P[3-1,i]+P[2-1,i]>=P[1-1,i+1]

    if (one and two):

        OR[i]=0
        C[3-1,i]=C[1-1,i+1]+P[3-1,i]
        C[2-1,i]=C[1-1,i+1]
        C[1-1,i]=C[2-1,i]-P[2-1,i]
        supp=C[1-1,i+1]-P[1-1,i+1]

    elif (one and not two and three) or (not one and three):

        OR[i]=1
        C[3-1,i]=C[1-1,i+1]
        C[2-1,i]=C[3-1,i]-P[3-1,i]
        C[1-1,i]=C[2-1,i]-P[2-1,i]
        supp=C[1-1,i+1]-P[1-1,i+1]

    elif (one and not two and not three) or (not one and not three):

        OR[i]=1
        C[1-1,i]=C[1-1,i+1]-P[1-1,i+1]
        C[2-1,i]=C[1-1,i]+P[2-1,i]
        C[3-1,i]=C[2-1,i]+P[3-1,i]
        supp=C[1-1,i+1]-P[1-1,i+1]

    else:
        raise ValueError('Error in patients scheduling')

C = {key: (value-C[1-1,0]+P[1-1,0]) for key, value in C.items()}

#Plotting
Display_schedule(C,OR,pos)

Plot_gantt(C,P,OR,pos,'prova_back_.png')

















