import gurobipy as gp
from Package_scheduling import *
from Plotting import Plot_gantt

P=Read_patients("Prova_.txt")
N_patients=int(len(P)/3)

# New model 
m=gp.Model('my_model')
#m.setParam('TimeLimit',15)

# Variables
I=range(3) ; J=range(N_patients)
Cycles=[(j,position) for j in J for position in J]
C={} ; OR={} ; z={}
M=3000

C=m.addVars(I,J,vtype=gp.GRB.INTEGER,name='C')
OR=m.addVars(J,vtype=gp.GRB.BINARY,name='OR')
z=m.addVars( Cycles ,vtype=gp.GRB.BINARY, name='z' )


# Objective function
m.setObjective(C[3-1,N_patients-1],gp.GRB.MINIMIZE)

# Constraints
m.addConstr( C[1-1,1-1] - sum(P[1-1,k]*z[k,1-1] for k in J) == 0, name='c000' )
m.addConstr( OR[N_patients-1] == 1 , name='c001' )

#HERE
# pos=[2, 4, 12, 0, 3, 10, 5, 8, 1, 14, 13, 6, 9, 11, 7]
# for j in J:
#     m.addConstr( z[j,pos[j]] == 1, 'newconst')

for j in J:
    m.addConstr(sum(z[j, j1] for j1 in J) == 1, "c10")
    m.addConstr(sum(z[j1, j] for j1 in J) == 1, "c11")
    m.addConstr( C[2-1,j] - sum(P[2-1,k]*z[k,j] for k in J) - C[1-1,j] == 0, name='c1' )
    m.addConstr( C[3-1,j] - sum(P[3-1,k]*z[k,j] for k in J) - C[2-1,j] == 0, name='c2' )
    

for j in range(N_patients-1):
    m.addConstr( C[1-1,j+1] - sum(P[1-1,k]*z[k,j+1] for k in J) - C[1-1,j]  >= 0, name='c3' )
    #m.addConstr( C[3-1,j+1] - sum(P[3-1,k]*z[k,j+1] for k in J) - C[3-1,j] + sum(P[3-1,k]*z[k,j] for k in J) >= 0, name='c5' )
    m.addConstr( C[2-1,j+1] - sum(P[2-1,k]*z[k,j+1] for k in J) - C[2-1,j] >= 0, name='c6' )
    m.addConstr( C[2-1,j+1] - sum(P[2-1,k]*z[k,j+1] for k in J) - C[2-1,j] - sum(P[3-1,k]*z[k,j] for k in J) + M*(1-OR[j]) >= 0, name='c6bis' ) 
    m.addConstr( C[3-1,j] - sum(P[3-1,k]*z[k,j] for k in J) - C[1-1,j+1] + M * (OR[j]) >= 0 , name='c8')

for j in range(N_patients-2):
    m.addConstr( C[1-1,j+2] - sum(P[1-1,k]*z[k,j+2] for k in J) - C[3-1,j] + M * OR[j] >= 0 , name='c7')

# Solving
m.optimize()

# Formatting and reordering
pos_alt=Extract_sequence_alt(z)

C_waste,P,OR_waste=Reorder_schedule(C,P,OR,pos_alt)

C,OR=Gurobi_to_values(C,OR)

# Printing
Display_schedule(C,OR,pos_alt)

Plot_gantt(C,P,OR,pos_alt,'Comb_plac_id.png')

