import pygame
import astar
import time
import tkinter
from tkinter import messagebox

class Connection:
    def __init__(self):
        self.init = None
        self.walls = []
        self.end = []
        self.size = 40
        self.reference = [0, 0]

    def reset(self):
        self.init = None
        self.walls = []
        self.end = []

    def add_wall(self, wall):
        self.walls.append(self.__reference_cells(wall))

    def add_init(self, init):
        self.init = self.__reference_cells(init)

    def add_end(self, end):
        if end not in self.end:
            self.end.append(self.__reference_cells(end))

    def __reference_cells(self, coord):
         return (self.reference[0] + coord[0], self.reference[1] + coord[1])

    def __remove(self, array, coordinate):
        x = []
        for i in array:
            if coordinate != i:
                x.append(i)
        return x

    def erase(self, coordinate):
        new_coordinate = self.__reference_cells(coordinate)
        if new_coordinate == self.init:
            self.init = None
        if new_coordinate in self.walls:
            self.walls = self.__remove(self.walls, new_coordinate)
        if new_coordinate in self.end:
            self.end = self.__remove(self.end, new_coordinate)

    def set_up(self):
        to_delete = []
        for i in range (len(self.walls)):
            if self.walls[i][0] >= self.reference[0] and self.walls[i][0] < self.reference[0] + self.size and self.reference[1] <= self.walls[i][1] < self.reference[1] + self.size:
                    self.walls[i] = (self.walls[i][0] - self.reference[0], self.walls[i][1] - self.reference[1])
            else:
                to_delete.append(self.walls[i])

        for element in to_delete:
            self.walls = self.__remove(self.walls, element)

        self.init = (self.init[0] - self.reference[0], self.init[1] - self.reference[1])

        for i in range(len(self.end)):
            self.end[i] = (self.end[i][0] - self.reference[0], self.end[i][1] - self.reference[1])



class Observer:
    def __init__(self, size):
        toSend.size = size

    def paint_init(self, i, j):
        paint(i, j, (46, 139, 87))
    def paint_end(self, i, j):
        paint(i, j, (124, 10, 2))
    def paint_seen(self, i, j):
        paint(i, j, (96, 125, 139))
    def paint_current(self, i, j):
        paint(i, j, (176, 190, 197))
    def paint_shortest_path(self, i, j):
        paint(i, j, (253, 216, 53))

    def not_found(self):
        tkinter.Tk().wm_withdraw()
        messagebox.showerror('Warning', "Couldn't reach one checkpoint. After Accept, press ESC to retry")

screen_size = 600
num_lines = 40
toSend = Connection()
MIN_SIZE = 3
MAX_SIZE = 200

pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))

def create_screen():
    pygame.display.set_caption("A* PathFinder > Drawing Walls")
    screen.fill((250, 250, 250))
    pygame.display.update()


