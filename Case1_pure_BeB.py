from Package_scheduling import *
from Plotting import Plot_gantt
from Schedule_generators import *

P=Read_patients('Prova_pazienti_irrealistica.txt')
N_patients=int(len(P)/3)


pos=None
#pos=[0, 12, 2, 7, 11, 9, 13, 5, 10, 14, 3, 8, 6, 4, 1]
#P=Impose_schedule_to_case1(P,pos)


Mytree=Tree({ 0:P[0,0] , 1:P[1,0] ,2:P[2,0] })

for lvl in range(1,N_patients):
    
    for sub_leaf in Mytree.get_certain_keys_at_level(lvl,'Active'):
        
        sprout0=Mytree.branches[sub_leaf][1].add_patient(Take_single_patient(P,lvl),0)
        sprout1=Mytree.branches[sub_leaf][1].add_patient(Take_single_patient(P,lvl),1)

        if (sprout0.OF<sprout1.OF and sprout0.Gap_width>=sprout1.Gap_width):
            Mytree.new_leaf(tuple(sprout0.OR.values()),'Active',sprout0)
            Mytree.new_leaf(tuple(sprout1.OR.values()),'Pruned',sprout1)
        elif (sprout0.OF>sprout1.OF and sprout0.Gap_width>=sprout1.Gap_width):
            Mytree.new_leaf(tuple(sprout0.OR.values()),'Pruned',sprout0)
            Mytree.new_leaf(tuple(sprout1.OR.values()),'Active',sprout1)
        else:
            Mytree.new_leaf(tuple(sprout0.OR.values()),'Active',sprout0)
            Mytree.new_leaf(tuple(sprout1.OR.values()),'Active',sprout1)


Mytree.print_branches_at_levels()
Mytree.print_OF_information_at_level()




        














