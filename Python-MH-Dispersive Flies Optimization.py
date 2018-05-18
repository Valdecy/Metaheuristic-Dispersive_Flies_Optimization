############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Metaheuristics
# Lesson: Dispersive Flies Optimization

# Citation: 
# PEREIRA, V. (2018). Project: Metaheuristic-Dispersive_Flies_Optimization, File: Python-MH-Dispersive Flies Optimization.py, GitHub repository: <https://github.com/Valdecy/Metaheuristic-Dispersive_Flies_Optimization>

############################################################################

# Required Libraries
import pandas as pd
import numpy  as np
import os

# Function: Initialize Variables
def initial_flies(swarm_size = 3, min_values = [-5,-5], max_values = [5,5]):
    position = pd.DataFrame(np.zeros((swarm_size, len(min_values))))
    position['Fitness'] = 0.0
    for i in range(0, swarm_size):
        for j in range(0, len(min_values)):
             r = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
             position.iloc[i,j] = min_values[j] + r*(max_values[j] - min_values[j])
    for i in range(0, swarm_size):
         position.iloc[i,-1] = target_function(position.iloc[i,0:position.shape[1]-1])
    return position

# Function: Best Fly
def best_fly(position):
    return position.iloc[position['Fitness'].idxmin(),:].copy(deep = True)

# Function: Update Position
def update_position(position, neighbour_best, swarm_best, min_values = [-5,-5], max_values = [5,5], fly = 0):
    for j in range(0, position.shape[1] - 1):
        r = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
        position.iloc[fly, j] = neighbour_best[j] + r*(swarm_best[j] - position.iloc[fly, j])
        if (position.iloc[fly, j] > max_values[j]):
           position.iloc[fly, j] = max_values[j]
        elif(position.iloc[fly, j] < min_values[j]):
           position.iloc[fly, j]  = min_values[j]
    position.iloc[fly, -1] = target_function(position.iloc[fly, 0:position.shape[1]-1])
    return position

# DFO Function
def dispersive_fly_optimization(swarm_size = 3, min_values = [-5,-5], max_values = [5,5], generations = 50, dt = 0.2):
    population = initial_flies(swarm_size = swarm_size, min_values = min_values, max_values = max_values)
    count = 0
    neighbour_best = best_fly(population)
    swarm_best = best_fly(population)
    while (count <= generations):
        print("Generation: ", count, " of ", generations)
        for i in range (0, swarm_size):
            #for j in range (0, len(min_values)):
            population = update_position(population, neighbour_best, swarm_best, min_values = min_values, max_values = max_values, fly = i)
            r = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            if (r < dt):
                for j in range(0, len(min_values)):
                    r = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
                    population.iloc[i,j] = min_values[j] + r*(max_values[j] - min_values[j])
                population.iloc[i,-1] = target_function(population.iloc[i,0:population.shape[1]-1])    
        neighbour_best = best_fly(population)
        if (swarm_best['Fitness'] > neighbour_best['Fitness']):
           swarm_best = neighbour_best.copy(deep = True)
        count = count + 1
    optimal_fly = population.iloc[population['Fitness'].idxmin(),:].copy(deep = True)
    return optimal_fly

######################## Part 1 - Usage ####################################

# Function to be Minimized. Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def target_function (variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

dispersive_fly_optimization(swarm_size = 25, min_values = [-5,-5], max_values = [5,5], generations = 50, dt = 0.2)
