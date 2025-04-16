# ** CELLULAR AUTOMATA - Tumor Dynamics
# ** Author: Zhouji WU
# ** MASTER SOURCE
# ** Paris Saclay University
# ** 2025-04-04

# Reference: C. A. Valentim, J. A. Rabi, and S. A. David, 
# “Cellular-automaton model for tumor growth dynamics: Virtualization of different scenarios,” 
# Computers in Biology and Medicine, vol. 153, p. 106481, Feb. 2023, doi: 10.1016/j.compbiomed.2022.106481.

from random import random
from random import choices
import numpy as np
from copy import deepcopy
from cellularautomata import GuiCA


KEYS = ['CCT', 'dtp' , 'u', 'dtu', 'Pa', 'Pps', 'pmax']

RTC_INIT = {
 'CCT': 24,
 'dtp': 1,
 'u': 10/24,
 'dtu': 1.0,
 'Pa': 0,
 'Pps': 0,
 'pmax': 10}

STC_INIT = {
 'CCT': 24,
 'dtp': 1,
 'u': 10/24,
 'dtu': 1.0,
 'Pa': 0,
 'Pps': 0,
 'pmax': 10}

TSTC_INIT = {
 'CCT': 24,
 'dtp': 1,
 'u': 10/24,
 'dtu': 1.0,
 'Pa': 0,
 'Pps': 0.05,
 'pmax': 10}


"""
TC (RTC or (T)STC) = {
    'True_Stem': True/False,
    'CCT': Int,
    ## 'Pp' = CCT*dt/24, (0,1),
    'u' = float,
    ## 'pu' = u*dt, (0,1),
    'Pa' = float(0,1),
    'Ps' = float(0,1), # very low
    'pmax' = Int
    
}
"""

## Attributes: Pa, Pp, Pu, Pi, CCT, u, Ps, pmax
def Attr_dic2str(attr_dic):
    str_attr = ''
    for key in attr_dic:
        str_attr += str(attr_dic[key]) + ', '
    return str_attr[:-2]

def Attr_str2dic(attr_str):
    #keys = ['CCT', 'dtp' , 'u', 'dtu', 'Pa', 'Pps', 'pmax']
    
    attr_dic = {}
    attrs = attr_str.split(',')
    

    attr_dic['CCT'] = float(attrs[0].strip())
    attr_dic['dtp'] = float(attrs[1].strip())
    attr_dic['u'] = float(attrs[2].strip())
    attr_dic['dtu'] = float(attrs[3].strip())
    attr_dic['Pa'] = float(attrs[4].strip())
    attr_dic['Pps'] = float(attrs[5].strip())
    attr_dic['pmax'] = int(attrs[6].strip())
    return attr_dic

def Empty_flag2str(flag_list):
    str_flag = ''
    for i in range(len(flag_list)):
        single_flag = ''
        for j in range(len(flag_list[i])):
            single_flag += str(flag_list[i][j]) + ','
        str_flag += single_flag[:-1] + ';'
    return str_flag[:-1]

def Empty_str2flag(flag_str):
    flag_list = []
    flags = flag_str.split(';')
    for i in range(len(flags)):
        flag = flags[i].split(',')
        flag_list.append((int(flag[0]), flag[1], int(flag[2]), int(flag[3])))
    return flag_list
    

