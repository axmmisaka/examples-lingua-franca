### File for AI Pac-Man moves 
# Benjamin Asch

import sys
from random import randint
from math import sqrt

moves = {
            "LEFT": [30, 0], 
            "RIGHT": [-30, 0], 
            "DOWN": [0, 30], 
            "UP": [0, -30],
            }

# class Movefinders:
    #TODO: make so doesn't look in opposite direction of past move
    #TODO: add condition that tells whether or not should be reevaluated by pacman sprite
def closestpillpath(layout, ghosts, x, y, blocks):
    paths = []
    def pathfinder(layout, ghosts, x, y, blocks, temp = [], search_len = 8, add_anyways = False):
        oncurrpath = False
        #search_length = search_len
        if len(temp) < search_len:
            for name, change in possiblepacmoves(layout, ghosts, x, y).items():
                if len(temp) < 1 or not (change[0] * -1 == temp[len(temp) - 1][0] and change[1] * -1 == temp[len(temp) - 1][1]):
                    new_x = x + change[0]
                    new_y = y + change[1]
                    for block in blocks:
                        #print(abs(block.rect.left - x))
                       # x_condition = x >= block.rect.left - block.rect.width - 15 and x <= block.rect.left + block.rect.width + 15
                       # y_condition = y >= block.rect.top - block.rect.width - 15 and y <= block.rect.bottom + block.rect.width + 15
                        #print(x_condition, y_condition)
                        other_cond = x + 16 >= block.rect.left - block.rect.width and x + 16 <= block.rect.left + block.rect.width and y + 16 >= block.rect.top - block.rect.height and y + 16 <= block.rect.top + block.rect.height
                        if other_cond:
                            temp.append(change)
                            paths.append(temp)
                            oncurrpath = True
                            break
                    if oncurrpath:
                        oncurrpath = False
                        break
                    else:
                        pathfinder(layout, ghosts, new_x, new_y, blocks, [*temp, change], search_len, add_anyways)
        elif add_anyways:
            #print("added anyways")
            paths.append(temp)
    pathfinder(layout, ghosts, x, y, blocks)
    #print(paths, " is paths")
    #print("this is paths")
    if len(paths) > 0:
        smallest = []
        for path in paths:
            if len(path) == min(map(len, paths)):
                smallest.append(path)
        return smallest[randint(0, len(smallest) - 1)]
    else:
        # minimum = sys.maxsize
        # move = None
        # for name, change in possiblepacmoves(layout, ghosts, x, y).items():
        #     if avg_block_dist(blocks, x + change[0], y + change[1]) < minimum:
        #         move = [change]
        #         minimum = avg_block_dist(blocks, x + change[0], y + change[1])
        #         print("move is ", move)
        #         print("minimum is ", minimum)
        pathfinder(layout, ghosts, x, y, blocks, [], 3, True)
        #print(paths)
        return paths[0]

    #TODO: makemore efficient by changing wall list to save by section
    # and only check nearby walls
def possiblepacmoves(layout, ghosts, x, y, cond=True, moves=moves):
        possible = {}
        add = True
        for name, change in moves.items():
            for wall in layout:
                #print(wall)
                wall_left = wall[0]
                wall_right = wall_left + wall[2]
                wall_top = wall[1]
                wall_bottom = wall_top + wall[3]
                new_x = x + change[0]
                new_y = y + change[1]
                #print(wall_top, wall_bottom, new_y)
                condition_x = (new_x + 16 > wall_left - 20 and new_x + 16 < wall_right + 20) 
                condition_y = (new_y + 16 > wall_top - 20 and new_y + 16 < wall_bottom + 20)
                #print(condition_x, condition_y)
                off_grid = new_x < 10 or new_x > 565 or new_y < 10 or new_y > 565
                if off_grid or (condition_x and condition_y):
                    add = False
                    break
            if cond:
                for ghost in ghosts:
                    if (x + change[0]) == ghost.rect.left and (y + change[1]) == ghost.rect.top:
                        add = False;
                        break

            if add:
                possible.update({name : change})
            else:
                add = True
        #print(possible, " is possible")
        return possible
#TODO: make more efficient by stopping once length of single path htis threshold
def closeghostdist(layout, ghosts, x, y, threshold):
    paths = []
    def ghostfinder(layout, ghosts, x, y, temp = []):
        oncurrpath = False
        if len(temp) <= threshold:
            for name, change in possiblepacmoves(layout, ghosts, x, y, False).items():
                if len(temp) < 1 or not (change[0] * -1 == temp[len(temp) - 1][0] and change[1] * -1 == temp[len(temp) - 1][1]):
                    new_x = x + change[0]
                    new_y = y + change[1]
                    for ghost in ghosts:
                        x_condition = x >= ghost.rect.left - 16 and x <= ghost.rect.left + 16
                        y_condition = y >= ghost.rect.top - 16 and y <= ghost.rect.bottom + 16
                        if x_condition and y_condition:
                            temp.append(change)
                            paths.append(temp)
                            oncurrpath = True
                            break
                    if oncurrpath:
                        oncurrpath = False
                        break
                    else:
                        ghostfinder(layout, ghosts, new_x, new_y, [*temp, change])
    ghostfinder(layout, ghosts, x, y)
    if len(paths) == 0:
        longest = []
        for i in range(threshold + 1):
            longest.append([0, 0])
        return longest
    return min(paths, key=len)
        
