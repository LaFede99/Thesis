from Package_scheduling import *
from Plotting import Plot_gantt
from collections import Counter
import copy


class Solution:
    '''Solution object is described by:\n
    C: dict(3xN_patients) completion times\n
    OR: dict(N_patients)  awakening placement\n
    C_OR: int available time in OR\n
    C_AOP: int available time in AOP\n
    Gap_width: int Gap available at end of schedule.'''
    def __init__(self,C,OR,C_OR,C_AOP,Gap_width):
        self.C=C
        self.OR=OR
        self.C_OR=C_OR
        self.C_AOP=C_AOP
        self.Gap_width=Gap_width
        self.OF=max(C_OR,C_AOP)
    
    def __str__(self):
        Display_schedule(self.C,self.OR)
        return ''              #f'{self.C}, {self.OR}, {self.C_OR}, {self.C_AOP}, {self.Gap_width}\n'
    
    def __repr__(self):
        return f'C_OR={self.C_OR}, C_AOP={self.C_AOP}, Gap={self.Gap_width}'
    
    def copy_from(self):
        '''Returns an indipendent copy of the solution'''
        copied_solution=copy.deepcopy(self)
        return copied_solution
    
    def get_last_positioning(self):
        '''Returns an int=1 if last patient's\n
        positioning is in OR, 0 if in AOP.'''
        positioning=self.OR[len(self.OR)-1]
        return positioning
    
    def add_patient(self,processing_new_patient, where_awakening):
        '''Processing_new_patient is a dict { 0:A , 1:S , 2:Aw }\n
        Where_awakening is int number OR_AW\n
        Returns an indipendent copy of the input solution with\n
        the additional patient inserted.'''

        old_schedule=Solution.copy_from(self)

        amount_already_scheduled=len(old_schedule.OR)

        P1={(i,j) : 0 for i in range(3) for j in range(amount_already_scheduled)}
        P2={(proced,amount_already_scheduled):processing_new_patient[proced] for proced in range(3)}
        support_P = { **P1,**P2 }

        support_OR={**old_schedule.OR,amount_already_scheduled:where_awakening}

        updated_schedule=Impose_placement(support_P,support_OR,old_schedule.C,old_schedule.C_OR,old_schedule.C_AOP,old_schedule.Gap_width)

        return updated_schedule
   
