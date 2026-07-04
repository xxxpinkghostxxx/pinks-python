import random
energy = random.randint(0, 255)


def dna_construct(n):
    if not isinstance(n, int):
        return []
    if n < 0 or n > 255:
        return []
    toggle = n // 128
    action = ((n % 128) // 32) + 1
    modality = 2 * ((n % 32) // 16) - 1
    weight = n % 16 + 1
    return [toggle, action, modality, weight]



dna_registry = {}

for n in range(0, 256):
    dna_registry[n] = dna_construct(n)

grid = {}






## grid is a dict the keys are an integer cooridinate system



run = True

## first battle loop
while run is True:
    if (0,0,0) in grid:
        grid[(0,0,0)][0] += 5
        grid[(0,0,0)][0] = min(255, max(0, grid[(0,0,0)][0]))
    else:
        grid[(0,0,0)] = [255] + [dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)]]
    if (255,255,255) in grid:
        grid[(255,255,255)][0] += 1
        grid[(255,255,255)][0] = min(255, max(0,grid[(255,255,255)][0]))
    else:
        grid[(255,255,255)] = [1] + [dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)],dna_registry[random.randint(0,255)]]



    for cords in grid:
        x = cords[0]
        y = cords[1]
        z = cords[2]
        left = (x-1,y,z)
        right = (x+1,y,z)
        up = (x,y+1,z)
        down = (x,y-1,z)
        front = (x,y,z+1)
        back = (x,y,z-1)
        self_energy = grid[cords][0]
        self_right = grid[cords][1]
        self_right_type = self_right[1]
        self_right_switch = self_right[0]
        self_right_direction = self_right[2]
        self_right_weight = self_right[3]
        self_up = grid[cords][3]
        self_up_type = self_up[1]
        self_up_switch = self_up[0]
        self_up_direction = self_up[2]
        self_up_weight = self_up[3]
        self_front = grid[cords][5]
        self_front_type = self_front[1]
        self_front_switch = self_front[0]
        self_front_direction = self_front[2]
        self_front_weight = self_front[3]
        if up in grid:
##            print(f'{cords} selected is here\n{up} up is here')
            up_node_energy = grid[up][0]
            up_node_down_dna = grid[up][4]
            up_node_down_type = up_node_down_dna[1]
            up_node_down_switch = up_node_down_dna[0]
            up_node_down_direction = up_node_down_dna[2]
            up_node_down_weight = up_node_down_dna[3]
            self_force = 0
            up_force = 0
            if self_up_type == 1:
                self_force = (self_up_weight + up_node_down_weight * self_up_direction) * self_up_switch
            elif self_up_type == 2:
                self_force = (self_up_weight - up_node_down_weight * self_up_direction) * self_up_switch
            elif self_up_type == 3:
                self_force = (max(0,self_energy - (self_up_weight * up_node_down_weight))) * self_up_direction * self_up_switch
            elif self_up_type == 4:
                energy_delta = abs(self_energy - up_node_energy)
                self_force = ((energy_delta + (self_up_weight * up_node_down_weight))) * self_up_direction * self_up_switch
            if up_node_down_type == 1:
                up_force = (up_node_down_weight + self_up_weight * up_node_down_direction) * up_node_down_switch
            elif up_node_down_type == 2:
                up_force = (up_node_down_weight - self_up_weight * up_node_down_direction) * up_node_down_switch
            elif up_node_down_type == 3:
                up_force = (max(0, up_node_energy - (self_up_weight * up_node_down_weight)) * up_node_down_direction) * up_node_down_switch
            elif up_node_down_type == 4:
                energy_delta = abs(up_node_energy - self_energy)
                up_force = ((energy_delta + (up_node_down_weight * self_up_weight)) * up_node_down_direction) * up_node_down_switch
            if abs(self_force) > abs(up_force):
                self_energy -= self_force
                up_node_energy += self_force
                self_energy = max(0, min(255, self_energy))
                up_node_energy = max(0, min(255, up_node_energy))
                grid[cords][0] = self_energy
                grid[up][0] = up_node_energy
