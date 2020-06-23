import gui

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
    def __init__(self):
        Node.__init__(self)

    def is_wall(self):
        return True

class Grid:
    VOID = 0
    WALL = -1

    def __init__(self, size, initial_pos, end_position):
        self.size = size
        self.grid = [[Node()] * size for _ in range(size)]
        self.actual_pos = Node(None, [initial_pos[0], initial_pos[1]])
        self.end_pos = (end_position[0], end_position[1])
        self.observer = gui.Observer()

    def can_move_diagonals(self, movement):
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
        return (self.actual_pos.position[0] + direction[0], self.actual_pos.position[1] + direction[1])

    def distance(self, position):
        #return abs(position[0] - self.end_pos[0]) + abs(position[1] - self.end_pos[1])
        return max([abs(position[0] - self.end_pos[0]), abs(position[1] - self.end_pos[1])])
        #return ((position[0] - self.end_pos[0]) ** 2) + ((position[1] - self.end_pos[1]) ** 2)

    def have_finished(self):
        return self.actual_pos.position == self.end_pos

    def set_wall(self, position):
        self.grid[position[0]][position[1]] = Wall()

    def actual_observed(self):
        self.observer.paint_current(self.actual_pos.position[0], self.actual_pos.position[1])

    def visited_observed(self, i, j):
        self.observer.paint_seen(i, j)

    def paint_init(self, i, j):
        self.observer.paint_init(i, j)

    def paint_end(self, i, j):
        self.observer.paint_end(i, j)

    def shortest_path(self, i, j):
        self.observer.paint_shortest_path(i, j)

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
    start_node = maze.actual_pos

    open_list = []
    open_list.append(start_node)
    closed_list = []

    while open_list:
        import time
        time.sleep(0.01)
        current_index = 0
        maze.actual_pos = open_list[0]
        for index, item in enumerate(open_list):
            if item.f < maze.actual_pos.f:
                maze.actual_pos = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(maze.actual_pos)
        maze.actual_observed()

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
                maze.visited_observed(child.position[0], child.position[1])

def remove(open_list, open):
    arr = []
    for x in open_list:
        if open  != x:
            arr.append(x)
    return arr

def in_open_list(child, open_list):
    if child not in open_list:
        return False
    return True

def paint_shortest_path(maze, shortest_path):
    maze.paint_end(shortest_path[0][0], shortest_path[0][1])
    maze.paint_init(shortest_path[-1][0], shortest_path[-1][1])
    shortest_path = shortest_path[1:-1]
    for pos in shortest_path:
        maze.shortest_path(pos[0], pos[1])



def main(walls, initial, end):
    maze = Grid(gui.num_lines, initial, end[0])#REFEEEER
    set_walls(maze, walls)
    shortest_path = astar2(maze)
    paint_shortest_path(maze, shortest_path)

def set_walls(maze, walls):
    for wall in walls:
        maze.set_wall(wall)