class Tree:
    '''Decision tree, initialized with a patient:\n
    dict { 0:A , 1:S , 2:Aw }.
    The tree attribute 'branches' is a dict whose keys are tuples containing\n
    the OR_AW int choices, and as values a list having the state\n
    of the node as element 0, being either 'Active' or 'Pruned',\n
    and as element 1 the solution associated to the key.\n
    branches= { OR_AW_tuple : [ state , solution ] }'''
    def __init__(self,first_patient):
        '''First_patient: dict { 0:A , 1:S , 2:Aw }'''
        self.branches={}
        self.branches[(0,)] = [ 'Active' , Impose_placement( {(i,0):first_patient[i] for i in range(3)},{0:0}) ]
        self.branches[(1,)] = [ 'Active' , Impose_placement( {(i,0):first_patient[i] for i in range(3)},{0:1}) ]
    
    def __str__(self):
        self.print_branches_at_levels()
        return '' 
    
    def get_depth(self):
        '''Returns how many patients are in the tree\n
        at the moment as an int'''
        depth=max([len(key) for key in self.branches.keys()])
        return depth
    
    def solution_from_node(self,key):
        '''Returns the solution associated to\n
        the node associated to the tuple key'''
        return self.branches[key][1]
    
    def status_from_node(self,key):
        '''Returns the status ofthe node\n
        associated to the tuple key'''
        return self.branches[key][0]

    def print_tree_keys_at_level(self,level=None,printamount=100):
        '''Prints the keys at a specific int level (if not specified\n
        selects the deepest level) unless the amount of Active leafs\n
        exceeds the int printamount'''

        if (level is None):
            level=self.get_depth()

        Active_keys=self.get_certain_keys_at_level(level,'Active')
        Amount_active_branches=len(Active_keys)

        if (Amount_active_branches<printamount) :
            print(f'\n--------------------------------\nActive branches at level {level}:\
               {Amount_active_branches}\n')
            for key in Active_keys:
                print(f'{key}---{self.solution_from_node(key).OF}')
        else:
            print(f'Too many active branches to print: {Amount_active_branches}')    
        print('')    

    def get_certain_keys_at_level(self,level,status):
        '''Returns the list containing the keys of all the \n
        leafs of a specific level havig a specific status.'''
        keys=[key for key in self.branches.keys() if (
            len(key)==level and self.status_from_node(key)==status)]
        return keys
    
    def get_OR_AW_keys_at_level(self,level,where_AW):
        '''Returns the list containing the keys of the\n
        leafs of a specific level with a specific placement\n
        for the alst patient.\n
        Where_Aw is an int 0 or 1'''
        keys=[key for key in self.branches.keys() if (
            len(key)==level and self.status_from_node(key)=='Active'
            and self.solution_from_node(key).get_last_positioning()==where_AW)]
        return keys
    
    def print_branches_at_levels(self):
        '''Prints informations about Pruned and Active \n
        leafs at each level'''
        depth=self.get_depth()
        print('-------------------------------------------------------------------')
        for lvl in range(1,depth+1):
            dead_leafs=len(self.get_certain_keys_at_level(lvl,'Pruned'))
            healthy_leafs=len(self.get_certain_keys_at_level(lvl,'Active'))

            print(f'level {lvl} has {dead_leafs} Pruned leafs and {healthy_leafs} Active leafs')
        print(f'\nTotal Active branches: {healthy_leafs}\nMaximum tree branches: {2**depth}')
        print('-------------------------------------------------------------------')

    def print_OF_information_at_level(self,level=None):
        '''Prints the ordered OF values and the frequency\n
        at which they occurr among the leafs of level selected.'''
        if level is None:
            level=self.get_depth()
        interested_keys=self.get_certain_keys_at_level(level,'Active')
        OF_values=[self.solution_from_node(key).OF for key in interested_keys]
        frequency=Counter(OF_values)
        sorted_freq=dict(sorted(frequency.items(), key=lambda item: item[0]))
        print('--------------------------------')
        for index, (key, value) in enumerate(sorted_freq.items()):
            if index >= 10:
                break
            print(f'OF= {key}, amount: {value}')
 
    def new_leaf(self,key,status,solution):
        '''Creates a new leaf from a solution setting\n
        the desired status.'''
        self.branches[key]=[status,solution]    

    def kill_leaf(self,key):
        '''Sets an existing leaf to 'Pruned'. '''
        self.branches[key][0]='Pruned'

    def extract_best_leaf(self,lvl=None,has_to_print=False):
        '''Return a solution object containing the best solution\n
        of the given level. Indipendent from the Tree. '''
        if lvl==None:
            lvl=self.get_depth()
        keys=self.get_certain_keys_at_level(lvl,'Active')
        best=keys[0]
        for key in keys:
            if self.solution_from_node(key).OF<self.solution_from_node(best).OF:
                best=key
        best_solution=self.solution_from_node(best)
        if has_to_print is not False:
            print(best_solution)
        return Solution.copy_from(best_solution)