##                print(self_energy,'self force', up_node_energy,'up node energy', self_force,'self force')
            else:
                self_energy += up_force
                up_node_energy -= up_force
                self_energy = max(0, min(255, self_energy))
                up_node_energy = max(0, min(255, up_node_energy))
                grid[cords][0] = self_energy
                grid[up][0] = up_node_energy
##                print(self_energy,'self energy', up_node_energy,'up node energy', up_force,' up force')



        if right in grid:
##            print(f'{cords} selected is here\n{right} right is here')
            right_node_energy = grid[right][0]
            right_node_left_dna = grid[right][2]
            right_node_left_type = right_node_left_dna[1]
            right_node_left_switch = right_node_left_dna[0]
            right_node_left_direction = right_node_left_dna[2]
            right_node_left_weight = right_node_left_dna[3]
            self_force = 0
            right_force = 0
            if self_right_type == 1:
                self_force = (self_right_weight + right_node_left_weight * self_right_direction) * self_right_switch
            elif self_right_type == 2:
                self_force = (self_right_weight - right_node_left_weight * self_right_direction) * self_right_switch
            elif self_right_type == 3:
                self_force = (max(0,self_energy - (self_right_weight * right_node_left_weight)) * self_right_direction) * self_right_switch
            elif self_right_type == 4:
                energy_delta = abs(self_energy - right_node_energy)
                self_force = ((energy_delta + (self_right_weight * right_node_left_weight)) * self_right_direction) * self_right_switch
            if right_node_left_type == 1:
                right_force = (right_node_left_weight + self_right_weight * right_node_left_direction) * right_node_left_switch
            elif right_node_left_type == 2:
                right_force = (right_node_left_weight - self_right_weight * right_node_left_direction) * right_node_left_switch
            elif right_node_left_type == 3:
                right_force = (max(0, right_node_energy - (right_node_left_weight * self_right_weight))) * right_node_left_direction * right_node_left_switch
            elif right_node_left_type == 4:
                energy_delta = abs(right_node_energy - self_energy)
                right_force = ((energy_delta + (right_node_left_weight * self_right_weight)) * right_node_left_direction) * right_node_left_switch
            if abs(self_force) > abs(right_force):
                self_energy -= self_force
                right_node_energy += self_force
                self_energy= max(0, min(255, self_energy))
                right_node_energy = max(0, min(255, right_node_energy))
                grid[cords][0] = self_energy
                grid[right][0] = right_node_energy
##                print(self_energy,'self_energy',right_node_energy,'right node energy' , self_force, 'self force')
            else:
                self_energy += right_force
                right_node_energy -= right_force
                self_energy = max(0, min(255, self_energy))
                right_node_energy = max(0, min(255, right_node_energy))
                grid[cords][0] = self_energy
                grid[right][0] = right_node_energy