def closestghost(layout, ghosts, x, y, threshold, give_all = False):
    paths = []
    def ghostfinder(layout, ghosts, x, y, temp = []):
        oncurrpath = False
        if len(temp) <= threshold:
            for name, change in possiblepacmoves(layout, ghosts, x, y).items():
                if len(temp) < 1 or not (change[0] * -1 == temp[len(temp) - 1][0] and change[1] * -1 == temp[len(temp) - 1][1]):
                    new_x = x + change[0]
                    new_y = y + change[1]
                    for ghost in ghosts:
                        x_condition = x >= ghost.rect.left - 16 and x <= ghost.rect.left + 16
                        y_condition = y >= ghost.rect.top - 16 and y <= ghost.rect.bottom + 16
                        if x_condition and y_condition:
                            temp.append(change)
                            paths.append([len(temp), ghost.rect.left, ghost.rect.top])
                            oncurrpath = True
                            break
                    if oncurrpath:
                        oncurrpath = False
                        break
                    else:
                        ghostfinder(layout, ghosts, new_x, new_y, [*temp, change])
    ghostfinder(layout, ghosts, x, y)
    if not give_all:
        mini = [sys.maxsize, 0, 0]
        for item in paths:
            if item[0] < mini[0]:
                mini = item
        return mini
    return paths
#FIXME: does not work
def avoider(layout, ghosts, x, y, threshold):
    paths = []
    def avoidfinder(layout, ghosts, x, y, threshold, temp = []):
        #oncurrpath = False
        if len(temp) < threshold:
            for name, change in possiblepacmoves(layout, ghosts, x, y).items():
                if len(temp) < 1 or not (change[0] * -1 == temp[len(temp) - 1][0] and change[1] * -1 == temp[len(temp) - 1][1]):
                    new_x = x + change[0]
                    new_y = y + change[1]
                    avoidfinder(layout, ghosts, new_x, new_y, threshold, [*temp, change])
        else:
            paths.append(temp)
    avoidfinder(layout, ghosts, x, y, 3)
    print("avoider paths: ", paths)
    maximum = len(closeghostdist(layout, ghosts, x, y, 5))
    best = []
    for path in paths:
        pos_x = x
        pos_y = y
        for move in path:
            pos_x += move[0]
            pos_y += move[1]
        dist = len(closeghostdist(layout, ghosts, pos_x, pos_y, 5))
        if dist > maximum:
            maximum = dist
            best = path
    if len(best) == 0:
        return [[0, 0]]
    return best

def allghostavoid(layout, ghosts, x, y, threshold):
    paths = []
    def avoidfinder(layout, ghosts, x, y, threshold, temp = []):
        #oncurrpath = False
        if len(temp) < threshold:
            for name, change in possiblepacmoves(layout, ghosts, x, y).items():
                if len(temp) < 1 or not (change[0] * -1 == temp[len(temp) - 1][0] and change[1] * -1 == temp[len(temp) - 1][1]):
                    new_x = x + change[0]
                    new_y = y + change[1]
                    avoidfinder(layout, ghosts, new_x, new_y, threshold, [*temp, change])
        else:
            paths.append(temp)
    avoidfinder(layout, ghosts, x, y, 3)
    print("avoider paths: ", paths)
    ghosts_dists = closestghost(layout, ghosts, x, y, 4, True)
    minimum = avg_dist_funcher(ghosts_dists)
    best = []
    for path in paths:
        pos_x = x
        pos_y = y
        for move in path:
            pos_x += move[0]
            pos_y += move[1]
        dist = avg_dist_funcher(closestghost(layout, ghosts, pos_x, pos_y, 4, True))
        if dist < minimum:
            minimum = dist
            best = path
    if len(best) == 0:
        return [[0, 0]]
    return best


def euclid_avoider(layout, ghosts, x, y):
    closeghost = closestghost(layout, ghosts, x, y, 7)
    maximum_dist = euclid_dist(closeghost[1], closeghost[2], x, y)
    best = []
    for name, change in possiblepacmoves(layout, ghosts, x, y).items():
        new_x = x + change[0]
        new_y = y + change[1]
        new_dist = euclid_dist(closeghost[1], closeghost[2], new_x, new_y)
        if new_dist > maximum_dist:
            maximum_dist = new_dist
            best = [change]
    return best

