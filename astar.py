class Grid:
    VOID = 0
    WALL = -1

    def __init__(self, size, initial_pos, end_position):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.actual_pos = {initial_pos[0], initial_pos[1]}
        self.end_pos = (end_position[0], end_position[1])
        self.grid[initial_pos[0]][initial_pos[1]] = 1

    def can_move(self, direction):
        i = self.actual_pos[0] + direction[0]
        j = self.actual_pos[1] + direction[1]

        if i < 0 or j < 0 or i >= self.size or j >= self.size:
            return False
        if self.grid[i][j] == self.WALL:
            return False

        return True

    def move(self, direction):
        self.actual_pos[0] += direction[0]
        self.actual_pos[1] += direction[1]

    def distance(self, position):
        return abs(position[0] - self.end_pos[0]) + abs(position[1] - self.end_pos[1])

    def print(self):
        for row in self.grid:
            print (row)


x = Grid(10, (0, 0), (5, 2))
x.print()

