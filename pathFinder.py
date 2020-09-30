"""
This project was written by: Coby Chapman.

The Idea:
Make a algorith that any school could use to help year 7 pupils find there way between class rooms.

CURRENTLY UNDER DEVELOPMENT
Meaning there is some bugs and some room coordinates are wrong.
"""

# Modules that i need

import algorithm
import pygame
import math
from queue import PriorityQueue  # This is a module to help program the alogorithm
import sys
import time
import os
import shutil
import random

# Default variables

WIDTH = 1000  # The width of the screen
# Make the window object for pygame
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("School Algorithm")  # Set the title of the display

# Color variables for the visulisation

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (94, 139, 245)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 244, 208)
LIGHTBLUE = (141, 244, 255)


class Spot:
    """
    The spot class
    Each instance of this will be a spot on the board
    They will have different colors depending on the state
    This is so we can loop through them and draw them all
    very quickly

    """

    def __init__(self, row, col, width, total_rows):
        """
        Args:
            row (int): The row this spot is on.
            col (int): The column this spot is on.
            width (int): The width of the spot.
            total_rows (int): The total number of rows and columns in the grid.
        """
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.total_rows = total_rows
        # Each color represents a state. EG: BLUE is a barrier meaning that the algorithm knows it cannot go through this spot. See all colors bellow:
        self.color = WHITE
        """
        RED = If the algorithm has already checked this spot for the final destination.
        BLUE = If the spot is a wall / barrier.
        ORANGE = If the spot is the starting point.
        TURQUOISE = If the spot is the ending point.
        PURPLE: If this spot is in the final path.
        """
        self.neighbors = []
        self.width = width

    def get_pos(self):
        # This will return the position of this spot
        return self.row, self.col

    def is_closed(self):
        # This will return true or false depending on if it is closed
        return self.color == RED

    def is_open(self):
        # This will return true or false depending on if it is open
        return self.color == GREEN

    def is_barrier(self):
        # This will return true or false depending on if it is a barrier
        return self.color == BLUE

    def is_start(self):
        # This will return true or false depending on if it is start position
        return self.color == ORANGE

    def is_end(self):
        # This will return true or false depending on if it is end position
        return self.color == TURQUOISE

    def reset(self):
        # Reset the spot to white
        self.color = WHITE

    """
    The rest of these functions just make the spot into a different color
    """

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLUE

    def make_stair(self):
        self.color = GREY

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def make_room(self):
        self.color = LIGHTBLUE

    def draw(self, win):
        """This function will draw the spot on the screen.

        Args:
            win (pygame surface): The pygame surface to draw on.
        """
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        """This function will bring back all the spot classes in a cross formation one spot around this spot
        and will add to the neighbors list if it is not a barrier.

        Args:
            grid (list): The list you store all the spot classes in. EG: if the grid was 2x2 [[SPOT, SPOT], [SPOT, SPOT]]
        """
        # Reset the neighbors list.
        self.neighbors = []
        # Look down.
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Look up.
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Look right.
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Look left.
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        """This function is used if the spot class is commpared to another like this: SPOT1 > SPOT2 . It will always return False.

        Args:
            other (SpotClass): The other spot class it is commpared to.

        Returns:
            bool: False
        """
        return False

def make_grid(rows, width):
    """This function will generate all the spots for your grid
    and store them in a 2d list EG: 
    If it was a 2x2 grid [[SPOT, SPOT], [SPOT, SPOT]] .
    """

    grid = []
    # Get the gap needed between spots
    # so when we make a new spot we now what the x and y coordinates are
    gap = width // rows
    # Loop through all the rows
    for i in range(rows):
        # Append a empty list into the grid so that each spot on that col goes in that list
        grid.append([])
        for j in range(rows):
            # Create a new spot object in the current row and col
            spot = Spot(i, j, gap, rows)
            # Append that spot to the empty list we created above
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    """This function will draw the grid lines between each spot."""

    # Once again calculate the gap between each line
    gap = width // rows
    # Loop through the rows of the grid
    for i in range(rows):
        # Draw a horizontal line
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        # pass
        # Loop through the cols of the row
        for j in range(rows):
            # Draw a vertical line
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    """This function will draw all the spots onto the screen.
    We will call this function each frame"""

    # Fill the screen with white
    win.fill(WHITE)
    # Loop through all the rows in grid
    for row in grid:
        # Loop through the spots in the row
        for spot in row:
            # Draw the spots
            spot.draw(win)
    # Draw the grid lines
    draw_grid(win, rows, width)
    # Update screen so it appears
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """This function translate a mouse click position into a row and col.
    """

    gap = width // rows  # Work out the width of each spot
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def make_barrier(grid, ROWS, floor):
    """This function will add all the barriers and rooms to the grid

    Args:
        grid (list): The 2d list that stores all the spots in there row and column.
        ROWS (int): The number of rows and columns in the grid
        floor (int): The floor you want to create the grid for

    Returns:
        list: The 2d list that stores all the spots in there row and column with the new spots.
    """

    """The files that are being read below contain coordinates for that thing
    Say for example f1/locs.txt stores the coordinates for all the barriers that need to be drawn.
    We add new coordinates to this file via the draw.py file.
    """

    if floor == "0":  # If bottom floor
        f = open(
            "f1\\locs.txt", "r")  # The barrier coordinates for floor 1
        # Read all the lines
        lines = f.readlines()
        for line in lines:
            line = line.split(", ")
            try:
                spot = grid[int(line[0])][int(line[1])]
                spot.make_barrier()
            except:
                pass
        f.close()

        f = open(
            "f1\\locsroom1.txt", "r")  # The room coordinates for floor 1
        # Read all the lines
        lines = f.readlines()
        for line in lines:
            line = line.split(", ")
            spot = grid[int(line[0])][int(line[1])]
            spot.make_room()
        f.close()
    else:
        f = open(
            "f2\\locs.txt", "r")  # The barrier coordinates for floor 2
        # Read all the lines
        lines = f.readlines()
        for line in lines:
            line = line.split(", ")
            try:
                spot = grid[int(line[0])][int(line[1])]
                spot.make_barrier()
            except:
                pass

        f.close()

        f = open(
            "f2\\locsroom1.txt", "r")  # The room coordinates for floor 2
        # Read all the lines
        lines = f.readlines()
        for line in lines:
            line = line.split(", ")
            spot = grid[int(line[0])][int(line[1])]
            spot.make_room()
        f.close()

    return grid


