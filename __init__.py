import gurobipy as gp
import os

def Read_patients(filename):
    '''Input is the name of the file to read, output \n
    a dictionary having keys (operation-1,patient-1) \n
    and values the processing times of said procedure'''
    
    dir = os.path.dirname(os.path.abspath(__file__))
    folder_name='data'
    path=os.path.join(dir,folder_name)
    filepath=os.path.join(path,filename)

    Patients_times={}
    
    with open(filepath,"r") as file:
        
        next(file)

        for line in file:
            if not line.strip():
                continue
            assert len(line.split()) == 4 and all(s.isdigit() for s in line.split()), "Line does not contain 4 integers separated by spaces"
            a, b, c, d = map( int , line.split())
            Patients_times[1-1,a-1] =  b  
            Patients_times[2-1,a-1] =  c  
            Patients_times[3-1,a-1] =  d  
    
    return Patients_times

def Take_single_patient(P,position):
    '''Extracts from a dictionary P containing processing\n
    times of various patients the dictionary of structure:\n
    {0:A,1:S,2:AW} of the patient in position '''
    single_P={0:P[0,position],1:P[1,position],
              2:P[2,position]}
    return single_P

def Empty_schedule(Petients_times):
    '''Input is the dictionary having the procedures \n
    times as values, output am empty dictionary of \n
    equal size with all zeros.'''
    
    B={}

    for i in range(int(len(Petients_times)/3)):
        B[1-1,i]=0
        B[2-1,i]=0
        B[3-1,i]=0
    
    return B

def Completion_from_begin(B,P):
    '''B is dictionary of beginnings, while P \n
    dictionary of processing times. \n
    Given begin times and processing times, returns \n
    completion times in a dictionary of the same structure.'''

    assert len(B)==len(P), 'Dictionaries of different dimensions'
    C={}
    for i in range(int(len(B)/3)):
        C[1-1,i]=B[1-1,i]+P[1-1,i]
        C[2-1,i]=B[2-1,i]+P[2-1,i]
        C[3-1,i]=B[3-1,i]+P[3-1,i]
    return C

def Extract_sequence(C):
    '''Input is gurobi-dictionary of completion times, \n
    output is an array having in position i the \n
    position of i-th patient in given schedule'''
    pos=[]
    J=range(int(len(C)/3))
    for j1 in J:
        count=0
        for j2 in J:
            if C[1,j1].X > C[1,j2].X :
                count=count+1
        pos.append(count)
    print()
    print(pos)
    return pos

def Extract_sequence_no_Gurobi(C):
    '''Input is dictionary of completion times, \n
    output is an array having in position i the \n
    position of i-th patient in given schedule'''
    pos=[]
    J=range(int(len(C)/3))
    for j1 in J:
        count=0
        for j2 in J:
            if C[1,j1] > C[1,j2] :
                count=count+1
        pos.append(count)
    print()
    print(pos)
    return pos

def Extract_sequence_alt(z):
    '''Input is NxN gurobi binary matrix representing \n
    whether patient i is j-th in order of the schedule \n.
    Returns the array having the position of i-th patient \n
    in the given schedule'''
    pos=[]
    J=range(int(len(z)**0.5))
    for j1 in J:
        for j2 in J:
            if int(z[j1,j2].X)==1:
                pos.append(j2)
                break
    print()
    print(pos)
    return pos

def Impose_schedule_to_case1(P_old,Ordering):
    '''Inputs are old processing times as dictionary and\n
    new ordering as a list.\n
    Returns the reordered dictionary of processing times'''
    
    L=int(len(P_old)/3)
    assert L==len(Ordering), 'Wrong dimensions for schedule to impose' 
    P_new={}
    for j in range(L):
        P_new[1-1,j]=P_old[1-1,Ordering.index(j)]
        P_new[2-1,j]=P_old[2-1,Ordering.index(j)]
        P_new[3-1,j]=P_old[3-1,Ordering.index(j)]
    return P_new

def Reorder_schedule(C_old,P_old,OR_old,Ordering):
    '''Inputs are old completion times as dictionary, old\n
    OR dictionary and new ordering as a list\n
    Returns the reordered dictionary of completion times'''
    
    L=int(len(C_old)/3)
    assert L==len(Ordering), 'Wrong dimensions for schedule to impose' 
    C_new={}
    P_new={}
    OR_new={}
    for j in range(L):
        OR_new[j]=OR_old[Ordering.index(j)]
        C_new[1-1,j]=C_old[1-1,Ordering.index(j)]
        C_new[2-1,j]=C_old[2-1,Ordering.index(j)]
        C_new[3-1,j]=C_old[3-1,Ordering.index(j)]
        P_new[1-1,j]=P_old[1-1,Ordering.index(j)]
        P_new[2-1,j]=P_old[2-1,Ordering.index(j)]
        P_new[3-1,j]=P_old[3-1,Ordering.index(j)]
    return C_new,P_new,OR_new

def Display_schedule(C,OR_AW,pos=None):
    '''Inputs are dictionary with completion times as values and\n
    dictionary of binary values representing OR awakening.\n
    Third optionary input is position of patients once reordered'''
    
    L=int(len(C)/3)

    if pos is None:
        pos=range(L)

    assert L==len(OR_AW), 'Wrong inputs, dimensions not matching'
    print('\n-------------------------------------------------\
------------------')
    print('The resulting schedule is organized as follows:\n')
  
    for i in range(L):
        print((f"{str(pos.index(i)).zfill(3)}:   C_A={str(C[1-1,i]).zfill(4)}m  C_S={str(C[2-1,i]).zfill(4)}m"
                f"  C_AW={str(C[3-1,i]).zfill(4)}m  OR_AW={OR_AW[i]}"))
    print(f'\nThe Objective function is: {max(C[3-1,j] for j in range(L))}')

    print('\n-------------------------------------------------\
------------------')

def Gurobi_to_values(C,OR):
    '''Input are Gurobi dictionaries, output are \n
    normal dictionaries of values'''
    C_new={}
    OR_new={}
    for operation in C.keys():
        i,j=operation
        C_new[operation]=int(C[operation].X)
        if i==0:
            OR_new[j]=int(OR[j].X)
    return C_new,OR_new


