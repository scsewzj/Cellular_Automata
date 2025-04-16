# Tumor Dynamics Global Cellular Automaton

Author: [@Zhouji WU](https://github.com/scsewzj), [@Priyasha PAUL](https://github.com/Priyasha14), [@Frank DELAPLACE](https://github.com/Franck-Delaplace)
GitHub Repository URL: [Cellular_Automata](https://github.com/scsewzj/Cellular_Automata)

## Local CA Engine Installation

Library of cellular automaton written in Python with examples including the game of life.
This library is used for my Master course at Paris-Saclay University, Evry.
Please feel free to use it for educational purposes or other.

<code>celllularautomata</code> is the name of the library. The other programs are examples for using the library.
See game-of-life for a tutorial to use the library. See game-of-life or forest-fire examples for a demo.

The simulation can be controlled using the GUI. To adjust the weight of each cell type, use the slider provided.  The GUI includes two buttons: NEW and RUN. Clicking NEW generates a new initial state for the CA and opens a window where you can modify the cells graphically using a region selector. Clicking RUN starts the simulation.

Clicking NEW generates a new initial state and opens a window where you can modify the cells graphically. The configuration of this window will be the initial state of the CA as long as it remains open.

To display the simulation, simply click on RUN, and a new window will open. You can then save the simulation as a GIF. The waiting delay depends on the number of steps requested, as the simulation is pre-calculated.

To install the project, go in the directory of the CA library type: 
<ul>
<li> <code>pip install .</code>  </li>
<li> or,  <code> python -m pip install .</code></li>
</ul>

For more information, please reference repository of [Cellular Automata Python](https://github.com/Franck-Delaplace/Cellular-Automata-Python) developed by [@Frank Delaplace](https://github.com/Franck-Delaplace).

## Usage of Tumor Dynamic CA Engine

### Import Library

```python

from TumorDynamics import set_cellparam, main_GUICA

def your_global_fn(cells):
    pass

#set_cellparam('RTC', 'Pa', 0.3)
main_GUICA(maxtime=500, gridsize=500, second_level_time_step= True, outfile='./scenario1.log', global_fn = your_global_fn)
```

### Parameters
You can use set_cellparam() interface to modify parameter from default settings. Default parameters are as below.

```python
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

```

### Global Function
A decorator is implemented to handle pending data after local rules. It is optional and can be remained as default then only local_fn will be executed.


### Second Level of Time Step

In our tumor dynamic CA engine, basic time step is 1 hour. If you want to do long term simulation, for saving cost of handling graphical data, a optional secondary time step for visualization can be switched on. The secondary time steps = 24 hours (1 day). If you want to customize it, please revise the source code.

### Log File Format

```python
('Empty', [2499, 2498, 2497, 2495, 2493, 2491, 2489, 2486, 2487, 2484, 2480, 2480, 2477, 2477, 2480, 2488, 2492, 2497, 2499, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500])
('RTC', [1, 2, 3, 5, 7, 9, 11, 14, 13, 16, 20, 20, 23, 23, 20, 12, 8, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
('STC', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
('TSTC', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
```