def Impose_placement(P,OR,C=None,C_OR=None,C_AOP=None,Gap_width=None):
    '''Returns the solution object obtained by imposing\n
    processsing times and OR placements\n
    Inputs are:\n
    P[i,j], dict of processing times dim=3xn,\n
    OR[j],  dict of placements in OR/AOP dim=n\n
    The dict of placements can be shorter than P\n
    Optional inputs:\n
    C[i,j], dict of already started scheudule, dim 3xn\n
    C_OR, int with current available time in OR\n
    C_AOP, in with current available time in AOP\n
    Gap_width, in case there is a gap available'''

    if (C is None):
        C={}

    if (C_OR is None):
        C_OR=0
        C_AOP=0
        Gap_width=0

    num_patients=int(len(OR))
    assert num_patients>0, 'No placements to impose'
    num_already_scheduled=int(len(C)/3)
    
    #First patient if empty schedule
    if num_already_scheduled==0:
        C[0,0]=P[0,0]
        C[1,0]=C[0,0]+P[1,0]
        C[2,0]=C[1,0]+P[2,0]
        C_AOP=C[0,0]+(P[1,0]+P[2,0])*(1-OR[0])
        C_OR=C[1,0]+P[2,0]*OR[0]
        Gap_width=P[1,0]*(1-OR[0])
        num_already_scheduled+=1

    while num_already_scheduled<num_patients:
        cond1 = OR[num_already_scheduled-1]
        cond2 = P[0,num_already_scheduled] <= C_OR - C_AOP
        cond3 = P[0,num_already_scheduled] <= Gap_width
        cond4 = C_AOP - C_OR <= P[1,num_already_scheduled]
        cond5 = OR[num_already_scheduled]
        if ( cond1 and cond2 ):
            #print('Choice1')
            C[0,num_already_scheduled] = C_OR
            C[1,num_already_scheduled] = C[0,num_already_scheduled] + P[1,num_already_scheduled]
            C[2,num_already_scheduled] = C[1,num_already_scheduled] + P[2,num_already_scheduled]

            C_OR = C[1,num_already_scheduled] + P[2,num_already_scheduled] * ( OR[num_already_scheduled] )
            C_AOP = C[0,num_already_scheduled] + ( P[1,num_already_scheduled] + P[2,num_already_scheduled] ) * ( 1 - OR[num_already_scheduled] )
            Gap_width = P[1,num_already_scheduled] * (1-OR[num_already_scheduled])

        elif ( ( cond1 and not cond2 ) 
              or (not cond1 and cond3 and not cond4 and not cond5) 
              or (not cond1 and not cond3) ):
            #print('Choice2')
            C[0,num_already_scheduled]= C_AOP + P[0,num_already_scheduled]
            C[1,num_already_scheduled]= C[0,num_already_scheduled] + P[1,num_already_scheduled]
            C[2,num_already_scheduled]= C[1,num_already_scheduled] + P[2,num_already_scheduled]

            C_OR = C[1,num_already_scheduled] + P[2,num_already_scheduled] * ( OR[num_already_scheduled] )
            C_AOP = C[0,num_already_scheduled] + ( P[1,num_already_scheduled] + P[2,num_already_scheduled] ) * ( 1 - OR[num_already_scheduled] )
            Gap_width = P[1,num_already_scheduled] * (1-OR[num_already_scheduled])
            
        elif ( not cond1 and cond3 and not cond4 and cond5 ):
            #print('Choice3')
            C[0,num_already_scheduled]= C_OR
            C[1,num_already_scheduled]= C[0,num_already_scheduled] + P[1,num_already_scheduled]
            C[2,num_already_scheduled]= C[1,num_already_scheduled] + P[2,num_already_scheduled]

            C_OR = C[2,num_already_scheduled]
            Gap_width = 0

        elif ( not cond1 and cond3 and cond4 ):
            #print('Choice4')
            C[0,num_already_scheduled]= C_OR
            C[1,num_already_scheduled]= C[0,num_already_scheduled] + P[1,num_already_scheduled]
            C[2,num_already_scheduled]= C[1,num_already_scheduled] + P[2,num_already_scheduled]

            C_OR = C[1,num_already_scheduled] + P[2,num_already_scheduled] * ( OR[num_already_scheduled] )
            Gap_width = ( C[1,num_already_scheduled] - C_AOP ) * (1-OR[num_already_scheduled])
            C_AOP = C_AOP * ( OR[num_already_scheduled] ) + C[2,num_already_scheduled] * ( 1 - OR[num_already_scheduled] )

        else:
            print('Error in cases subdivision')

        num_already_scheduled+=1

    return Solution(C,OR,C_OR,C_AOP,Gap_width)
    
