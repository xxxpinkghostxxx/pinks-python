import numpy as np
import random
import PIL
from PIL import ImageGrab
from PIL import Image
import cv2
import mss

def dna_construct(n):
    if not isinstance(n, int): return
    if n < 0 or n > 255: return
    toggle = n // 128
    action = ((n % 128) // 32) + 1
    modality = 2 * ((n % 32) // 16) - 1
    weight = n % 16 + 1
    return [toggle, action, modality, weight]
dna_registry = {}
for n in range(0, 256):    dna_registry[n] = dna_construct(n)

## grid setup
width, height, depth = 1080, 1920, 10
grid = np.zeros((width, height, depth, 7), dtype=np.uint16)
sct = mss.MSS()
monitor = sct.monitors[1]

##  initial nodes
grid[:,:,0:-1:2,] = 1
grid[:,:,0:-1:3,] = 0
grid[:,:,0:-1:4,] = 15
run = True

self_right_force = np.zeros((width, height, depth), dtype=np.float32)
self_up_force = np.zeros((width, height, depth), dtype=np.float32)
self_forward_force = np.zeros((width, height, depth), dtype=np.float32)

neighbor_left_force = np.zeros((width, height, depth), dtype=np.float32)
neighbor_down_force = np.zeros((width, height, depth), dtype=np.float32)
neighbor_back_force = np.zeros((width, height, depth), dtype=np.float32)

while run:

    self_right_force.fill(0)
    self_up_force.fill(0)
    self_forward_force.fill(0)
    neighbor_left_force.fill(0)
    neighbor_down_force.fill(0)
    neighbor_back_force.fill(0)

    screen = sct.grab(monitor)
    screen_arr = np.array(Image.frombytes('RGB', screen.size, screen.rgb).convert('L'), dtype=np.uint8)

    current_energy_plane = grid[:, :, 0, 0]
    active_mask = current_energy_plane > 0
    updated_plane = np.maximum(current_energy_plane, screen_arr)
    current_energy_plane[active_mask] = updated_plane[active_mask]

    # ALL casts updated to signed int32 to prevent underflow
    self_energy = grid[:, :, :, 0].astype(np.int32)
    self_right = grid[:, :, :, 1].astype(np.int32)
    self_up = grid[:, :, :, 3].astype(np.int32)
    self_forward = grid[:, :, :, 5].astype(np.int32)
    alive_mask = self_energy > 0

    ##  decoding the dna
    self_right_toggle = self_right // 128
    self_up_toggle = self_up // 128
    self_forward_toggle = self_forward // 128

    self_right_action = ((self_right % 128) // 32) + 1
    self_up_action = ((self_up % 128) // 32) + 1
    self_forward_action = ((self_forward % 128) // 32) + 1

    self_right_modality = 2 * ((self_right % 32) // 16) - 1
    self_up_modality = 2 * ((self_up % 32) // 16) - 1
    self_forward_modality = 2 * ((self_forward % 32) // 16) - 1

    self_right_weight = self_right % 16 + 1
    self_up_weight = self_up % 16 + 1
    self_forward_weight = self_forward % 16 + 1

    ## neighbor shift grids
    neighbor_right_grid = np.roll(grid, -1, axis=0)
    neighbor_forward_grid = np.roll(grid, -1, axis=2)
    neighbor_up_grid = np.roll(grid, -1, axis=1)

    ## energy lookups (Signed)
    neighbor_right_energy = neighbor_right_grid[:, :, :, 0].astype(np.int32)
    neighbor_up_energy = neighbor_up_grid[:, :, :, 0].astype(np.int32)
    neighbor_forward_energy = neighbor_forward_grid[:, :, :, 0].astype(np.int32)

    ## mask maker
    neighbor_right_alive_mask = neighbor_right_energy > 0
    neighbor_up_alive_mask = neighbor_up_energy > 0
    neighbor_forward_alive_mask = neighbor_forward_energy > 0

    ## dna decoding (Fixed to int32)
    neighbor_left = neighbor_right_grid[:, :, :, 2].astype(np.int32)
    neighbor_down = neighbor_up_grid[:, :, :, 4].astype(np.int32)
    neighbor_back = neighbor_forward_grid[:, :, :, 6].astype(np.int32)

    neighbor_left_toggle = neighbor_left // 128
    neighbor_down_toggle = neighbor_down // 128
    neighbor_back_toggle = neighbor_back // 128

    neighbor_left_action = ((neighbor_left % 128) // 32) + 1
    neighbor_down_action = ((neighbor_down % 128) // 32) + 1
    neighbor_back_action = ((neighbor_back % 128) // 32) + 1

    neighbor_left_modality = 2 * ((neighbor_left % 32) // 16) - 1
    neighbor_down_modality = 2 * ((neighbor_down % 32) // 16) - 1
    neighbor_back_modality = 2 * ((neighbor_back % 32) // 16) - 1

    neighbor_left_weight = neighbor_left % 16 + 1
    neighbor_down_weight = neighbor_down % 16 + 1
    neighbor_back_weight = neighbor_back % 16 + 1

    self_right_force = np.zeros_like(self_energy, dtype=np.float32)
    self_up_force = np.zeros_like(self_energy, dtype=np.float32)
    self_forward_force = np.zeros_like(self_energy, dtype=np.float32)

    neighbor_left_force = np.zeros_like(neighbor_right_energy, dtype=np.float32)
    neighbor_down_force = np.zeros_like(neighbor_up_energy, dtype=np.float32)
    neighbor_back_force = np.zeros_like(neighbor_forward_energy, dtype=np.float32)

    ## right

    ##push
    mask = (self_right_action == 1) & alive_mask
    self_right_force[mask] = (
                (self_right_weight[mask] + neighbor_left_weight[mask] * self_right_modality[mask]) * self_right_toggle[
            mask])

    ##pull
    mask = (self_right_action == 2) & alive_mask
    self_right_force[mask] = (
                (self_right_weight[mask] - neighbor_left_weight[mask] * self_right_modality[mask]) * self_right_toggle[
            mask])

    ## gate
    mask = (self_right_action == 3) & alive_mask
    gate_calc = self_energy[mask] - (self_right_weight[mask] * neighbor_left_weight[mask])
    self_right_force[mask] = (np.clip(gate_calc, 0, None) * self_right_modality[mask]) * self_right_toggle[mask]

    ## diff
    mask = (self_right_action == 4) & alive_mask
    energy_delta = np.abs(self_energy[mask] - neighbor_right_energy[mask])
    diff_calc = energy_delta * (self_right_weight[mask] * neighbor_left_weight[mask] - 1) / 255
    self_right_force[mask] = (np.clip(diff_calc, 0, None) * self_right_modality[mask]) * self_right_toggle[mask]

    ## up
    ##push
    mask = (self_up_action == 1) & alive_mask
    self_up_force[mask] = (
                (self_up_weight[mask] + neighbor_down_weight[mask] * self_up_modality[mask]) * self_up_toggle[mask])

    ##pull
    mask = (self_up_action == 2) & alive_mask
    self_up_force[mask] = (
                (self_up_weight[mask] - neighbor_down_weight[mask] * self_up_modality[mask]) * self_up_toggle[mask])

    ##gate
    mask = (self_up_action == 3) & alive_mask
    gate_calc = self_energy[mask] - (self_up_weight[mask] * neighbor_down_weight[mask])
    self_up_force[mask] = (np.clip(gate_calc, 0, None) * self_up_modality[mask]) * self_up_toggle[mask]

    ##diff
    mask = (self_up_action == 4) & alive_mask
    energy_delta = np.abs(self_energy[mask] - neighbor_up_energy[mask])
    diff_calc = energy_delta * (self_up_weight[mask] * neighbor_down_weight[mask] - 1) / 255
    self_up_force[mask] = (np.clip(diff_calc, 0, None) * self_up_modality[mask]) * self_up_toggle[mask]

    ## forward
    ##push
    mask = (self_forward_action == 1) & alive_mask
    self_forward_force[mask] = ((self_forward_weight[mask] + neighbor_back_weight[mask]) * self_forward_modality[
        mask]) * self_forward_toggle[mask]

    ##pull
    mask = (self_forward_action == 2) & alive_mask
    self_forward_force[mask] = ((self_forward_weight[mask] - neighbor_back_weight[mask]) * self_forward_modality[
        mask]) * self_forward_toggle[mask]

    ## gate
    mask = (self_forward_action == 3) & alive_mask
    gate_calc = self_energy[mask] - (self_forward_weight[mask] * neighbor_back_weight[mask])
    self_forward_force[mask] = (np.clip(gate_calc, 0, None) * self_forward_modality[mask]) * self_forward_toggle[mask]

    ##diff
    mask = (self_forward_action == 4) & alive_mask
    energy_delta = np.abs(self_energy[mask] - neighbor_forward_energy[mask])
    diff_calc = energy_delta * (self_forward_weight[mask] * neighbor_back_weight[mask] - 1) / 255
    self_forward_force[mask] = (np.clip(diff_calc, 0, None) * self_forward_modality[mask]) * self_forward_toggle[mask]

    ## ==========================================
    ## NEIGHBOR FORCES (Fighting Back)
    ## ==========================================

    ## left (fighting against self_right)
    mask = (neighbor_left_action == 1) & neighbor_right_alive_mask  # push
    neighbor_left_force[mask] = ((neighbor_left_weight[mask] + self_right_weight[mask] * neighbor_left_modality[mask]) *
                                 neighbor_left_toggle[mask])

    mask = (neighbor_left_action == 2) & neighbor_right_alive_mask  # pull
    neighbor_left_force[mask] = ((neighbor_left_weight[mask] - self_right_weight[mask] * neighbor_left_modality[mask]) *
                                 neighbor_left_toggle[mask])

    mask = (neighbor_left_action == 3) & neighbor_right_alive_mask  # gate
    gate_calc = neighbor_right_energy[mask] - (neighbor_left_weight[mask] * self_right_weight[mask])
    neighbor_left_force[mask] = (np.clip(gate_calc, 0, None) * neighbor_left_modality[mask]) * neighbor_left_toggle[
        mask]

    mask = (neighbor_left_action == 4) & neighbor_right_alive_mask  # diff
    energy_delta = np.abs(neighbor_right_energy[mask] - self_energy[mask])
    diff_calc = energy_delta * (neighbor_left_weight[mask] * self_right_weight[mask] - 1) / 255
    neighbor_left_force[mask] = (np.clip(diff_calc, 0, None) * neighbor_left_modality[mask]) * neighbor_left_toggle[
        mask]

    ## down (fighting against self_up)
    mask = (neighbor_down_action == 1) & neighbor_up_alive_mask
    neighbor_down_force[mask] = ((neighbor_down_weight[mask] + self_up_weight[mask] * neighbor_down_modality[mask]) *
                                 neighbor_down_toggle[mask])

    mask = (neighbor_down_action == 2) & neighbor_up_alive_mask
    neighbor_down_force[mask] = ((neighbor_down_weight[mask] - self_up_weight[mask] * neighbor_down_modality[mask]) *
                                 neighbor_down_toggle[mask])

    mask = (neighbor_down_action == 3) & neighbor_up_alive_mask
    gate_calc = neighbor_up_energy[mask] - (neighbor_down_weight[mask] * self_up_weight[mask])
    neighbor_down_force[mask] = (np.clip(gate_calc, 0, None) * neighbor_down_modality[mask]) * neighbor_down_toggle[
        mask]

    mask = (neighbor_down_action == 4) & neighbor_up_alive_mask
    energy_delta = np.abs(neighbor_up_energy[mask] - self_energy[mask])
    diff_calc = energy_delta * (neighbor_down_weight[mask] * self_up_weight[mask] - 1) / 255
    neighbor_down_force[mask] = (np.clip(diff_calc, 0, None) * neighbor_down_modality[mask]) * neighbor_down_toggle[
        mask]

    ## back (fighting against self_forward)
    mask = (neighbor_back_action == 1) & neighbor_forward_alive_mask
    neighbor_back_force[mask] = (
                (neighbor_back_weight[mask] + self_forward_weight[mask] * neighbor_back_modality[mask]) *
                neighbor_back_toggle[mask])

    mask = (neighbor_back_action == 2) & neighbor_forward_alive_mask
    neighbor_back_force[mask] = (
                (neighbor_back_weight[mask] - self_forward_weight[mask] * neighbor_back_modality[mask]) *
                neighbor_back_toggle[mask])

    mask = (neighbor_back_action == 3) & neighbor_forward_alive_mask
    gate_calc = neighbor_forward_energy[mask] - (neighbor_back_weight[mask] * self_forward_weight[mask])
    neighbor_back_force[mask] = (np.clip(gate_calc, 0, None) * neighbor_back_modality[mask]) * neighbor_back_toggle[
        mask]

    mask = (neighbor_back_action == 4) & neighbor_forward_alive_mask
    energy_delta = np.abs(neighbor_forward_energy[mask] - self_energy[mask])
    diff_calc = energy_delta * (neighbor_back_weight[mask] * self_forward_weight[mask] - 1) / 255
    neighbor_back_force[mask] = (np.clip(diff_calc, 0, None) * neighbor_back_modality[mask]) * neighbor_back_toggle[
        mask]

    # X-Axis Edges (Index -1 is the absolute edge)
    self_right_force[-1, :, :] = 0
    neighbor_left_force[-1, :, :] = 0

    # Y-Axis Edges
    self_up_force[:, -1, :] = 0
    neighbor_down_force[:, -1, :] = 0

    # Z-Axis Edges
    self_forward_force[:, :, -1] = 0
    neighbor_back_force[:, :, -1] = 0

    ## ==========================================
    ## BATTLE RESOLUTION & ENERGY TRANSFER
    ## ==========================================

    # --- X-AXIS ---
    both_alive_x = (self_energy > 0) & (neighbor_right_energy > 0)
    winning_force_x = np.where(np.abs(self_right_force) > np.abs(neighbor_left_force), self_right_force,
                               -neighbor_left_force)
    # Block energy transfer unless BOTH cells are alive
    winning_force_x = np.where(both_alive_x, winning_force_x, 0.0)

    grid[:, :, :, 0] = np.clip(self_energy - winning_force_x + np.roll(winning_force_x, shift=1, axis=0), 0, 255)

    # --- Y-AXIS ---
    self_energy = grid[:, :, :, 0].astype(np.int32)
    both_alive_y = (self_energy > 0) & (neighbor_up_energy > 0)
    winning_force_y = np.where(np.abs(self_up_force) > np.abs(neighbor_down_force), self_up_force, -neighbor_down_force)
    # Block energy transfer unless BOTH cells are alive
    winning_force_y = np.where(both_alive_y, winning_force_y, 0.0)

    grid[:, :, :, 0] = np.clip(self_energy - winning_force_y + np.roll(winning_force_y, shift=1, axis=1), 0, 255)

    # --- Z-AXIS ---
    self_energy = grid[:, :, :, 0].astype(np.int32)
    both_alive_z = (self_energy > 0) & (neighbor_forward_energy > 0)
    winning_force_z = np.where(np.abs(self_forward_force) > np.abs(neighbor_back_force), self_forward_force,
                               -neighbor_back_force)
    # Block energy transfer unless BOTH cells are alive
    winning_force_z = np.where(both_alive_z, winning_force_z, 0.0)

    grid[:, :, :, 0] = np.clip(self_energy - winning_force_z + np.roll(winning_force_z, shift=1, axis=2), 0, 255)


    dead_mask = grid[:, :, :, 0] <= 0
    grid[dead_mask] = 0
    # ==========================================
    # VECTORIZED SPAWNING & REPRODUCTION
    # ==========================================
    active_mask = grid[:, :, :, 0] > 0

    if np.any(active_mask):
        avg_energy = np.mean(grid[active_mask, 0])
        spawn_threshold = avg_energy * 1.25
        spawn_cost = int(avg_energy / 1.8)
        child_energy = int(spawn_cost / 2)

        # 1. Parent Mask: Cells eligible to reproduce
        parent_mask = grid[:, :, :, 0] >= spawn_threshold

        # Pick a random offset direction for this tick (e.g., +1 on X, 0 on Y, 0 on Z)
        # You can cycle through directions or pick randomly per frame
        dx, dy, dz = random.choice([
            (dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)
            if not (dx == 0 and dy == 0 and dz == 0)
        ])

        # 2. Shift parent locations to target child coordinates
        # Roll parent locations by (dx, dy, dz) to see where kids would land
        potential_child_mask = np.roll(parent_mask, shift=(dx, dy, dz), axis=(0, 1, 2))

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


    # Video-style display output using OpenCV
    screen_out = grid[:,:,depth - 1, 0]
    img_out = np.uint8(screen_out)
    active_mask = grid[:, :, :, 0] > 0
    # Resize the tiny 32x32 view so you can actually see what's happening
    img_display = cv2.resize(img_out, (512, 512), interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Simulation Data', img_display)
    print(grid[active_mask])
    if cv2.waitKey(1) & 0xFF == ord('q'):
         run = False







cv2.destroyAllWindows()