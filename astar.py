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

    def can_move(self, movement):
        i = self.actual_pos.position[0] + movement[0]
        j = self.actual_pos.position[1] + movement[1]

        if i < 0 or j < 0 or i >= self.size or j >= self.size:
            return False
        return not self.grid[i][j].is_wall()

    def move(self, direction):
        return (self.actual_pos.position[0] + direction[0], self.actual_pos.position[1] + direction[1])

    def distance(self, position):
        return abs(position[0] - self.end_pos[0]) + abs(position[1] - self.end_pos[1])

    def have_finished(self):
        return self.actual_pos.position == self.end_pos

    def set_wall(self, position):
        self.grid[position[0]][position[1]] = Wall()

    def print(self):
        for row in self.grid:
            print ([i.g for i in row])

LEFT = (0, -1)
RIGHT = (0, 1)
UP = (1, 0)
DOWN = (-1, 0)
DIAG_NW = (1, -1)
DIAG_SW = (-1, -1)
DIAG_NE = (1, 1)
DIAG_SE = (-1, 1)
movements = (RIGHT, DOWN, LEFT, UP)

def astar2(maze):
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

        if maze.have_finished():
            path = []
            current = maze.actual_pos
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        children = []
        for move in movements:
            if maze.can_move(move):
                children.append(Node(maze.actual_pos, maze.move(move)))

        print("Node actual --> " + str(maze.actual_pos.position)+" Distancia: "+str(maze.actual_pos.f))
        for child in children:
            if child not in closed_list and not in_open_list(child, open_list):

                child.g = maze.actual_pos.g + 1
                child.h = maze.distance(child.position)
                child.f = child.g + child.h

                open_list.append(child)
                maze.grid[child.position[0]][child.position[1]] = child

def in_open_list(child, open_list):
    if child not in open_list:
        return False
    for open in open_list:
        if open == child and child.g < open.g:
            return False
    return True


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            #print(child.position)

            # Child is on the closed list
            for closed_child in closed_list:
                #print("for closed_child")
                if child == closed_child:
                    #print("chiled == closed_child")
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():
    maze = Grid(5, (0, 0), (4, 2))
    maze.set_wall((4, 1))
    maze.set_wall((3, 2))
    maze.set_wall((2, 3))
    maze.set_wall((1, 3))
    maze.set_wall((2, 1))
    print(astar2(maze))
    maze.print()

def main2():
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    path = astar(maze, start, end)
    print(path)

if __name__ == '__main__':
    main()

