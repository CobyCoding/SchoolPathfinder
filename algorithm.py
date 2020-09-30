import pygame
import math
from queue import PriorityQueue

def reconstruct_path(came_from, current, draw):
    """This function will take a list of spots that the algorithm has decided that they are the quickest root from start to end and turn them into a path spot.

    Args:
        came_from (list): Look for the above comment.
        current (Spot): The piece the algorith last checked. Normaly the end spot
        draw ([type]): [description]
    """

    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()  # Redraw the screen with the new path spot


def Algorithm(draw, grid, start, end):
    # This function will run the algorithm to calculate the shortest route between the end pos and the start pos

    # Default variables
    count = 0
    open_set = PriorityQueue()
    # Put is basicly the same a append but put is for the PriorityQueue module
    # Add the start node to the open_set with its f score
    open_set.put((0, count, start))
    # Keep track of what node came from what node
    came_from = {}
    # This will store all g scores
    g_score = {spot: float("inf") for row in grid for spot in row}
    # Set the g score of the starting node to 0
    g_score[start] = 0
    # This will store all f scores
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    # This will keep track of the spriority queue
    open_set_hash = {start}
    # Run until open set is empty
    while not open_set.empty():
        # If player wants to quit algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        # If current node is end node we got a path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        # Consider neighbors of current node
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def h(p1, p2):
    """This will give a estimate of the distance between the positions passed in and the end position.
    We use this to not even consider longer routes."""

    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)
