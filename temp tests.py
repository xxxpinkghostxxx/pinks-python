import math
import random

import numpy as np
from numpy._core import ndarray

energy = random.randint(0, 255)





def dna_construct(n):
    if not isinstance(n,int):
        return "temp_dna failed to convert to int"
    if n < 0 or n > 255:
        return "temp_dna failed due to input variable range error"
    toggle = n // 128
    action = ((n % 128) // 32) + 1
    modality = 2 * ((n % 32) // 16) - 1
    weight = n % 16
    return [toggle, action, modality, weight]



dna_registry = {}

for n in range(0, 256):
    dna_registry[n] = dna_construct(n)

print(dna_construct(1))
print(dna_registry[1])
grid = {}
node_1 = [energy] + [dna_registry[255],dna_registry[255],dna_registry[255],dna_registry[255]]
node_2 = [energy] + [dna_registry[254],dna_registry[254],dna_registry[254],dna_registry[254]]
node_3 = [energy] + [dna_registry[253],dna_registry[253],dna_registry[253],dna_registry[253]]
node_4 = [energy] + [dna_registry[252],dna_registry[252],dna_registry[252],dna_registry[252]]
node_5 = [energy] + [dna_registry[251],dna_registry[251],dna_registry[251],dna_registry[251]]
node_6 = [energy] + [dna_registry[250],dna_registry[250],dna_registry[250],dna_registry[250]]
node_7 = [energy] + [dna_registry[249],dna_registry[249],dna_registry[249],dna_registry[249]]
node_8 = [energy] + [dna_registry[248],dna_registry[248],dna_registry[248],dna_registry[248]]
node_9 = [energy] + [dna_registry[247],dna_registry[247],dna_registry[247],dna_registry[247]]



my_dict = {'a': [1, 2], 'b': [3, 4], 'c': [2, 5]}
target_value = 2

# Iterate over a copy of the items to safely modify the dictionary while looping
for key, value in list(my_dict.items()):
    if target_value in value:
        popped_value = my_dict.pop(key)
        print(f"Popped {key}: {popped_value}")

print(my_dict)  # Output: {'b': [3, 4]}



grid is dict
grid[(0, 0)] = node_1
grid[(1, 0)] = node_2
grid[(0,1)] = node_3
grid[(1,1)] = node_4
grid[(0,2)] = node_5
grid[(1,2)] = node_6
grid[(2,0)] = node_7
grid[(2,1)] = node_8
grid[(2,2)] = node_9



if grid is None:
    print('no grid')
for cords in grid:
    x = cords[0]
    y = cords[1]
    left = (x-1,y)
    right = (x+1,y)
    up = (x,y+1)
    down = (x,y-1)
    print(f'\nselected: {cords} {grid[cords]}')
    if left in grid:
        left_face = grid[cords][1]
        left_dna = grid[left][1]
        print(f'left: {left} {grid[left]}')
    if right in grid:
        print (f'right: {right} {grid[right]}')
    if up in grid:
        print(f'up: {up} {grid[up]}')
    if down in grid:
        print(f'down: {down} {grid[down]}')
    