def Optimal_plac_from_order(filename,pos=None,has_to_print_tree=False, has_to_print_opt=False):
    '''Returns the Solution object containing \n
    the optimal placement for patients in filename\n
    orderded according to pos, if given.\n
    Inputs
    filename: name of the file containing proc. times\n
    pos: if given, position of patients\n
    has_to_print_tree: 'yes' or 'no' \n
    has_to_print_opt: 'yes' or 'no' if you want\n
                      to print the optimal solution. '''

    def which_AOP_gets_pruned(solution1,solution2):
        '''-1 if solution1 gets pruned, +1 if solution2\n
        gets pruned, 0 if none'''
        if (solution1.OF<=solution2.OF and 
            solution1.Gap_width>=solution2.Gap_width):
            return +1
        elif (solution1.OF>=solution2.OF and 
            solution1.Gap_width<=solution2.Gap_width):
            return -1
        else:
            return 0

    def which_OR_gets_pruned(solution1,solution2):
        '''-1 if solution1 gets pruned, +1 if solution2\n
        gets pruned, 0 if none'''
        if (solution1.OF<=solution2.OF and 
            solution1.C_AOP<=solution2.C_AOP):
            return +1
        elif (solution1.OF>=solution2.OF and 
            solution1.C_AOP>=solution2.C_AOP):
            return -1
        else:
            return 0

    def get_rid_of_AOP_leafs(mytree,leafs_keys):
        i=0
        while i < len(leafs_keys):
            current_leaf=leafs_keys[i]
            j=i+1
            while j < len(leafs_keys):
                other_leaf=leafs_keys[j]
                temp=which_AOP_gets_pruned(mytree.solution_from_node(current_leaf),mytree.solution_from_node(other_leaf))
                if temp!=0:
                    if temp==1:
                        mytree.kill_leaf(other_leaf)
                        leafs_keys.pop(j)
                    else:
                        mytree.kill_leaf(current_leaf)
                        leafs_keys.pop(i)
                        break
                else:
                    j+=1
            else:
                i+=1
        return leafs_keys

    def get_rid_of_OR_leafs(mytree,leafs_keys):
        i=0
        while i < len(leafs_keys):
            current_leaf=leafs_keys[i]
            j=i+1
            while j < len(leafs_keys):
                other_leaf=leafs_keys[j]
                temp=which_OR_gets_pruned(mytree.solution_from_node(current_leaf),mytree.solution_from_node(other_leaf))
                if temp!=0:
                    if temp==1:
                        mytree.kill_leaf(other_leaf)
                        leafs_keys.pop(j)
                    else:
                        mytree.kill_leaf(current_leaf)
                        leafs_keys.pop(i)
                        break
                else:
                    j+=1
            else:
                i+=1
        return leafs_keys

    P=Read_patients(filename)
    N_patients=int(len(P)/3)

    if pos is not None:
        P=Impose_schedule_to_case1(P,pos)

    Mytree=Tree({ 0:P[0,0] , 1:P[1,0] ,2:P[2,0] })

    for lvl in range(1,N_patients):
    
        AOP_keys=Mytree.get_OR_AW_keys_at_level(lvl,0)
        OR_keys=Mytree.get_OR_AW_keys_at_level(lvl,1)
    
        alive_AOP=get_rid_of_AOP_leafs(Mytree,AOP_keys)
        alive_OR=get_rid_of_OR_leafs(Mytree,OR_keys)
    
        for sub_leaf in alive_AOP + alive_OR:         
        
            sprout_AOP=Mytree.solution_from_node(sub_leaf).add_patient(Take_single_patient(P,lvl),0)
            sprout_OR=Mytree.solution_from_node(sub_leaf).add_patient(Take_single_patient(P,lvl),1)

            Mytree.new_leaf(tuple(sprout_AOP.OR.values()),'Active',sprout_AOP)
            Mytree.new_leaf(tuple(sprout_OR.OR.values()),'Active',sprout_OR)

    if has_to_print_tree is True:
        Mytree.print_branches_at_levels()
        Mytree.print_tree_keys_at_level()
        Mytree.print_OF_information_at_level()

    Optimal_solution=Mytree.extract_best_leaf(None, has_to_print_opt)

    return Optimal_solution

sol=Optimal_plac_from_order('Prova_finalissima.txt',None,True)

#Plot_gantt(sol.C,Read_patients('Prova_pazienti_facile.txt'),sol.OR,None,'Test_no_bueno.png')