def GetStartAndEndPosition(RoomLocations, startroom, endroom, grid):
    """This function will use a dictionary to find out what the start and end positions should be

    Args:
        RoomLocations (dict): A dictionary with the coordinates for each room in it
        startroom (int): The start room number
        endroom (int): The end room number
        grid (list): The 2d list that stores all the spots in there row and column

    Returns:
        list: All of the infomation that this function generates.
    """
    try:
        startloc = RoomLocations[startroom]
    except KeyError:
        return f"{startroom} is not currently in our database or it is not a valid room."
    
    try:
        endloc = RoomLocations[endroom]
    except KeyError:
        return f"{endroom} is not currently in our database or it is not a valid room."

    startloc = startloc.split(" ")
    endloc = endloc.split(" ")

    startSpot = grid[int(startloc[0])][int(startloc[1])]
    endSpot = grid[int(endloc[0])][int(endloc[1])]

    startSpot.make_start()
    endSpot.make_end()

    # Index 2 - 3 are the floor numbers of each location
    Spots = [startSpot, endSpot, startloc[2], endloc[2]]
    return Spots


def MultifloorCheck(EndStartPositions, grid, startRoom, win, ROWS, width):
    """This file will handle multifloor requests

    Args:
        EndStartPositions (list): The positions of the start and end
        grid (list): The 2d list that stores all the spots in there row and column
        startRoom (int): The room number that the user is starting algorithm
        win (pygame surface): The surface to draw on the
        ROWS (int): The amount of rows in the grid that
        width (int): The width of each spot

    Returns:
        bool or list: False if not multifoor if multifloor returns the floor grid for the floor we move to next and the starting spot on that floor.
    """

    # This dict stores the closest stair to each room.
    ClosestStair = {
        "34": "1",
        "p1": "1",
        "33": "2",
        "35": "2",
        "p2": "1",
        "31": "1",
        "32": "1",
        "1": "1",
        "2a": "3",
        "2": "3",
        "3": "3",
        "4": "3",
        "5": "3",
        "6": "3",
        "7": "4",
        "8": "4",
        "9": "4",
        "18": "4",
        "19": "4",
        "20": "2",
        "27": "4",
        "26": "2",
        "21": "2",
        "24": "2",
        "25": "2",
        "22": "2",
        "23": "2",
        "37": "5",
        "38": "5",
        "p3": "6",
        "39": "6",
        "40": "6",
        "41": "6",
        "10": "7",
        "10a": "7",
        "11": "8",
        "12": "8",
        "13": "8",
        "14": "8",
        "15": "8",
        "16": "8",
        "16a": "8",
        "17": "7"
    }

    # This dict stores each stairs locations and the location it comes out.
    StairLocations = {
        "1": "21 38 18 41",
        "2": "53 39 49 40",
        "3": "34 93 32 95",
        "4": "45 73 32 95",
        "5": "18 41 21 38",
        "6": "49 40 53 39",
        "7": "37 75 34 93",
        "8": "32 95 45 73"
    }

    # If the floor value of the starting and ending positions are different
    if EndStartPositions[2] != EndStartPositions[3]:
        start = EndStartPositions[0]

        end = StairLocations[ClosestStair[startRoom]]  # Get the stair location
        end = end.split(" ")
        Endx = int(end[0])
        Endy = int(end[1])
        end = grid[Endx][Endy]
        end.make_end()

        for row in grid:
            for spot in row:
                # Update that spots neighbors
                spot.update_neighbors(grid)
        # Make the algorithm start
        algorithm.Algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
        ScreenShot()

        # This section works out where the stair it led you to comes out.
        ofloorEnd = ClosestStair[startRoom]
        ofloorEnd = StairLocations[ofloorEnd]
        ofloorEnd = ofloorEnd.split(" ")

        # Remake the grid for the other floor
        grid = make_grid(ROWS, width)
        grid = make_barrier(grid, ROWS, EndStartPositions[3])

        return [grid[int(ofloorEnd[2])][int(ofloorEnd[3])], grid]

    else:
        return False