##                print(self_energy,'self energy', right_node_energy,'right node energy', right_force, 'right force')

        if front in grid:
            front_node_energy = grid[front][0]
            front_node_back_dna = grid[front][6]
            front_node_back_type = front_node_back_dna[1]
            front_node_back_switch = front_node_back_dna[0]
            front_node_back_direction = front_node_back_dna[2]
            front_node_back_weight = front_node_back_dna[3]
            self_force = 0
            front_force = 0
            if self_front_type == 1:
                self_force = (self_front_weight + front_node_back_weight * self_front_direction) * self_front_switch
            elif self_front_type == 2:
                self_force = (self_front_weight - front_node_back_weight * self_front_direction) * self_front_switch
            elif self_front_type == 3:
                self_force = (max(0,self_energy - (self_front_weight * front_node_back_weight)) * self_front_direction) * self_front_switch
            elif self_front_type == 4:
                energy_delta = abs(self_energy - front_node_energy)
                self_force = ((energy_delta + (self_front_weight * front_node_back_weight)) * self_front_direction) * self_front_switch
            if front_node_back_type == 1:
                front_force = (front_node_back_weight + self_front_weight * front_node_back_direction) * front_node_back_switch
            elif front_node_back_type == 2:
                front_force = (front_node_back_weight - self_front_weight * front_node_back_direction) * front_node_back_switch
            elif front_node_back_type == 3:
                front_force = (max(0, front_node_energy - (front_node_back_weight * self_front_weight)) * front_node_back_direction) * front_node_back_switch
            elif front_node_back_type == 4:
                energy_delta = abs(front_node_energy - self_energy)
                front_force = ((energy_delta + (front_node_back_weight * self_front_weight)) * front_node_back_direction) * front_node_back_switch
            if abs(self_force) > abs(front_force):
                self_energy -= self_force
                front_node_energy += self_force
                self_energy= max(0, min(255, self_energy))
                front_node_energy = max(0, min(255, front_node_energy))
                grid[cords][0] = self_energy
                grid[front][0] = front_node_energy
            else:
                self_energy += front_force
                front_node_energy -= front_force
                self_energy = max(0, min(255, self_energy))
                front_node_energy = max(0, min(255, front_node_energy))
                grid[cords][0] = self_energy
                grid[front][0] = front_node_energy
## heres the death mechanic since the energy in the node cords is 0 it just dies so bye bye

    for cords, dna in list(grid.items()):
        if dna[0] <= 0:
            grid.pop(cords)
    average_energy = 0
    for cords in grid:
        average_energy += grid[cords][0]
    average_energy /= len(grid)
    average_energy = int(average_energy)
    spawn_cost = average_energy / 1.8
    spawn_cost = int(spawn_cost)
    initial_energy = spawn_cost / 2
    initial_energy = int(initial_energy)
    if average_energy == 255:
        grid[(255,255,255)][0] = 2
    if average_energy * 1.25 > 255:
        print('oh god its off')

    spawning_directions = {(-1,0,0), (0,-1,0), (0,0,-1), (-1,-1,0), (0,-1,-1), (-1,-1,-1), (+1,0,0), (0,+1,0), (0,0,+1), (+1,+1,0), (0,+1,+1), (+1,+1,+1), (-1,+1,+1), (+1,-1,+1), (-1,+1,0), (+1,-1,0), (-1,0,-1), (-1,0,+1), (+1,0,-1), (+1,0,+1), (0,-1,+1), (0,+1,-1), (-1,-1,+1), (-1,+1,-1), (+1,-1,-1), (+1,+1,-1)}
    temp_grid = {}
    for cords in grid:
        if grid[cords][0] >= average_energy * 1.25:
            x = cords[0]
            y = cords[1]
            z = cords[2]
            for dx, dy, dz in spawning_directions:
                neighbors = (min(255, abs(x + dx)),min(255, abs(y + dy)),min(255, abs(z + dz)))
                if neighbors not in grid and neighbors not in temp_grid:
                    parent = grid[cords]
                    parent_energy = parent[0]
                    parent_dna = parent[1:]
                    spawned_dna = [initial_energy]
                    grid[cords][0] = grid[cords][0] - spawn_cost
                    for dna in parent_dna:
                        toggle = dna[0]
                        action = dna[1]
                        modality = dna[2]
                        weight = dna[3]
                        mod_bit = 1 if modality == 1 else 0
                        dna_int = (toggle * 128) + ((action - 1) * 32) + (mod_bit * 16) + (weight - 1)
                        dna_variance = round(dna_int * (1 + random.uniform(-.10, .10)))
                        dna_variance = int(dna_variance)
                        dna_variance = max(0, min(255, dna_variance))


                        spawned_dna.append(dna_construct(dna_variance))
                    temp_grid[neighbors] = spawned_dna
                    break

    grid.update(temp_grid)
    temp_grid.clear()
    print(len(grid))
    if len(grid) >= 256 * 256 * 256:
        run = False
print(grid)
print(len(grid))
print('this is the equilibrium point')
