import gurobipy as gp
from Package_scheduling import *
from Case2_greedy import *

def Gurobi_solve(filename):
    P=Read_patients(filename)
    N_patients=int(len(P)/3)

    # New model 
    m=gp.Model('my_model')
    m.setParam('TimeLimit',900)


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
    #t="{:.2f}".format(m.Runtime)
    OF=int(m.objVal)
    Lbound=m.objBound
    del m
    return OF,Lbound #(OF,t)

def Greedy_solve(filename):
    MyOrder=Order(filename)
    MyOrder.Initialize_greedy()
    #OF_greedy=MyOrder.OF
    # OF_swap=MyOrder.Evaluate_OF(MyOrder.Pos_by_iterate_local_search('swapping',30,'no',None,1))
    # OF_slide=MyOrder.Evaluate_OF(MyOrder.Pos_by_iterate_local_search('sliding',30,'no',None,1))
    # OF_group_slide=MyOrder.Evaluate_OF(MyOrder.Pos_by_iterate_local_search('group_sliding',30,'no',None,1))
    MyOrder.Search_improvement(3)
    OF_adaptive=MyOrder.OF
    return OF_adaptive#(OF_greedy,OF_swap,OF_slide,OF_group_slide,OF_adaptive)

for case in range(4):
    file = open(f"Package_scheduling\data\Validation\Final_groupof3_kern3__{case}.txt", 'a')
    file.writelines("! case - N_patients - Instance_number: \n")
    for N in range(11,21,2):
        for i in range(1,21):
            finame=f'Validation\OF_X_N\OF_{case}_{N}_{i}.txt'
            #(OFG,bound)=Gurobi_solve(finame)
            OF_mod=Greedy_solve(finame)   #(OF1,OF2,OF3,OF4,OF5)
            line=f'{case} - {N} - {i} : {OF_mod} \n'       #'{case} - {N} - {i} : {OFG} _ {bound} _ {OF1} _ {OF2} _ {OF3} _ {OF4} _ {OF5} \n'
            file.writelines(line)
        print(f'-------I AM AT N={N}------------\
----------------------------------\
----------------------------------\
----------------------------------\
----------------------------------')
    file.close()