def euclid_close_people(people, x, y):
    minimum = sys.maxsize
    closest = people[0]
    for person in people:
        if euclid_dist(person.rect.left, person.rect.top, x, y) < minimum:
            minimum = euclid_dist(person.rect.left, person.rect.top, x, y)
            closest = person
    return [person, minimum]

def euclid_dist(x1, y1, x2, y2):
    return sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

def avg_block_dist(blocks, x, y):
    num_blocks = len(blocks)
    total = 0
    for block in blocks:
        total += euclid_dist(block.rect.left, block.rect.top, x, y)
    return total / num_blocks

def dist_funch(x):
    if x == 0 or x == 1:
        return 3000 * (2-x)
    return (10/(x - 0.99)) - 1
    #return (2 ** (-x+8))

def mine_dist_funch(x):
    # if x < 60:
    #     return 300
    # elif x < 120:
    #     return 100
    # elif x < 210:
    #     return 30
    # return 0
    if x < 2:
        return 350
    return (20/(x - 2.0001)) - 1

def avg_dist_funcher(ghosts_dists):
    total = 0
    for ghost in ghosts_dists:
        total += dist_funch(ghost[0])
    return total

def avg_people_euclid_funcher(people, x, y):
    total = 0
    for person in people:
        total += mine_dist_funch(euclid_dist(person.rect.left, person.rect.top, x, y))
    return total/(len(people))

def peopleavoid(layout, people, x, y):
    # new_moves = {
    #         "LEFT": [30, 0], 
    #         "RIGHT": [-30, 0], 
    #         "DOWN": [0, 30], 
    #         "UP": [0, -30]
    #         # "DIAG0": [30, 30],
    #         # "DIAG1": [-30, 30],
    #         # "DIAG2": [30, -30],
    #         # "DIAG3": [-30, -30]
    #         }
    #ghosts_dists = closestghost(layout, ghosts, x, y, 7, True)
    minimum = avg_people_euclid_funcher(people, x, y)
    print("avoid min: ", minimum)
    best = [[0, 0]]
    for name, change in possiblepacmoves(layout, people, x, y).items():
        new_x = x + change[0]
        new_y = y + change[1]
        #ghost_dists = closestghost(layout, ghosts, new_x, new_y, 7, True)
        print("avoid min: ", minimum)
        if avg_people_euclid_funcher(people, new_x, new_y) < minimum:
            minimum = avg_people_euclid_funcher(people, new_x, new_y)
            best = [change]

    print("best is ", best)
    return best

def pplavoidcloseghost(layout, people, x, y):
    closeperson = euclid_close_people(people, x, y)
    minimum = euclid_dist(closeperson[0].rect.left, closeperson[0].rect.top, x, y)
    best = [[0, 0]]
    for name, change in possiblepacmoves(layout, people, x, y).items():
        new_x = x + change[0]
        new_y = y + change[1]
        if euclid_dist(closeperson[0].rect.left, closeperson[0].rect.top, new_x, new_y) > minimum:
            minimum = euclid_dist(closeperson[0].rect.left, closeperson[0].rect.top, new_x, new_y)
            best = [change]
    return best

def mod_a_star(layout, people, x, y, goal_x, goal_y, acceptable_dev = 180):
    paths = []
    accept_dist = euclid_dist(x, y, goal_x, goal_y) + acceptable_dev
    def pathfinder(layout, people, x, y, temp = [], search_len = 5, add_anyways = False):
        if len(temp) < search_len and euclid_dist(x, y, goal_x, goal_y) < accept_dist:
            for name, change in possiblepacmoves(layout, people, x, y).items():
                if len(temp) < 1 or not (change[0] * -1 == temp[len(temp) - 1][0] and change[1] * -1 == temp[len(temp) - 1][1]):
                    new_x = x + change[0]
                    new_y = y + change[1]
                    if new_x == goal_x and new_y == goal_y:
                        temp.append(change)
                        paths.append(temp)
                        break
                    else:
                        pathfinder(layout, people, new_x, new_y, [*temp, change], search_len, add_anyways)
        elif add_anyways:
            #print("added anyways")
            paths.append(temp)
    pathfinder(layout, people, x, y)
    #print(paths, " is paths")
    #print("this is paths")
    if len(paths) > 0:
        smallest = []
        for path in paths:
            if len(path) == min(map(len, paths)):
                smallest.append(path)
        return smallest[randint(0, len(smallest) - 1)]
    else:
        # minimum = sys.maxsize
        # move = None
        # for name, change in possiblepacmoves(layout, ghosts, x, y).items():
        #     if avg_block_dist(blocks, x + change[0], y + change[1]) < minimum:
        #         move = [change]
        #         minimum = avg_block_dist(blocks, x + change[0], y + change[1])
        #         print("move is ", move)
        #         print("minimum is ", minimum)
        pathfinder(layout, people, x, y, [], 3, True)
        #print(paths)
        return paths[randint(0, len(paths) - 1)]
