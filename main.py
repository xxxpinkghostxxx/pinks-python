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



def force_calc(self_energy, target_energy, self_dna, target_dna):
    self_type = self_dna[1]
    self_toggle = self_dna[0]
    self_direction = self_dna[2]
    self_weight = self_dna[3]
    target_type = target_dna[1]
    target_toggle = target_dna[0]
    target_direction = target_dna[2]
    target_weight = target_dna[3]
    self_force = 0
    target_force = 0

    if self_type == 1: ## push
        self_force = (self_weight + target_weight * self_direction) * self_toggle
    elif self_type == 2: ## pull
        self_force = (self_weight - target_weight * self_direction) * self_toggle
    elif self_type == 3: ## gate
        self_force = (max(0,self_energy - (self_weight * target_weight)) * self_direction) * self_toggle
    elif self_type == 4: ## diff
        energy_delta = abs(self_energy - target_energy)
        self_force = (max(0,(energy_delta * (self_weight * target_weight - 1 )/ 255)) * self_direction) * self_toggle
    if target_type == 1:
        target_force = (target_weight + self_weight * target_direction) * target_toggle
    elif target_type == 2:
        target_force = (target_weight - self_weight * target_direction) * target_toggle
    elif target_type == 3:
        target_force = (max(0,target_energy - (target_weight * self_weight)) * target_direction) * target_toggle
    elif target_type == 4:
        energy_delta = abs(target_energy - self_energy)
        target_force = (max(0,(energy_delta * (target_weight * self_weight - 1 )/ 255)) * target_direction) * target_toggle
    return self_force, target_force






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
        self_up = grid[cords][3]
        self_front = grid[cords][5]
        if right in grid:
            right_node_energy = grid[right][0]
            right_node_left_dna = grid[right][2]
            self_force,right_force = force_calc(self_energy,right_node_energy,self_right,right_node_left_dna)
            if abs(self_force) > abs(right_force):
                self_energy -= self_force
                right_node_energy += self_force
                self_energy = max(0, min(255, self_energy))
                right_node_energy = max(0, min(255, right_node_energy))
                grid[cords][0] = self_energy
                grid[right][0] = right_node_energy
            else:
                self_energy += right_force
                right_node_energy -= right_force
                self_energy = max(0, min(255, self_energy))
                right_node_energy = max(0, min(255, right_node_energy))
                grid[cords][0] = self_energy
                grid[right][0] = right_node_energy
        if front in grid:
            front_node_energy = grid[front][0]
            front_node_back_dna = grid[front][6]
            self_force,front_force = force_calc(self_energy,front_node_energy,self_front,front_node_back_dna)
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
        if up in grid:
            up_node_energy = grid[up][0]
            up_node_down_dna = grid[up][4]
            self_force,up_force = force_calc(self_energy,up_node_energy,self_up,up_node_down_dna)
            if abs(self_force) > abs(up_force):
                self_energy -= self_force
                up_node_energy += self_force
                self_energy = max(0, min(255, self_energy))
                up_node_energy = max(0, min(255, up_node_energy))
                grid[cords][0] = self_energy
                grid[up][0] = up_node_energy
            else:
                self_energy += up_force
                up_node_energy -= up_force
                self_energy = max(0, min(255, self_energy))
                up_node_energy = max(0, min(255, up_node_energy))
                grid[cords][0] = self_energy
                grid[up][0] = up_node_energy
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
