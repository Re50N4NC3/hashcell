from PIL import Image
from datetime import datetime
import base64
import math
import os
import sys


def password_to_bytes(password, salt):
    pw_byte_list = []
    pw_salted = salt + password + salt

    for p in range(len(pw_salted)):
        pw_bytes =  ''.join(map(bin,bytearray(pw_salted[p],'utf8')))
        for l in range(2, len(pw_bytes)):
            pw_byte_list.append(int(pw_bytes[l]))
    
    return pw_byte_list


def assign_cell_values(password_byte_list):
    cells = [[0 for x in range(w)] for y in range(h)]
    cells_next = [[0 for x in range(w)] for y in range(h)]

    byte_counter = 0

    center_h = math.floor(h / 2)
    center_w = math.floor(w / 2)

    current_y = center_h
    current_x = center_w

    move_distance_max = 1
    move_distance_counter = 0
    move_distance_repeats = 0

    direction_counter = 0
    move_directions = [(1,0),(0,1),(-1,0),(0,-1)]

    for b in range(0, len(password_byte_list)):
        cells[current_x][current_y] = password_byte_list[b]
        cells_next[current_x][current_y] = password_byte_list[b]

        move_distance_counter += 1

        if move_distance_counter > move_distance_max:
            move_distance_counter = 0
            move_distance_repeats += 1
            direction_counter += 1
        
        if move_distance_repeats >= 1:
            move_distance_repeats = 0
            move_distance_max += 1
        
        if direction_counter > len(move_directions) - 1:
            direction_counter = 0

        current_x += move_directions[direction_counter][0]
        current_y += move_directions[direction_counter][1]

    return cells, cells_next


def cell_steps(steps_amount, cells, cells_next):
    for s in range(0, steps_amount):
        cells_step = grid_iteration(cells, cells_next)
        cells = cells_step
    return cells


def grid_iteration(cells, cells_next):
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            current_cell = cells[x][y]
            current_cell_neighbors = count_neighbors(cells, current_cell, x, y)

            if current_cell == 0:
                if current_cell_neighbors in birth_states:
                    cells_next[x][y] = 1
            if current_cell == 1:
                if current_cell_neighbors not in survive_states:
                    cells_next[x][y] = 0

    return cells_next
    

def count_neighbors(cells, center_cell, x_pos, y_pos):
    cell_neighbors = 0
    for xx in (-1, 0, 1):
        for yy in (-1, 0, 1):
            cell_neighbors += cells[x_pos + xx][y_pos + yy]
    
    cell_neighbors -= center_cell
    return cell_neighbors


def generate_image(image_cells, timestamp):
    img = Image.new('1', (w, h))
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = image_cells[i][j]

    image_name = 'hash_image_' + timestamp +'.png'
    img.save(image_name)

    if draw_image:
        img.show()


def convert_image_to_text(timestamp):
    with open('hash_image_' + timestamp +'.png', "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())

    if print_hash:
        print(converted_string)

    if save_to_bin:
        text_name = 'hash_' + str(datetime.now()) +'.bin'
        with open(text_name, "wb") as file:
            file.write(converted_string)

    if delete_image:
        os.remove('hash_image_' + timestamp +'.png')


def main():
    password_byte_list = password_to_bytes(pw, salt)
    cells_grid, cells_delta = assign_cell_values(password_byte_list)
    hashed_cells = cell_steps(steps, cells_grid, cells_delta)

    timestamp = str(datetime.now())
    generate_image(hashed_cells, timestamp)
    convert_image_to_text(timestamp)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments, provide at least phrase to hash.')
        print("Arguments schema: 0: phrase, 1: salt, 2: grid size, 3: steps, 4: image draw, 5: image deletion, 6: bin save, 7: hash printing, 8: picked rule")

    for i in range(len(sys.argv), 9):
        sys.argv.append(None)
    
    if sys.argv[2] is None: w, h = 256, 256
    else: w, h = sys.argv[2], sys.argv[2]

    if sys.argv[3] is None: steps = 256
    else: steps = sys.argv[3]

    # output options
    if sys.argv[4] is None: draw_image = True
    else: draw_image = sys.argv[4]
    if sys.argv[5] is None: delete_image = False
    else: delete_image = sys.argv[5]
    if sys.argv[6] is None: save_to_bin = True
    else: save_to_bin = sys.argv[6]
    if sys.argv[7] is None: print_hash = True
    else: print_hash = sys.argv[7]

    # automata rules
    rules_birth = [[1,3,5,7], [2,3,8], [2,3,5,6,7,8], [0,1,2,3,4,5,6,7,8], [1], [3,6,7]]
    rules_survival = [[1,3,5,7], [3,5,7], [3,7,8], [3], [1], [2,3]]

    if sys.argv[8] is None: picked_rules = 0
    else: picked_rules = sys.argv[8]

    if picked_rules > len(rules_birth):
        print('Rule out of range, picking rule number 0.')

    birth_states = rules_birth[picked_rules]
    survive_states = rules_survival[picked_rules]

    # password
    pw = sys.argv[0]

    if sys.argv[7] is None: salt = ""
    else: salt = sys.argv[1]
    
    main()