def behavior(cells, neighbors_indice_s):
    n = cells.shape[0]
    npar_cells = deepcopy(cells)
    cells = [[npar_cells[i,j] for j in range(n)] for i in range(n)]
    for posi in range(n):
        for posj in range(n):
            
            cell = cells[posi][posj]
            neighbor_indices = neighbors_indice_s[posi][posj]
            #print(neighbor_indices)
            #neighbors = [cells[i[0]][i[1]] for i in neighbor_indices]
            category, attr_str = cell
    
            #print(neighbors[1])
    
            if category == 'Empty':
                # do nothing
                cells[posi][posj] = (category, attr_str)
            else:
                attr = Attr_str2dic(attr_str)
                # Apoptosis
                if random() < attr['Pa']:
                    #print('Apoptosis')
                    #print(cells[posi][posj])
                    cells[posi][posj]=Apoptosis(category, attr_str)
                    #print(cells[posi][posj])
                else:
                    
                # Proliferation_flag
                    Pp = Prob_p(attr['CCT'], attr['dtp'])
                    if random() < Pp:
                        p_flag = Proliferation_flag(cells, neighbor_indices, posi, posj)
                    else:
                        p_flag = False
                    if p_flag:
                        cells[posi][posj] = (category, attr_str)
                    else:
                        # Migration_flag
                        Pu = Prob_u(attr['u'], attr['dtu'])
                        if random() < Pu:
                            u_flag = Migration_flag(cells, neighbor_indices, posi, posj)
                        else:
                            u_flag = False
                        if u_flag:
                            cells[posi][posj] = (category, attr_str)
                        else:
                        # Quiescence
                            cells[posi][posj] = Quiescence(category, attr_str)
    #print(cells)
    return np.array(cells)
                        

def Apoptosis(category, attr_str):
    if category == 'RTC' or category == 'STC':
        return ('Empty', None)
    else:
        return (category, attr_str)

        
def Proliferation_flag(cells, neighbor_indices, posi, posj):
    cell = cells[posi][posj]
    category, attr_str = cell
    attr = Attr_str2dic(attr_str)
    
    #neighbors = [cells[i[0]][i[1]] for i in neighbor_indices]
    
    neighbor_available = [i for i in neighbor_indices if cells[i[0]][i[1]][0] == 'Empty']
    if len(neighbor_available) == 0:
        return False
    else:
        neighbor_i, neighbor_j = choices(neighbor_available, k=1)[0]
        
        flag_truestem = False
        if category == 'RTC':
            priority = 2 
        elif category == 'STC':
            priority = 5
        else:
            priority = 6
            if random() < attr['Pps']:
                flag_truestem = True
        
        if flag_truestem:
            flag = (priority, 'proliferation_ts', posi, posj)
        else:
            flag = (priority, 'proliferation', posi, posj)
        
        if cells[neighbor_i][neighbor_j][1] in ['None', None]:
            cells[neighbor_i][neighbor_j] = ('Empty', Empty_flag2str([flag]))
        else:
            #print(cells[neighbor_i][neighbor_j][1])
            flaglist = Empty_str2flag(cells[neighbor_i][neighbor_j][1])
            flaglist.append(flag)
            cells[neighbor_i][neighbor_j] = ('Empty', Empty_flag2str(flaglist))
            #print(cells[neighbor_i][neighbor_j])
        return True
    

def Migration_flag(cells, neighbor_indices, posi, posj):
    cell = cells[posi][posj]
    category, attr_str = cell
    
    #neighbors = [cells[i[0]][i[1]] for i in neighbor_indices]
    
    neighbor_available = [i for i in neighbor_indices if cells[i[0]][i[1]][0] == 'Empty']
    if len(neighbor_available) == 0:
        return False
    else:
        neighbor_i, neighbor_j = choices(neighbor_available, k=1)[0]
        
        if category == 'RTC':
            priority = 1
        elif category == 'STC':
            priority = 3
        else:
            priority = 4
        
        flag = (priority, 'migration', posi, posj)
        
        if cells[neighbor_i][neighbor_j][1] in ['None', None]:
            cells[neighbor_i][neighbor_j] = ('Empty', Empty_flag2str([flag]))
        else:
            #print(cells[neighbor_i][neighbor_j][1])
            flaglist = Empty_str2flag(cells[neighbor_i][neighbor_j][1])
            flaglist.append(flag)
            cells[neighbor_i][neighbor_j] = ('Empty', Empty_flag2str(flaglist))
            #print(cells[neighbor_i][neighbor_j])
        return True

def Quiescence(category, attr_str):
    attr = Attr_str2dic(attr_str)
    attr['dtu'] = attr['dtu'] + 1
    attr['dtp'] = attr['dtp'] + 1
    return (category, Attr_dic2str(attr))

def Prob_p(CCT, dtp):
    return CCT*dtp/24
def Prob_u(u, dtu):
    return u*dtu

