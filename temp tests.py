import scipy as sp
import numpy as np
import random
import cv2
import mss


width = int(input("width: "))
height = int(input("height: "))
depth = int(input("depth: "))

## builds a cube with 7 slots inside each 3 dimensional cube
grid = np.zeros((height, width, depth, 7))
node_count = int(input("node_count: "))
grid[:,:,0:node_count,0:] = 80



neighbors = np.stack([
    np.roll(grid, -1, axis=0),  ## down
    np.roll(grid, -1, axis=1),  ## left
    np.roll(grid, -1, axis=2)]  ## back
, axis=0)




## decoding dna
#self toggle
##self_right_toggle = self_right_dna // 128
##self_up_toggle = self_up_dna // 128
##self_forward_toggle = self_forward_dna // 128

#self action
##self_right_action = ((self_right_dna % 128) // 32) + 1
##self_up_action = ((self_up_dna % 128) // 32) + 1
##self_forward_action = ((self_forward_dna % 128) // 32) + 1

#self direction
##self_right_modality = 2 * ((self_right_dna % 32) // 16) - 1
##self_up_modality = 2 * ((self_up_dna % 32) // 16) - 1
##self_forward_modality = 2 * ((self_forward_dna % 32) // 16) - 1

#self weight
##self_right_weight = self_right_dna % 16 + 1
##self_up_weight = self_up_dna % 16 + 1
##self_forward_weight = self_forward_dna % 16 + 1

