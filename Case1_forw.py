from Package_scheduling import *
from Plotting import Plot_gantt

P=Read_patients('Prova_pazienti_irrealistica.txt')
N_patients=int(len(P)/3)

#pos=None
pos=[0, 12, 2, 7, 11, 9, 13, 5, 10, 14, 3, 8, 6, 4, 1]
P=Impose_schedule_to_case1(P,pos)

B=Empty_schedule(P)
OR={}

# Solving
B[1-1,0]=0
C_OR=0
C_AOP=P[1-1,0]

for i in range( N_patients -1 ):

    one=P[1-1,i+1] <= (B[1-1,i] + P[1-1,i]) + P[2-1,i] - C_AOP
    two=P[1-1,i+1] <= (B[1-1,i] + P[1-1,i]) + P[2-1,i] + P[3-1,i] - C_AOP

    if one : 
        #print(1)
        B[2-1,i] = B[1-1,i] + P[1-1,i]
        B[3-1,i] = B[2-1,i] + P[2-1,i]
        OR[i] = 0
        B[1-1,i+1] = B[3-1,i] - P[1-1,i+1]
        C_OR = B[2-1,i] + P[2-1,i]
        C_AOP = B[3-1,i] + P[3-1,i]

    elif not one and two :  
        #print(2)
        B[2-1,i] = B[1-1,i] + P[1-1,i]
        B[3-1,i] = B[2-1,i] + P[2-1,i]
        OR[i] = 1
        B[1-1,i+1] = B[3-1,i] + P[3-1,i] - P[1-1,i+1]
        C_AOP= B[1-1,i+1] + P[1-1,i+1]    
        C_OR = B[3-1,i] + P[3-1,i]

    elif not one and not two :   
        #print(3)
        B[2-1,i] = B[1-1,i] + P[1-1,i]
        B[3-1,i] = B[2-1,i] + P[2-1,i]
        OR[i] = 1
        B[1-1,i+1] = C_AOP 
        C_AOP = B[1-1,i+1] + P[1-1,i+1]
        C_OR = B[3-1,i] + P[3-1,i]

B[2-1,N_patients-1] = B[1-1,N_patients-1] + P[1-1,N_patients-1]
C_OR = B[2-1,N_patients-1] + P[2-1,N_patients-1]
B[3-1,N_patients-1] = C_OR
OR[N_patients-1]=1
C_OR = B[3-1,N_patients-1] + P[3-1,N_patients-1]

C=Completion_from_begin(B,P)

# Display
Display_schedule(C,OR,pos)

Plot_gantt(C,P,OR,pos,'prova_forw_prova.png')





    