def add_lines():
    """Draw all the squares"""
    color = (150, 150, 150) #Soft Grey Color
   #Vertical lines
    for pos in range(0, screen_size, screen_size//toSend.size):
        pygame.draw.line(screen, color, [pos, 0], [pos, screen_size], 1)

    #Horitzontal lines
    for pos in range(0, screen_size, screen_size//toSend.size):
        pygame.draw.line(screen, color, [0, pos], [screen_size, pos], 1)

    pygame.display.update()

def paint_grid_border():
    #print("reference :"+str(toSend.reference)+", size: "+str(toSend.size))
    blanc_casse = (210, 210, 210)
    if toSend.reference[0] == 0:
        for j in range (toSend.size):
            paint_no_update(0, j, blanc_casse)
    if toSend.reference[1] == 0:
        for i in range(toSend.size):
            paint_no_update(i, 0, blanc_casse)
    if toSend.reference[0] + toSend.size >= MAX_SIZE:
        for j in range(toSend.size):
            paint_no_update(toSend.size - 1, j, blanc_casse)
    if toSend.reference[1] + toSend.size >= MAX_SIZE:
        for i in range(toSend.size):
            paint_no_update(i, toSend.size - 1, blanc_casse)

def coordinates_click(status):
    x, y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click == (1, 0, 0):
        if status == "Draw Walls":
            mark_as_wall((x, y))
        elif status == "Select Initial Point":
            mark_as_initial((x, y))
        elif status == "Select Checkpoints":
            mark_as_end((x, y))

    if click == (0, 0, 1):
        unmark((x, y))

def mark_as_initial(coordinates):
    global toSend
    if toSend.init != None:
        i, j = toSend.init
        erase(i, j)
    i, j = coordinates_to_index(coordinates[0], coordinates[1])
    paint(i, j, (46, 139, 87))
    toSend.add_init((i, j))


def mark_as_end(coordinates):
    global toSend
    i, j = coordinates_to_index(coordinates[0], coordinates[1])
    paint(i, j, (124, 10, 2))
    time.sleep(1)
    toSend.add_end((i, j))


def mark_as_wall(coordinates):
    global toSend
    i, j = coordinates_to_index(coordinates[0], coordinates[1])
    paint(i, j, (0, 0, 0))
    toSend.add_wall((i, j))

def unmark(coordinates):
    global toSend
    i, j = coordinates_to_index(coordinates[0], coordinates[1])
    erase(i, j)
    toSend.erase((i, j))

def paint(i, j, color):
    paint_no_update(i, j, color)
    pygame.display.update()

def paint_no_update(i, j, color):
    pygame.draw.rect(screen, color, (
    i*screen_size//toSend.size, j*screen_size//toSend.size, screen_size//toSend.size, screen_size//toSend.size))
    draw_mini_border(i*screen_size//toSend.size, j*screen_size//toSend.size)


def erase(i, j):
    pygame.draw.rect(screen, (250, 250, 250), (
    i*screen_size//toSend.size, j*screen_size//toSend.size, screen_size//toSend.size, screen_size//toSend.size))
    draw_mini_border(i*screen_size//toSend.size, j*screen_size//toSend.size)
    pygame.display.update()

def draw_mini_border(i, j):
    pygame.draw.line(screen, (150, 150, 150), [i, j], [i+screen_size//toSend.size, j], 1)
    pygame.draw.line(screen, (150, 150, 150), [i, j], [i, j+screen_size//toSend.size], 1)


def coordinates_to_index(x, y):
    count = 0
    i = 0
    for init in range(0, screen_size, screen_size//toSend.size):
        if x >= init and x < init + screen_size//toSend.size:
            i = count
        count += 1

    count = 0
    j = 0
    for init in range(0, screen_size, screen_size//toSend.size):
        if y >= init and y < init + screen_size//toSend.size:
            j = count
        count += 1
    return i, j

def check_status(status):
    global toSend
    if status == "Select Initial Point" and toSend.init == (0, 0):
        unmark((0, 0))
        mark_as_initial((0, 0))
        return True
    elif status == "Select Initial Point" and toSend.init == None:
        tkinter.Tk().wm_withdraw()  # to hide the main window
        messagebox.showerror('Warning', "You need to select one initial-point")
        return False
    elif status == "Select Checkpoints" and toSend.end == []:
        tkinter.Tk().wm_withdraw() # to hide the main window
        messagebox.showerror('Warning', "You need to select at least one end-point")
        return False
    elif status == "Select Checkpoints":
        toSend.set_up()
        astar.main(toSend.walls, toSend.init, toSend.end, toSend.size)
    return True

def new_size(direction):
    index = toSend.size
    not_found = not (index + direction < MIN_SIZE or index + direction > MAX_SIZE)
    while not_found:
        index += direction
        if screen_size % index == 0:
            not_found = False
    return index

def maximaze_grid():
    global toSend
    x, y = pygame.mouse.get_pos()
    i, j = coordinates_to_index(x, y)
    toSend.size = new_size(-1)
    create_screen()
    add_lines()
    new_grid_maximaze(i, j)

def set_walls(x_init, y_init, x_end, y_end):
    for wall in toSend.walls:
        if wall[0] >= x_init and wall[0] <= x_end and wall[1] >= y_init and wall[1] <= y_end:
            paint_no_update(wall[0] - x_init, wall[1] - y_init, (0, 0, 0))
    pygame.display.update()

def new_grid_maximaze(i, j):
    global toSend
    i += toSend.reference[0]
    j += toSend.reference[1]
    print("Cells clicked: " + str((i, j)))
    toSend.reference = (min(MAX_SIZE - toSend.size, max(i - toSend.size//2, 0)),
                        min(MAX_SIZE - toSend.size, max(j - toSend.size//2, 0)))
    print("Reference: " + str(toSend.reference)+" size: "+str(toSend.size))

    paint_grid_border()
    set_walls(toSend.reference[0], toSend.reference[1],
              toSend.reference[0] + toSend.size, toSend.reference[1] + toSend.size)

def new_grid_reduce(middle):
    global toSend
    toSend.reference = (min(max(middle[0] - toSend.size//2, 0), MAX_SIZE - toSend.size), min(max(middle[1] - toSend.size//2, 0), MAX_SIZE - toSend.size))
    paint_grid_border()
    set_walls(toSend.reference[0], toSend.reference[1], toSend.reference[0] + toSend.size, toSend.reference[1] + toSend.size)

def reduce_grid():
    global toSend
    middle = (toSend.reference[0] + toSend.size//2, toSend.reference[1] + toSend.size//2)
    toSend.size = new_size(1)
    create_screen()
    add_lines()
    new_grid_reduce(middle)

def main():
    global screen, toSend
    status_list = ["Draw Walls", "Select Initial Point", "Select Checkpoints", "Running"
                                                                              "", "Clear"]
    status = status_list[0]
    create_screen()
    paint_grid_border()
    add_lines()
    pygame.display.set_caption("A* PathFinder > "+status)
    while True:
        for event in pygame.event.get():
            coordinates_click(status)
            if status == "Clear" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and event.key == pygame.K_RETURN:
                    if not check_status(status):
                        continue
                    status_list = status_list[1:]
                    status = status_list[0]
                    pygame.display.set_caption("A* PathFinder > " + status)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    status_list = ["Draw Walls", "Select Initial Point", "Select Checkpoints", "Running"
                                                                              "", "Clear"]
                    status = status_list[0]
                    toSend.reset()
                    create_screen()
                    paint_grid_border()
                    add_lines()
            if event.type == pygame.KEYDOWN:
                if status == "Draw Walls":
                    if event.key == pygame.K_UP:
                        maximaze_grid()
                    elif event.key == pygame.K_DOWN:
                        reduce_grid()

if __name__ == '__main__':
    main()