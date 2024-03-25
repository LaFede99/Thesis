from Package_scheduling import *
from Plotting import Plot_gantt
from Schedule_generators import *
import copy

class Order:
    def __init__(self, patient_file,pos=None):
        '''Order object, contains \n
        P: Dictionary of processing times before\n
           any reordering \n
        patient_file: Name of the file read \n
        N_patients: Amount of patients \n
        pos: Vector of current positioning\n
        OF: Objective function with pos order'''
        self.P=Read_patients(patient_file)
        self.patient_file=patient_file
        self.N_patients = int(len(self.P)/3)
        self.pos=pos
        self.methods=['swapping','sliding','group_sliding']
        if pos is None:
            self.OF=None
        else:
            sol=Optimal_plac_from_order(self.patient_file,self.pos,False,False)
            self.OF=sol.OF

    def Initialize_greedy( self ):
        '''Orders the patients according to the criterion of \n
        who is closest to the available space'''

        def whos_closest_to( p, available, space_available ):
            Where_is_min=None
            Current_min=1000
            for patient in available:
                My_quantity = abs( p[0,patient] - space_available )
                if My_quantity < Current_min :
                    Where_is_min=patient
                    Current_min=My_quantity
            return (Where_is_min,Current_min)

        def whos_closest_but_less( p, available, space_available ):
            Where_is_min=None
            Current_min=1000
            for patient in available:
                My_quantity = space_available - p[0,patient] 
                if My_quantity < Current_min and My_quantity >= 0:
                    Where_is_min=patient
                    Current_min=My_quantity
            return (Where_is_min,Current_min)

        def add_following_and_remove( pos, available, amount_scheduled, next ):
            pos[next]=amount_scheduled[0]
            amount_scheduled[0] += 1
            available.remove(next)
        
        def a_vs_b( p, pos, available , amount_scheduled, previous ):
            second_case_a , fit_value_a = whos_closest_to( p , available , p[1,previous]+p[2,previous] )
            second_case_b , fit_value_b = whos_closest_but_less( p, available , p[1,previous] )

            if fit_value_a < fit_value_b :
                next=second_case_a
                last_choice='a'
            else:
                next=second_case_b
                last_choice='b'

            add_following_and_remove(pos, available, amount_scheduled, next) 
            return next , last_choice

        def c_vs_d( p, pos, available , amount_scheduled, previous, previous_previous ):
            second_case_c , fit_value_c = whos_closest_to( p , available, p[1,previous]+p[2,previous] - p[2,previous_previous] )
            second_case_d , fit_value_d = whos_closest_but_less( p , available , p[1,previous] - p[2,previous_previous] )

            if fit_value_c < fit_value_d :
                next=second_case_c
                last_choice='c'
            else:
                next=second_case_d
                last_choice='d'

            add_following_and_remove( pos, available, amount_scheduled, next)  
            return next , last_choice

        NewPos = [None] * self.N_patients
        Available = [x for x in range(self.N_patients)]
        Amount_scheduled = [0]
        Last_choice = None

        #Start of the function
        ( Previous_previous , waste ) = whos_closest_to( self.P, Available, 0 )
        add_following_and_remove( NewPos, Available, Amount_scheduled, Previous_previous )

        Previous , Last_choice = a_vs_b( self.P, NewPos, Available, Amount_scheduled, Previous_previous )

        while Amount_scheduled[0] < self.N_patients:
            
            if Last_choice == 'a' or Last_choice == 'c' :
                Current , Last_choice = a_vs_b( self.P, NewPos, Available, Amount_scheduled, Previous )

            elif Last_choice=='b' or Last_choice=='d':
                Current , Last_choice = c_vs_d( self.P, NewPos, Available, Amount_scheduled, Previous, Previous_previous )

            else:
                print('Error sei un pollo')

            Previous_previous=Previous
            Previous=Current

        self.Update_pos(NewPos)

    def Pos_by_local_search(self, method= 'swapping', update='no', starting_from = None):
        '''Returns the pos array containing the best \n
        solution among the possible solution obtained\n 
        by local search according to the chosen criterion.
        Inputs are\n
        method: 'swapping' or 'sliding' or 'group_sliding'\n
        update: 'yes' or 'no' if you want to update \n
                 self position to the better one
        starting_from: can put a pos array here to \n
                       start from a specific ordering
        '''

        def Decide_I(method,n_patients):
            if method=='swapping':
                return range(n_patients)
            elif method=='sliding':
                return range(n_patients)
            elif method=='group_sliding':
                #Here you have to manually change the -1, -1 for groups of 2 patients
                #-2 for 3 patients, -3 for 4 patients.
                return range(n_patients-2)
        
        def Decide_J(method,i,n_patients):
            if method=='swapping':
                return range(i+1,n_patients)
            elif method=='sliding':
                return range(n_patients)
            elif method=='group_sliding':
                #Here you have to manually change the -1, -1 for groups of 2 patients
                #-2 for 3 patients, -3 for 4 patients.
                return range(n_patients-2)

        if method == 'swapping':
            How_to_swap=self.New_order_swapping_patients
        elif method == 'sliding':
            How_to_swap=self.New_order_sliding_patients
        elif method == 'group_sliding':
            How_to_swap=self.New_order_sliding_group_patients

        if starting_from is None:
            Current_best_OF=copy.deepcopy(self.OF)
            Current_best_pos=copy.deepcopy(self.pos)
            Initial_OF=self.OF
        else:
            Current_best_OF=self.Evaluate_OF(starting_from)
            Current_best_pos=copy.deepcopy(starting_from)
            Initial_OF=self.Evaluate_OF(starting_from)
        
        for i in Decide_I(method,self.N_patients):
            for j in Decide_J(method,i,self.N_patients):
                new_pos=How_to_swap(i,j,starting_from)
                new_OF=self.Evaluate_OF(new_pos)
                if new_OF<Current_best_OF:
                    Current_best_OF=new_OF
                    Current_best_pos=new_pos

        FinalPos=copy.deepcopy(Current_best_pos)

        if Current_best_OF == Initial_OF:
            NoProgress=1
        else:
            NoProgress=0

        if update == 'yes':
            self.Update_pos(FinalPos)

        return FinalPos , NoProgress
    
    def Pos_by_iterate_local_search(self, method='swapping', howmany=1,update='no',starting_from = None,noprint=0):
        '''Iterates the local search returning the pos.\n
        Inputs are\n
        method: 'swapping' or 'sliding' or 'group_sliding'\n
        howmany: amount of iteration to perform\n
        update: 'yes' or 'no' if you want to update \n
                 self position to the better one
        starting_from: can put a pos array here to \n
                       start from a specific ordering'''
        
        Iterations=0
        if starting_from is None:
            newpos=self.pos
        else:
            newpos=starting_from

        while Iterations < howmany :
            if Iterations%4 == 0 and Iterations > 0 and noprint==0:
                print(f'Currently running iteration {Iterations}')

            newpos , NoProg = self.Pos_by_local_search( method,'no',newpos)
            Iterations+=1

            if NoProg==1:
                if noprint==0:
                    print(f'Stopped at iteration {Iterations}, no progress')
                break
        
        if update == 'yes':
            self.Update_pos(newpos)

        return newpos

    def Pos_by_iterative_kernel(self,kernel=['group_sliding','swapping'],update='no'):
        newpos=self.pos
        for method in kernel:
            newpos=self.Pos_by_iterate_local_search(method,10,update,newpos,1)
        return newpos

    def Kernel_of_best_next_methods(self,how_deep=2):
        Ms=self.methods
        best_OF=self.OF
        final_kernel=[]
        is_progress=0
        if how_deep==2:
            for m1 in Ms:
                for m2 in Ms:
                    if m1 != m2 :
                        new_OF=self.Evaluate_OF(self.Pos_by_iterative_kernel([m1,m2],'no'))
                        if new_OF<best_OF:
                            is_progress=1
                            best_OF=new_OF
                            final_kernel=[m1,m2]
        elif how_deep==3:
            for m1 in Ms:
                for m2 in Ms:
                    for m3 in Ms:
                        if m1 != m2 and m2 != m3 :
                            new_OF=self.Evaluate_OF(self.Pos_by_iterative_kernel([m1,m2,m3],'no'))
                            if new_OF<best_OF:
                                is_progress=1
                                best_OF=new_OF
                                final_kernel=[m1,m2,m3]
        if is_progress:
            return final_kernel
        else:
            return 'No improvement found'
        
    def Search_improvement(self,depth=2):
        x=[]
        keep_track=[]
        while x != 'No improvement found':
            keep_track+=x
            print(f'{len(keep_track)} local searches have been performed...')
            self.Pos_by_iterative_kernel(x,'yes')
            x=self.Kernel_of_best_next_methods(depth)
        print(keep_track)

    def New_order_swapping_patients(self,pat1_pos,pat2_pos, starting_from=None):
        '''Return the pos obtained by swapping\n
        two patients in position.\n
        Inputs are:\n
        pat1_pos: position of first patient currently\n
        pat2_pos: position of second patient currently\n
        starting_from: can put a pos array here to \n
                       start from a specific ordering'''
        if starting_from is None:
            index_pos1=self.pos.index(pat1_pos)
            index_pos2=self.pos.index(pat2_pos)
            Newpos=copy.deepcopy(self.pos)
            Newpos[index_pos2]=self.pos[index_pos1]
            Newpos[index_pos1]=self.pos[index_pos2]
        else:
            index_pos1=starting_from.index(pat1_pos)
            index_pos2=starting_from.index(pat2_pos)
            Newpos=copy.deepcopy(starting_from)    
            Newpos[index_pos2]=starting_from[index_pos1]
            Newpos[index_pos1]=starting_from[index_pos2]   
        return Newpos
    
    def New_order_sliding_patients(self,who_slides,where_slides, starting_from=None):
        '''Return the pos obtained by putting a patient\n
        in a specific position and sliding all the other\n
        accordingly.\n
        Inputs are:\n
        who_slides: position of patient to slide around\n
        where_slide: position where you want the patient to go\n
        starting_from: can put a pos array here to \n
                       start from a specific ordering'''
        if starting_from is None:
            Newpos=copy.deepcopy(self.pos)
        else:
            Newpos=copy.deepcopy(starting_from)   

        if who_slides > where_slides:
            for i in range(len(Newpos)):
                if where_slides <= Newpos[i] < who_slides:
                    Newpos[i] += 1
                elif Newpos[i] == who_slides:
                    Newpos[i] = where_slides

        else:
            for i in range(len(Newpos)):
                if who_slides < Newpos[i] <= where_slides:
                    Newpos[i] -= 1
                elif Newpos[i] == who_slides:
                    Newpos[i] = where_slides

        return Newpos
    
    def New_order_sliding_group_patients(self,who_starts,where_slides,starting_from=None, how_many_he_brings=2):
        '''Return the pos obtained by putting a group of\n
        patients in a specific position and sliding all\n
        the other accordingly.\n
        Numbers have to be coherent with amount of patients\n
        Inputs are:\n
        who_start: position of first patient to slide\n
                   of the group\n
        where_slide: position where you want the first patient\n
                     to end up\n
        starting_from: can put a pos array here to \n
                       start from a specific ordering\n
        how_many_...: number of patients (OTHER THAN FIRST)\n
                      to move together with him\n
        !!Default value for how many is 2, to move 3 patients!!'''
        
        if starting_from is None:
            Newpos=copy.deepcopy(self.pos)
        else:
            Newpos=copy.deepcopy(starting_from)   

        if how_many_he_brings > self.N_patients - who_starts - 1 :
            #print('Error, too many patients to bring along')
            return Newpos
        
        if where_slides > self.N_patients - how_many_he_brings - 1 :
            #print('Error, cant move patient that much forward')
            return Newpos

        if who_starts >= where_slides:
            for i in range(len(Newpos)):
                if where_slides <= Newpos[i] < who_starts:
                    Newpos[i]+= how_many_he_brings+1                    
                elif who_starts <= Newpos[i] <= who_starts + how_many_he_brings:
                    Newpos[i] += -who_starts +where_slides

        else:
            for i in range(len(Newpos)):
                if who_starts <= Newpos[i] <= who_starts + how_many_he_brings:
                    Newpos[i] += where_slides - who_starts
                elif who_starts + how_many_he_brings < Newpos[i] <= how_many_he_brings + where_slides:
                    Newpos[i] += -how_many_he_brings - 1

        return Newpos

    def Update_pos(self,NewPos):
        '''Updates current pos and OF\n
        of the Order object with Newpos.'''
        self.pos=NewPos
        self.OF=self.Evaluate_OF(self.pos)

    def Evaluate_OF(self,pos):
        '''Returns the OF of position pos \n
        applied to patients set in this Order\n
        object.'''
        sol=Optimal_plac_from_order(self.patient_file,pos,False,False)
        return sol.OF

    def PrintIt(self):
        '''Prints position and OF of \n
        Order object.'''
        print('-'*4*self.N_patients)
        print(self.pos)
        print(self.OF)

    def Print_gandtt(self,gandtt_name):
        '''Creates the gandtt figure associated\n
        to current Order object, calling it -gandtt_name.-'''
        sol=Optimal_plac_from_order(self.patient_file,self.pos,False,False)
        temp_P=Impose_schedule_to_case1(self.P,self.pos)
        Plot_gantt(sol.C,temp_P,sol.OR,self.pos,gandtt_name)


# MyOrder=Order('Validation\TIME_N\TIME_11_4.txt')
# MyOrder.Initialize_greedy()
# MyOrder.PrintIt()
# MyOrder.Search_improvement(2)
# MyOrder.PrintIt()









    
















