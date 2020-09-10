import run, tsp
import sys
from time import sleep

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def is_wall(self):
        return False

    def __eq__(self, other):
        return self.position == other.position

class Wall(Node):
    """Sub Class for the Walls"""
    def __init__(self):
        Node.__init__(self)

    def is_wall(self):
        return True

class Grid:

    def __init__(self, size, initial_pos, end_position):
        self.size = size
        self.grid = [[Node()] * size for _ in range(size)]
        self.inital_pos = initial_pos
        self.actual_pos = Node(None, (initial_pos[0], initial_pos[1]))
        self.end_pos = (end_position[0], end_position[1])
        self.observer = run.Observer(size)

    def can_move_diagonals(self, movement):
        """You'll be able to move diagonals if you can access there horitzontally or vertically"""
        i = self.actual_pos.position[0] + movement[0]
        j = self.actual_pos.position[1] + 0

        if i < 0 or j < 0 or i >= self.size or j >= self.size:
            first = False
        else:
            first =  not self.grid[i][j].is_wall()

        i = self.actual_pos.position[0] + 0
        j = self.actual_pos.position[1] + movement[1]

        if i < 0 or j < 0 or i >= self.size or j >= self.size:
            second = False
        else:
            second =  not self.grid[i][j].is_wall()

        return first or second


    def can_move(self, movement):

        i = self.actual_pos.position[0] + movement[0]
        j = self.actual_pos.position[1] + movement[1]

        if i < 0 or j < 0 or i >= self.size or j >= self.size:
            return False
        return not self.grid[i][j].is_wall()

    def move(self, direction):
        """Actual positions sets itself to new position"""
        return (self.actual_pos.position[0] + direction[0], self.actual_pos.position[1] + direction[1])

    def distance(self, position):
        """Different heuristics to final point"""
        #return abs(position[0] - self.end_pos[0]) + abs(position[1] - self.end_pos[1])
        return max([abs(position[0] - self.end_pos[0]), abs(position[1] - self.end_pos[1])])
        #return ((position[0] - self.end_pos[0]) ** 2) + ((position[1] - self.end_pos[1]) ** 2)

    def have_finished(self):
        return self.actual_pos.position == self.end_pos

    def set_wall(self, position):
        self.grid[position[0]][position[1]] = Wall()

    #Down bellow methods used for painting the grid in run.py

    def paint_actual_observed(self):
        if can_be_painted(self.actual_pos.position[0], self.actual_pos.position[1]):
            self.observer.paint_current(self.actual_pos.position[0], self.actual_pos.position[1])

    def paint_visited_observed(self, i, j):
        if can_be_painted(i, j):
            self.observer.paint_seen(i, j)

    def paint_init(self, i, j):
        self.observer.paint_init(i, j)

    def paint_end(self, i, j):
        self.observer.paint_end(i, j)

    def paint_shortest_path(self, i, j):
        self.observer.paint_shortest_path(i, j)

    def not_found(self):
        self.observer.not_found()

    def print(self):
        for row in self.grid:
            print (["--" if i.is_wall() else i.f for i in row])

LEFT = (0, -1)
RIGHT = (0, 1)
UP = (1, 0)
DOWN = (-1, 0)
DIAG_NW = (1, -1)
DIAG_SW = (-1, -1)
DIAG_NE = (1, 1)
DIAG_SE = (-1, 1)
movements = (RIGHT, DOWN, LEFT, UP, DIAG_SW, DIAG_SE, DIAG_NW, DIAG_NE)

def astar2(maze):
    """A* algorithm"""
    start_node = maze.actual_pos
    open_list = []
    open_list.append(start_node)
    closed_list = []

    while open_list:
        current_index = 0
        maze.actual_pos = open_list[0]
        for index, item in enumerate(open_list):
            if item.f < maze.actual_pos.f:
                maze.actual_pos = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(maze.actual_pos)
        maze.paint_actual_observed()

        if maze.have_finished():
            path = []
            current = maze.actual_pos
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path

        children = []
        for move in movements:
            if maze.can_move(move) and maze.can_move_diagonals(move):
                children.append(Node(maze.actual_pos, maze.move(move)))

        for child in children:
            if child not in closed_list:

                child.g = maze.actual_pos.g + 1
                child.h = maze.distance(child.position)
                child.f = child.g + child.h

                shall_continue = True
                for open in open_list:
                    if open == child and child.g < open.g:
                        open_list = remove(open_list, open)
                    if open == child and child.f >= open.f:
                        shall_continue = False
                        break

                if not shall_continue:
                    continue

                open_list.append(child)
                maze.grid[child.position[0]][child.position[1]] = child
                maze.paint_visited_observed(child.position[0], child.position[1])
    maze.not_found()
    return []

def remove(open_list, open):
    """removes from open_list, open"""
    arr = []
    for x in open_list:
        if open  != x:
            arr.append(x)
    return arr

def in_open_list(child, open_list):
    return not child not in open_list

def paint_shortest_path(maze, shortest_path):
    shortest_path = shortest_path[1:-1]
    for pos in shortest_path:
        maze.paint_shortest_path(pos[0], pos[1])
        sleep(0.01)

def can_be_painted(i, j):
    """Checks if painted cell is not a checkpoint"""
    return (i, j) not in allEnds

def main(walls, initial, end, size):
    global allEnds
    end = [initial] + end
    allEnds = end
    distance_matrix = [[sys.maxsize] * len(end) for _ in range (len(end))]
    dict_paths = {}
    maze = None
    for i in range(len(end)):
        for j in range(i+1, len(end)):
            distance, path, maze = astar(walls, end[i], end[j], size)
            if distance == 0:
                return
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
            dict_paths.update({(i, j): path})
            dict_paths.update({(j, i): path})

    find_shortest_path(maze, distance_matrix, dict_paths)

def find_shortest_path(maze, matrix, dict):
    shortest_path = tsp.tsp_algorithm(matrix)
    shortest_path.reverse()
    for i in range(len(shortest_path) - 1):
        paint_shortest_path(maze, dict[(shortest_path[i], shortest_path[i+1])])


def astar(walls, initial, end, size):
    maze = Grid(size, initial, end)
    set_walls(maze, walls)
    shortest_path = astar2(maze)
    return len(shortest_path), shortest_path, maze

def set_walls(maze, walls):
    for wall in walls:
        maze.set_wall(wall)

