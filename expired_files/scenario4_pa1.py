from TumorDynamics import set_cellparam, main_GUICA
# KEYS = ['CCT', 'dtp' , 'u', 'dtu', 'Pa', 'Pps', 'pmax']

"""
Pa = 0.01 

u= 1,5,10 

Ps = 1, 10  """

set_cellparam('RTC', 'Pa', 0.01)
main_GUICA(maxtime=500, gridsize=200, outfile='scenario4_pa1.log', second_level_time_step=True)