def global_conflict_resolve(cells):
    n = len(cells)
    for i in range(n):
        for j in range(n):
            if cells[i,j][0] == 'Empty':
                if cells[i,j][1] not in ['None', None]:
                    #print(cells[i,j])
                    flags = Empty_str2flag(cells[i,j][1])
                    """
                    flags = (priority, op_type, cell_posi, posj)
                    """
                    if len(flags) == 1:
                        flag = flags[0]
                    # execute the only one
                    if len(flags) > 1:
                    # only the highest priority will be executed
                        flags_array = np.array(flags)
                        np.random.shuffle(flags_array)
                        sorted_flags_array = flags_array[flags_array[:, 0].argsort(kind='stable')]
                    #flag_array.sort(key=lambda x: x[0])
                        flag = sorted_flags_array[0]
                        
                        for k in range(1, len(sorted_flags_array)):
                            cencel_flag = sorted_flags_array[k]
                            posi = int(cencel_flag[2])
                            posj = int(cencel_flag[3])
                            cells[posi][posj] = Quiescence(cells[posi][posj][0], cells[posi][posj][1])

                    # flag_exection(flag)
                    execute_flag(flag, cells, i, j)
    return cells


def execute_flag(flag, cells, empty_posi, empty_posj):
    
    op_type = flag[1]
    posi = int(flag[2])
    posj = int(flag[3])
    
    category, attr_str = cells[posi,posj]
    attr = Attr_str2dic(attr_str)
    
    if op_type == 'migration':
        # move the cell to the new position
        attr['dtu'] = 0
        attr['dtp'] += 1
        cells[empty_posi][empty_posj] = (category, Attr_dic2str(attr))
        cells[posi][posj] = ('Empty', None)
        
    elif op_type == 'proliferation':
        if cells[posi][posj][0] == 'RTC':
            attr['pmax'] -= 1
        
        if attr['pmax'] > 0:
            attr['dtp'] = 0
            new_attr = RTC_INIT.copy()
            new_attr['pmax'] = attr['pmax']
            new_attr['dtu'] = 0
            cells[empty_posi][empty_posj] = ('RTC', Attr_dic2str(new_attr))
            cells[posi][posj] = (category, Attr_dic2str(attr))
        else:
            cells[empty_posi][empty_posj] = ('Empty', None)
            cells[posi][posj] = ('Empty', None)
            
            
    elif op_type == 'proliferation_ts':
        cells[empty_posi][empty_posj] = ('STC', Attr_dic2str(STC_INIT))
        cells[posi][posj] = ('TSTC', Attr_dic2str(attr))
        
    else:
        raise ValueError('Unknown operation type: {}'.format(op_type))
    
    return cells

cellcolors = {
    ('Empty', None): 'white',
    ('RTC', Attr_dic2str(RTC_INIT)):'Yellow',
    ('STC', Attr_dic2str(STC_INIT)):'Orange',
    ('TSTC', Attr_dic2str(TSTC_INIT)): 'Red',
}


def set_cellparam(celltype, key, value):
    if key not in KEYS:
        raise ValueError('Invalid key: {}'.format(key))
    else:
        if celltype == 'RTC':
            RTC_INIT[key] = value
        elif celltype == 'STC':
            STC_INIT[key] = value
        elif celltype == 'TSTC':
            TSTC_INIT[key] = value
        else:
            raise ValueError('Invalid cell type: {}'.format(celltype))
        
        
def second_level_time_step_fn(cells, neighbors_indice_s):
    #print('second_level_time_step_fn')
    for i in range(24):
        #print('second_level_time_step_fn', i)
        cells = behavior(cells, neighbors_indice_s)
        cells = global_conflict_resolve(cells)
    return cells

def main_GUICA(maxtime=200, gridsize=100, outfile=None, second_level_time_step=False):
    if not second_level_time_step:
        GuiCA(behavior, cellcolors, extend=True, global_fn=global_conflict_resolve, duration=maxtime, gridsize=gridsize, outfile=outfile)
    else:
        GuiCA(second_level_time_step_fn, cellcolors, extend=True, duration=maxtime, gridsize=gridsize, outfile=outfile)