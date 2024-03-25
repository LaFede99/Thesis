import gurobipy as gp
from Package_scheduling import *
from Plotting import Plot_gantt

P=Read_patients('Prova_pazienti_irrealistica.txt')
N_patients=int(len(P)/3)

# New Model
m=gp.Model('my_model')
#m.setParam('TimeLimit',10)

# Variables initialization
I=range(3) ; J=range(N_patients)
BigCycles=[(i1,j1,i2,j2) for i1 in I for j1 in J for i2 in I for j2 in J if j1!=j2]
C={} ; OR={} ; Prec={}
M=5000

# Variables creation
F=m.addVar(vtype=gp.GRB.INTEGER,name='F')
C=m.addVars(I,J,vtype=gp.GRB.INTEGER,name='C')
OR=m.addVars(J,vtype=gp.GRB.BINARY,name='OR')
Prec=m.addVars( BigCycles ,vtype=gp.GRB.BINARY, name='Prec' )

# Objective function
m.setObjective(F,gp.GRB.MINIMIZE)

# Constraints
for j in J:
    m.addConstr( C[1-1,j] - P[1-1,j] >= 0, name='c1')
    m.addConstr( C[2-1,j] - P[2-1,j] - C[1-1,j] == 0, name='c2')
    m.addConstr( C[3-1,j] - P[3-1,j] - C[2-1,j] == 0, name='c3')
    m.addConstr( F - C[3-1,j] >= 0, name='c10')

for j1 in J:
    for j2 in J:
        if (j1 != j2):
            m.addConstr( C[2-1,j1] - P[2-1,j1] - C[2-1,j2] + M * Prec[2-1,j1,2-1,j2] >=0 , name='c4')
            m.addConstr( C[2-1,j1] - P[2-1,j1] - C[3-1,j2] + M * Prec[2-1,j1,3-1,j2] + M * (1-OR[j2]) >=0 , name='c5')
            m.addConstr( C[3-1,j1] - P[3-1,j1] - C[2-1,j2] + M * Prec[3-1,j1,2-1,j2] + M * (1-OR[j1]) >=0 , name='c6')
            m.addConstr( C[1-1,j1] - P[1-1,j1] - C[1-1,j2] + M * Prec[1-1,j1,1-1,j2] >=0 , name='c7')
            m.addConstr( C[1-1,j1] - P[1-1,j1] - C[3-1,j2] + M * Prec[1-1,j1,3-1,j2] + M * OR[j2] >=0 , name='c8')
            m.addConstr( C[3-1,j1] - P[3-1,j1] - C[1-1,j2] + M * Prec[3-1,j1,1-1,j2] + M * OR[j1] >=0 , name='c9')
            m.addConstr( C[3-1,j1] - P[3-1,j1] - C[3-1,j2] + M * Prec[3-1,j1,3-1,j2] + M * (OR[j1]+OR[j2]) >=0 , name='c91')     
            m.addConstr( Prec[1-1,j1,1-1,j2] + Prec[1-1,j2,1-1,j1] -1 ==0 , name='c11')
            m.addConstr( Prec[2-1,j1,2-1,j2] + Prec[2-1,j2,2-1,j1] -1 ==0 , name='c12')
            m.addConstr( Prec[3-1,j1,3-1,j2] + Prec[3-1,j2,3-1,j1] -1 ==0 , name='c13')
            m.addConstr( Prec[2-1,j1,3-1,j2] + Prec[3-1,j2,2-1,j1] -1 ==0 , name='c14')
            m.addConstr( Prec[1-1,j1,3-1,j2] + Prec[3-1,j2,1-1,j1] -1 ==0 , name='c15')

# Solving
m.optimize()

# Formatting and reordering
pos=Extract_sequence(C)

C,P,OR=Reorder_schedule(C,P,OR,pos)

C,OR=Gurobi_to_values(C,OR)

# Printing
Display_schedule(C,OR,pos)

Plot_gantt(C,P,OR,pos,'gurobi2_old.png')





