def force (self_dna:int,target_dna:int,self_energy:int,target_energy:int):
    self_toggle = self_dna // 128
    self_type = ((self_dna % 128) // 32) + 1
    self_direction = 2 * ((self_dna % 32) // 16) - 1
    self_weight = self_dna % 16 + 1
    target_toggle = target_dna // 128
    target_type = ((target_dna % 128) // 32) + 1
    target_direction = 2 * ((target_dna % 32) // 16) - 1
    target_weight = target_dna % 16 + 1
    self_force = np.zeros_like(self_energy, dtype=int)
    target_force = np.zeros_like(target_energy, dtype=int)
    energy_delta = np.abs(self_energy - target_energy)
    self_force = np.where(self_type == 1, (self_weight + target_weight * self_direction) * self_toggle, self_force)
    self_force = np.where(self_type == 2, (self_weight - target_weight * self_direction) * self_toggle, self_force)
    self_force = np.where(self_type == 3, (np.maximum(0,self_energy - (self_weight * target_weight)) * self_direction) * self_toggle, self_force)
    self_force = np.where(self_type == 4, (np.maximum(0,(energy_delta * (self_weight * target_weight - 1 )/ 255)) * self_direction) * self_toggle, self_force)
    target_force = np.where(target_type == 1, (target_weight + self_weight * target_direction) * target_toggle, target_force)
    target_force = np.where(target_type == 2, (target_weight - self_weight * target_direction) * target_toggle, target_force)
    target_force = np.where(target_type == 3, (np.maximum(0,target_energy - (self_weight * target_weight)) * target_direction * target_toggle),target_force)
    target_force = np.where(target_type == 4, ((np.maximum(0,(energy_delta * (target_weight * self_weight - 1 )/ 255)) * target_direction) * target_toggle), target_force)
    return self_force.astype(int), target_force.astype(int)

def step(grid, neighbors):
    neighbor_down = neighbors[0]
    neighbor_left = neighbors[1]
    neighbor_back = neighbors[2]

    ## energy assignments
    self_energy = grid[:, :, :, 0]
    neighbor_down_energy = neighbor_down[:, :, :, 0]
    neighbor_left_energy = neighbor_left[:, :, :, 0]
    neighbor_back_energy = neighbor_back[:, :, :, 0]

    ## self direction assignments
    self_right_dna = grid[:, :, :, 1]
    self_up_dna = grid[:, :, :, 3]
    self_forward_dna = grid[:, :, :, 5]

    ## neighbor direction assigments
    neighbor_down_dna = neighbor_down[:, :, :, 4]
    neighbor_left_dna = neighbor_left[:, :, :, 2]
    neighbor_back_dna = neighbor_back[:, :, :, 6]


    forward_calc = force(self_forward_dna,neighbor_back_dna,self_energy,neighbor_back_energy)
    up_calc = force(self_up_dna,neighbor_down_dna,self_energy,neighbor_down_energy)
    right_calc = force(self_right_dna,neighbor_left_dna,self_energy,neighbor_left_energy)

    winner_up      = np.where(np.abs(up_calc[0]) > np.abs(up_calc[1]),      up_calc[0],      -up_calc[1])
    winner_forward = np.where(np.abs(forward_calc[0]) > np.abs(forward_calc[1]), forward_calc[0], -forward_calc[1])
    winner_right   = np.where(np.abs(right_calc[0]) > np.abs(right_calc[1]),   right_calc[0],   -right_calc[1])

    winner_up[-1, :, :] = 0
    winner_forward[:, :, -1] = 0
    winner_right[:, -1, :] = 0

    delta = (-winner_up      + np.roll(winner_up, 1, axis=0)
             -winner_forward + np.roll(winner_forward, 1, axis=2)
             -winner_right   + np.roll(winner_right, 1, axis=1))

    grid[:, :, :, 0] = np.clip(self_energy + delta, 0, 255)


    dead_nodes = grid[:,:,:,0] <= 0
    grid[dead_nodes] = 0
    alive_nodes = grid[:,:,:,0] > 0
    average_energy = np.mean(grid[alive_nodes, 0])
    spawn_thresh = average_energy * 1.25
    spawn_cost = spawn_thresh // 1.8
    child_energy = spawn_cost // 2
    possible_parent = grid[:, :, :, 0] > spawn_thresh

    if np.any(possible_parent):
        dx, dy, dz = random.choice([
            (dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)
            if not (dx == 0 and dy == 0 and dz == 0)
        ])

        # 2. Shift parent locations to target child coordinates
        # Roll parent locations by (dx, dy, dz) to see where kids would land
        potential_child_mask = np.roll(possible_parent, shift=(dx, dy, dz), axis=(0, 1, 2))

        # Target Mask: Must be empty AND hit by a potential child
        empty_mask = grid[:, :, :, 0] == 0
        valid_spawn_mask = potential_child_mask & empty_mask

        # Source Parent Mask: Reverse-roll valid spawns to find the actual parents who succeeded
        successful_parent_mask = np.roll(valid_spawn_mask, shift=(-dx, -dy, -dz), axis=(0, 1, 2))

        # Prevent boundary wrapping artifact from np.roll on edges
        if dx == 1:
            valid_spawn_mask[0, :, :] = False
        elif dx == -1:
            valid_spawn_mask[-1, :, :] = False
        if dy == 1:
            valid_spawn_mask[:, 0, :] = False
        elif dy == -1:
            valid_spawn_mask[:, -1, :] = False
        if dz == 1:
            valid_spawn_mask[:, :, 0] = False
        elif dz == -1:
            valid_spawn_mask[:, :, -1] = False

        # Apply energy changes via masks simultaneously
        grid[successful_parent_mask, 0] -= spawn_cost
        grid[valid_spawn_mask, 0] = child_energy

        # DNA Mutation Vectorized across all valid new children
        # Gather parent DNA by rolling parent DNA into child slots
        parent_dna_grid = np.roll(grid[:, :, :, 1:], shift=(dx, dy, dz), axis=(0, 1, 2))

        # Calculate random variance for every cell in the grid
        variance = np.random.uniform(0.90, 1.10, size=grid[:, :, :, 1:].shape)
        mutated_dna = np.clip(parent_dna_grid * variance, 0, 255).astype(np.uint16)

        # Assign mutated DNA directly to child positions
        grid[valid_spawn_mask, 1:] = mutated_dna[valid_spawn_mask]
    else:
        pass

    neighbors = np.stack([
        np.roll(grid, -1, axis=0),  ## down
        np.roll(grid, -1, axis=1),  ## left
        np.roll(grid, -1, axis=2)]  ## back
        , axis=0)
    return grid, neighbors


capture = True
run = True
while run:
    if capture:
        with mss.mss() as sct:
            # 1. Capture and convert BGRA array
            screenshot = sct.grab(sct.monitors[1])
            screen_array = np.array(screenshot)
            greyscale = cv2.cvtColor(screen_array, cv2.COLOR_BGRA2GRAY)

            # 2. Resize and mask
            greyscale_resized = cv2.resize(greyscale, (width, height))
            alive_mask = grid[:, :, 0, 0] > 0
            grid[:, :, 0, 0] = np.where(
                alive_mask,
                np.maximum(grid[:, :, 0, 0], greyscale_resized),
                grid[:, :, 0, 0]
            )

    # 3. Advance the simulation!
    grid, neighbors = step(grid, neighbors)

    # 4. Cast the output layer to 8-bit unsigned integer for OpenCV
    out_layer = grid[:, :, depth - 1, 0].astype(np.uint8)

    cv2.imshow('out_layer', out_layer)

    # 5. Provide an exit key (press 'q' to quit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        run = False

cv2.destroyAllWindows()