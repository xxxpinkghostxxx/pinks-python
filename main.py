import random
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





## grid is a dict the keys are a integer cooridinate system



run = True

## first battle loop
while run == True:
    if (0,0) in grid:
        grid[(0,0)][0] += 5
        grid[(0,0)][0] = min(255, max(0, grid[(0,0)][0]))
    else:
        grid[(0,0)] = [255] + [dna_registry[255],dna_registry[255],dna_registry[255],dna_registry[255]]
    if (255,255) in grid:
        grid[(255,255)][0] += 1
        grid[(255,255)][0] = min(255, max(0,grid[(255,255)][0]))
    else:
        grid[(255,255)] = [1] + [dna_registry[255],dna_registry[255],dna_registry[255],dna_registry[255]]

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
        self_up = grid[cords][3]
        self_up_type = self_up[1]
        self_up_switch = self_up[0]
        self_up_direction = self_up[2]
        self_up_weight = self_up[3]
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
                print(self_energy,'self force', up_node_energy,'up node energy', self_force,'self force')
            else:
                self_energy += up_force
                up_node_energy -= up_force
                self_energy = max(0, min(255, self_energy))
                up_node_energy = max(0, min(255, up_node_energy))
                grid[cords][0] = self_energy
                grid[up][0] = up_node_energy
                print(self_energy,'self energy', up_node_energy,'up node energy', up_force,' up force')



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
                self_force = max(0,self_energy - (self_right_weight * right_node_left_weight)) * self_right_direction * self_right_switch
            elif self_right_type == 4:
                energy_delta = abs(self_energy - right_node_energy)
                self_force = (energy_delta + (self_right_weight * right_node_left_weight)) * self_right_direction * self_right_switch
            if right_node_left_type == 1:
                right_force = right_node_left_weight + self_right_weight * right_node_left_direction * right_node_left_switch
            elif right_node_left_type == 2:
                right_force = right_node_left_weight - self_right_weight * right_node_left_direction * right_node_left_switch
            elif right_node_left_type == 3:
                right_force = max(0, right_node_energy - (right_node_left_weight * self_right_weight)) * right_node_left_direction * right_node_left_switch
            elif right_node_left_type == 4:
                energy_delta = abs(self_energy - right_node_energy)
                right_force = (energy_delta + (right_node_left_weight * self_right_weight)) * right_node_left_direction * right_node_left_switch
            if abs(self_force) > abs(right_force):
                self_energy -= self_force
                right_node_energy += self_force
                self_energy= max(0, min(255, self_energy))
                right_node_energy = max(0, min(255, right_node_energy))
                grid[cords][0] = self_energy
                grid[right][0] = right_node_energy
                print(self_energy,'self_energy',right_node_energy,'right node energy' , self_force, 'self force')
            else:
                self_energy += right_force
                right_node_energy -= right_force
                self_energy = max(0, min(255, self_energy))
                right_node_energy = max(0, min(255, right_node_energy))
                grid[cords][0] = self_energy
                grid[right][0] = right_node_energy
                print(self_energy,'self energy', right_node_energy,'right node energy', right_force, 'right force')

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

    spawning_directions = {(0,-1),(-1,0),(0,+1),(+1,0),(-1,-1),(+1,+1),(-1,+1),(+1,-1)}
    temp_grid = {}
    for cords in grid:
        if grid[cords][0] >= average_energy * 1.25:
            x = cords[0]
            y = cords[1]
            for dx, dy in spawning_directions:
                neighbors = (min(255, abs(x + dx)),min(255, abs(y + dy)))
                if neighbors not in grid:
                    parent = grid[cords]
                    parent_energy = parent[0]
                    parent_dna = parent[1:]
                    spawned_dna:list[any] = [initial_energy,]
                    grid[cords][0] = grid[cords][0] - spawn_cost
                    for dna in parent_dna:
                        toggle = dna[0]
                        action = dna[1]
                        modality = dna[2]
                        weight = dna[3]
                        mod_bit = 1 if modality == 1 else 0
                        dna_int = (toggle * 128) + ((action - 1) * 32) + (mod_bit * 16) + weight
                        dna_variance = round(dna_int * (1 + random.uniform(-.10, .10)))
                        dna_variance = int(dna_variance)
                        dna_variance = max(0, min(255, dna_variance))


                        spawned_dna.append(dna_construct(dna_variance))
                    temp_grid[neighbors] = spawned_dna
                    break

    grid.update(temp_grid)
    temp_grid.clear()
    if len(grid) == (255 * 255):
        run = False
print(grid)
print(len(grid))
print('this is the equilibrium point')
