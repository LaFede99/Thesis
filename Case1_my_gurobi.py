import gurobipy as gp
from Package_scheduling import *
from Plotting import Plot_gantt

P=Read_patients('Prova_finalissima.txt')
N_patients=int(len(P)/3)

pos=None
#pos=[0, 12, 2, 7, 11, 9, 13, 5, 10, 14, 3, 8, 6, 4, 1]
#P=Impose_schedule_to_case1(P,pos)

# New model 
m=gp.Model('my_model')

# Variables
I=range(3) ; J=range(N_patients)
C={} ; OR={}
M=3000

C=m.addVars(I,J,vtype=gp.GRB.INTEGER,name='C')
OR=m.addVars(J,vtype=gp.GRB.BINARY,name='OR')


# Objective function
m.setObjective(C[3-1,N_patients-1],gp.GRB.MINIMIZE)

# Constraints
m.addConstr( C[1-1,1-1] - P[1-1,1-1] == 0, name='c000' )
m.addConstr( OR[N_patients-1] == 1 , name='c001' )

for j in J:
    m.addConstr( C[2-1,j] - P[2-1,j] - C[1-1,j] == 0, name='c1' )
    m.addConstr( C[3-1,j] - P[3-1,j] - C[2-1,j] == 0, name='c2' )

for j in range(N_patients-1):
    m.addConstr( C[1-1,j+1] - P[1-1,j+1] - C[1-1,j]  >= 0, name='c3' )
    m.addConstr( C[3-1,j+1] - P[3-1,j+1] - C[3-1,j] + P[3-1,j] >= 0, name='c5' )
    m.addConstr( C[2-1,j+1] - P[2-1,j+1] - C[2-1,j] - P[3-1,j] * OR[j] >= 0, name='c6' )
    m.addConstr( C[3-1,j] - P[3-1,j] - C[1-1,j+1] + M * (OR[j]) >= 0 , name='c8')

for j in range(N_patients-2):
    m.addConstr( C[1-1,j+2] - P[1-1,j+2] - C[3-1,j] + M * OR[j] >= 0 , name='c7')

# Solving
m.optimize()

#Display
C,OR=Gurobi_to_values(C,OR)

Display_schedule(C,OR,pos)

Plot_gantt(C,P,OR,pos,'gurobi1_.png')

