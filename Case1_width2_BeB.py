from Package_scheduling import *
from Plotting import Plot_gantt
from Schedule_generators import *

P=Read_patients('Prova_pazienti_irrealistica.txt')
N_patients=int(len(P)/3)

pos=None
#pos=[0, 12, 2, 7, 11, 9, 13, 5, 10, 14, 3, 8, 6, 4, 1]
#P=Impose_schedule_to_case1(P,pos)

branch1=Impose_placement(P,{0:0})     #the one that will hold AOP ending solutions
branch2=Impose_placement(P,{0:1})     #the one that will hold  OR ending solutions

for i in range(1,N_patients):

    branch1_OR=branch1.add_patient(Take_single_patient(P,i),1)
    branch1_AOP=branch1.add_patient(Take_single_patient(P,i),0)
    branch2_OR=branch2.add_patient(Take_single_patient(P,i),1)
    branch2_AOP=branch2.add_patient(Take_single_patient(P,i),0)

    if (branch1_AOP.OF<=branch2_AOP.OF):
        branch1=Solution.copy_from(branch1_AOP)
    else:
        branch1=Solution.copy_from(branch2_AOP)

    if (branch1_OR.OF<=branch2_OR.OF):
        branch2=Solution.copy_from(branch1_OR)
    else:
        branch2=Solution.copy_from(branch2_OR)


if (branch1.OF<=branch2.OF):
    winner=Solution.copy_from(branch1)
else:
    winner=Solution.copy_from(branch2)

print(winner)

#Plot_gantt(winner.C,P,winner.OR,pos,'Dynamic_attempt.png')
    














