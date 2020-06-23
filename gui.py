import pygame
import astar
import time
from tkinter import *
from tkinter import messagebox

class Connection:
    def __init__(self):
        self.init = (0, 0)
        self.walls = []
        self.end = []
        pass

    def add_wall(self, wall):
        self.walls.append(wall)

    def add_init(self, init):
        self.init = init

    def add_end(self, end):
        self.end.append(end)

    def remove(self, coordinate):
        x = []
        for i in self.walls:
            if coordinate != i:
                x.append(i)
        self.walls = x

    def erase(self, coordinate):
        if coordinate == self.init:
            self.init = (0, 0)
        if coordinate in self.walls:
            self.remove(coordinate)
        if coordinate in self.end:
            self.end.remove(coordinate)

class Observer:
    def __init__(self):
        pass
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


screen_size = 600
num_lines = 50 #screen_size%num_lones = 0
toSend = Connection()

pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))

def create_screen():
    pygame.display.set_caption("A* PathFinder")
    screen.fill((250, 250, 250))
    pygame.display.update()

def add_lines():
    """Draw all the squares"""
    color = (150, 150, 150) #Soft Grey Color
   #Vertical lines
    for pos in range(0, screen_size, screen_size//num_lines):
        pygame.draw.line(screen, color, [pos, 0], [pos, screen_size], 1)
        pygame.display.update()

    #Horitzontal lines
    for pos in range(0, screen_size, screen_size//num_lines):
        pygame.draw.line(screen, color, [0, pos], [screen_size, pos], 1)
        pygame.display.update()

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
    i, j = toSend.init
    erase(i, j)
    i, j = coordinates_to_index(coordinates[0], coordinates[1])
    paint(i, j, (46, 139, 87))
    toSend.init = (i, j)


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
    pygame.draw.rect(screen, color, (
    i*screen_size//num_lines, j*screen_size//num_lines, screen_size//num_lines, screen_size//num_lines))
    draw_mini_border(i*screen_size//num_lines, j*screen_size//num_lines)
    pygame.display.update()

def erase(i, j):
    pygame.draw.rect(screen, (250, 250, 250), (
    i*screen_size//num_lines, j*screen_size//num_lines, screen_size//num_lines, screen_size//num_lines))
    draw_mini_border(i*screen_size//num_lines, j*screen_size//num_lines)
    pygame.display.update()

def draw_mini_border(i, j):
    pygame.draw.line(screen, (150, 150, 150), [i, j], [i+screen_size//num_lines, j], 1)
    pygame.draw.line(screen, (150, 150, 150), [i, j], [i, j+screen_size//num_lines], 1)


def coordinates_to_index(x, y):
    count = 0
    i = 0
    for init in range(0, screen_size, screen_size//num_lines):
        if x >= init and x < init + screen_size//num_lines:
            i = count
        count += 1

    count = 0
    j = 0
    for init in range(0, screen_size, screen_size//num_lines):
        if y >= init and y < init + screen_size//num_lines:
            j = count
        count += 1
    return i, j

def check_status(status):
    if status == "Select Initial Point" and toSend.init == (0, 0):
        unmark((0, 0))
        mark_as_initial((0, 0))
        return True
    elif status == "Select Checkpoints" and toSend.end == []:
        Tk().wm_withdraw() # to hide the main window
        messagebox.showerror('Warning', "You need to select at least one end-point")
        return False
    elif status == "Select Checkpoints":
        astar.main(toSend.walls, toSend.init, toSend.end)
    return True

def main():
    status_list =["Draw Walls", "Select Initial Point", "Select Checkpoints", "Running"
                                                                              "", "Clear"]
    status = status_list[0]
    global screen
    create_screen()
    add_lines()
    turn_on = True
    pygame.display.set_caption("A* PathFinder > "+status)
    while turn_on:
        for event in pygame.event.get():
            coordinates_click(status)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and event.key == pygame.K_RETURN:
                    if not check_status(status):
                        continue
                    status_list = status_list[1:]
                    status = status_list[0]
                    pygame.display.set_caption("A* PathFinder > " + status)

            if event.type == pygame.QUIT:
                turn_on = False


if __name__ == '__main__':
    main()