def ScreenShot():
    """This function will take a screenshot of the screen. In the future it will have a meaningful name but for now it is just a random number.
    """
    Fileid = str(random.randint(0, 100000))
    pygame.image.save(WIN, "screenshot" + Fileid + ".jpg")  # Take screenshot

    os.rename("screenshot" + Fileid + ".jpg",
              "Screenshots\\screenshot" + Fileid + ".jpg")  # Move screenshot into Screeenshots folder

    ScreenshotList.append(
        "Screenshots\\screenshot" + Fileid + ".jpg")


def main(StartRoom, EndRoom, win=WIN, width=WIDTH):
    """This is the main function were everything will be managed by

    Args:
        StartRoom (int): The room number of the start room
        EndRoom (int): The room number of the end room
        win (pygame surface):, optional): The pygame surface to draw one. Defaults to WIN.
        width (int, optional): The width of each spot. Defaults to WIDTH.

    Returns:
        list: A list of paths to the screenshots so the main file can send them
    """
    ROWS = 100
    # Make the grid
    grid = make_grid(ROWS, width)
    # Start and end position
    start = None
    end = None
    done = False

    run = True

    global ScreenshotList
    ScreenshotList = []

    # The room coordinates the last didget is the floor number.
    RoomLocations = {
        "34": "32 35 0",
        "p1": "42 35 0",
        "33": "51 35 0",
        "35": "45 36 0",
        "p2": "37 36 0",
        "31": "25 48 0",
        "32": "25 55 0",
        "1": "25 67 0",
        "2a": "23 74 0",
        "2": "23 74 0",
        "3": "27 80 0",
        "4": "27 86 0",
        "5": "25 92 0",
        "6": "29 92 0",
        "7": "47 92 0",
        "8": "47 87 0",
        "9": "47 84 0",
        "18": "80 72 0",
        "19": "80 72 0",
        "20": "71 51 0",
        "27": "70 65 0",
        "26": "70 54 0",
        "21": "78 47 0",
        "24": "66 47 0",
        "25": "75 47 0",
        "22": "71 47 0",
        "23": "71 47 0",
        "37": "19 37 1",
        "38": "26 37 1",
        "p3": "33 37 1",
        "39": "42 37 1",
        "40": "44 38 1",
        "41": "36 38 1",
        "10": "26 82 1",
        "10a": "26 87 1",
        "11": "26 91 1",
        "12": "28 92 1",
        "13": "28 92 1",
        "14": "37 92 1",
        "15": "42 95 1",
        "16": "43 90 1",
        "16a": "43 86 1",
        "17": "43 81 1"
    }

    EndStartSpots = GetStartAndEndPosition(
        RoomLocations, StartRoom, EndRoom, grid)  # Get the start and end spots.

    if isinstance(EndStartSpots, str): # If file returned a string. In my case that means a exception happend.
        return EndStartSpots
    start = EndStartSpots[0]
    end = EndStartSpots[1]

    grid = make_barrier(grid, ROWS, EndStartSpots[2])

    NewFloorData = MultifloorCheck(
        EndStartSpots, grid, StartRoom, WIN, ROWS, width)
    if NewFloorData:
        start = NewFloorData[0]
        start.make_start()
        grid = NewFloorData[1]
        end = grid[end.get_pos()[0]][end.get_pos()[1]]
        end.make_end()

    # Infinate loop
    while run:
        draw(win, grid, ROWS, width)
        # Loop through all event that have happend in this frame
        for event in pygame.event.get():
            # If the event is a certain event
            if event.type == pygame.QUIT:  # If pressed X exit infinate loop
                run = False

            # If left mouse clicked
            if pygame.mouse.get_pressed()[0]:
                # Get x and y coordinate of mouse
                pos = pygame.mouse.get_pos()
                # Translate mouse pos into row and col
                row, col = get_clicked_pos(pos, ROWS, width)
                # Get the spot you clicked
                spot = grid[row][col]

    # Update all neighbors of all of the spots
    # Loop through the rows of the grid
        for row in grid:
            for spot in row:
                # Update that spots neighbors
                spot.update_neighbors(grid)
        # Make the algorithm start
        if not done:
            algorithm.Algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
            done = True
            ScreenShot()
            return ScreenshotList

    # When while loop breaks end game
    pygame.quit()


# FOR DEBUGGING ONLY. THIS FILE SHOULD NEVER BE RAN AS A STANDALONE FILE UNLESS FOR DEBUGGING.
if __name__ == "__main__":
    main(1, 1)
