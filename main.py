import math
import random

import numpy as np
from numpy._core import ndarray

energy = random.randint(0, 255)


def dna_construct(n):
    if not isinstance(n, int):
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
    self_energy = grid[cords][0]
    self_right = grid[cords][1]
    self_right_type = self_right[1]
    self_right_switch = self_right[0]
    self_right_direction = self_right[2]
    self_right_weight = self_right[3]
    self_left = grid[cords][2]
    self_left_type = self_left[1]
    self_left_switch = self_left[0]
    self_left_direction = self_left[2]
    self_left_weight = self_left[3]
    self_up = grid[cords][3]
    self_up_type = self_up[1]
    self_up_switch = self_up[0]
    self_up_direction = self_up[2]
    self_up_weight = self_up[3]
    self_down = grid[cords][4]
    self_down_type = self_down[1]
    self_down_switch = self_down[0]
    self_down_direction = self_down[2]
    self_down_weight = self_down[3]

    if up in grid:
        print(f'{cords} selected is here\n{up} up is here')
        up_node_energy = grid[up][0]
        up_node_down_dna = grid[up][4]
        up_node_down_type = up_node_down_dna[1]
        up_node_down_switch = up_node_down_dna[0]
        up_node_down_direction = up_node_down_dna[2]
        up_node_down_weight = up_node_down_dna[3]
        self_force = 0
        up_force = 0
        if self_up_type == 1:
            self_force = self_up_weight + up_node_down_weight * self_up_direction * self_up_switch
        elif self_up_type == 2:
            self_force = self_up_weight - up_node_down_weight * self_up_direction * self_up_switch
        elif self_up_type == 3:
            self_force = max(0,self_energy - (self_up_weight * up_node_down_weight)) * self_up_direction * self_up_switch
        elif self_up_type == 4:
            energy_delta = abs(self_energy - up_node_energy)
            self_force = (energy_delta + (self_up_weight * up_node_down_weight)) * self_up_direction * self_up_switch
        if up_node_down_type == 1:
            up_force = up_node_down_weight + self_up_weight * up_node_down_direction * up_node_down_switch
        elif up_node_down_type == 2:
            up_force = up_node_down_weight - self_up_weight * up_node_down_direction * up_node_down_switch
        elif up_node_down_type == 3:
            up_force = max(0, up_node_energy - (self_up_weight * up_node_down_weight)) * up_node_down_direction * up_node_down_switch
        elif up_node_down_type == 4:
            energy_delta = abs(self_energy - up_node_energy)
            up_force = (energy_delta + (up_node_down_weight * self_up_weight)) * up_node_down_direction * up_node_down_switch
        if abs(self_force) > abs(up_force):
            self_energy -= self_force
            up_node_energy += self_force
            self_energy= max(0, min(255, self_energy))
            up_node_energy = max(0, min(255, up_node_energy))
            grid[cords][0] = self_energy
            grid[up][0] = up_node_energy
            print(self_energy, up_node_energy, self_force)
        else:
            self_energy += up_force
            up_node_energy -= up_force
            self_energy = max(0, min(255, self_energy))
            up_node_energy = max(0, min(255, up_node_energy))
            grid[cords][0] = self_energy
            grid[up][0] = up_node_energy
            print(self_energy, up_node_energy, up_force)



    if right in grid:
        print(f'{cords} selected is here\n{right} right is here')
        right_node_energy = grid[right][0]
        right_node_left_dna = grid[right][2]
        right_node_left_type = right_node_left_dna[1]
        right_node_left_switch = right_node_left_dna[0]
        right_node_left_direction = right_node_left_dna[2]
        right_node_left_weight = right_node_left_dna[3]
        self_force = 0
        right_force = 0
        if self_right_type == 1:
            self_force = self_right_weight + right_node_left_weight * self_right_direction * self_right_switch
        elif self_right_type == 2:
            self_force = self_right_weight - right_node_left_weight * self_right_direction * self_right_switch
        elif self_right_type == 3:
            self_force = min(0,self_energy - (self_right_weight * right_node_left_weight)) * self_right_direction * self_right_switch
        elif self_right_type == 4:
            energy_delta = abs(self_energy - right_node_energy)
            self_force = (energy_delta + (self_right_weight * right_node_left_weight)) * self_right_direction * self_right_switch
        if right_node_left_type == 1:
            right_force = self_right_weight + right_node_left_weight * right_node_left_direction * right_node_left_switch
        elif right_node_left_type == 2:
            right_force = self_right_weight - right_node_left_weight * right_node_left_direction * right_node_left_switch
        elif right_node_left_type == 3:
            right_force = max(0, right_node_energy - (self_right_weight * right_node_left_weight)) * right_node_left_direction * right_node_left_switch
        elif right_node_left_type == 4:
            energy_delta = abs(self_energy - right_node_energy)
            right_force = (energy_delta + (self_right_weight * right_node_left_weight)) * right_node_left_direction * right_node_left_switch
        if abs(self_force) > abs(right_force):
            self_energy -= self_force
            right_node_energy += self_force
            self_energy= max(0, min(255, self_energy))
            right_node_energy = max(0, min(255, right_node_energy))
            grid[cords][0] = self_energy
            grid[right][0] = right_node_energy
            print(self_energy, right_node_energy, self_force)
        else:
            self_energy += right_force
            right_node_energy -= right_force
            self_energy = max(0, min(255, self_energy))
            right_node_energy = max(0, min(255, right_node_energy))
            grid[cords][0] = self_energy
            grid[right][0] = right_node_energy
            print(self_energy,'self energy', right_node_energy,'right node energy', right_force, 'right force')
    if self_energy == 0:
        print(f'{cords} selected is here and died')
        del grid[cords]