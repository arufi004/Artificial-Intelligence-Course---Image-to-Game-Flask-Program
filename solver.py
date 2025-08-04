"""
Name: 			            Anthony Rufin
Panther ID: 	            6227314
Class: 			            CAP5602 U01C 1255 - Introduction to Artificial Intelligence
Homework: 		            HW1 - Search
Due: 			            June 11, 2025
What is this program?		This program is an 8-Puzzle Game generator.
                            It takes an image from the user and turns it into a 3x3 tile puzzle.
                            This program can also reshuffle the puzzle,
                            and "solve" the puzzle by generating a list of
                            moves the user must do in order to solve the puzzle.
"""
import heapq
from collections import deque
from puzzle import PuzzleGame


def manhattan_distance(state):
    #Calculate Manhattan distance heuristic for the 8-puzzle
    distance = 0
    for i in range(3): # Iterate over all the rows and columns to calculate the manhattan distance of the
        for j in range(3):
            value = state[i * 3 + j]
            if value != 8:  # Skip the empty tile
                target_row = value // 3  # Flat Division converts a tile's value to its goal row (0,1,2)
                target_col = value % 3 # Modulo is used to map the values to columns (0,1,2)
                distance += abs(i - target_row) + abs(j - target_col) # Mahattan Distance = |x2 - x1| + |y2 - y1|
    return distance


def get_neighbors(state):
    #Generate possible moves from current state
    empty_index = state.index(8)
    row, col = empty_index // 3, empty_index % 3
    neighbors = [] # Neighbors are used to
    # The A* Algorithm requires this helper function to get all the possible next states from the current state, and to build the search tree.

    for dr, dc, move in [(1, 0, 'up'), (-1, 0, 'down'), (0, 1, 'left'), (0, -1, 'right')]: # Only valid moves are considered. Each moves cost 1 (using manhattan distance)
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = list(state)
            new_index = new_row * 3 + new_col
            new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
            neighbors.append((tuple(new_state), move))

    return neighbors


def solve_puzzle(game):
    #Solve the puzzle using A* with Manhattan distance heuristic
    start_state = tuple(game.get_flat_board()) # Converts current state and goal state into flat (1 dimensional) boards
    goal_state = tuple([0, 1, 2, 3, 4, 5, 6, 7, 8])

    if start_state == goal_state: # If we are already at the goal state, return nothing.
        return []

    # A* Algorithm
    open_set = []
    heapq.heappush(open_set, (manhattan_distance(start_state), 0, start_state)) # Push the start state and the distances of the start state tiles into the heap.

    came_from = {}
    g_score = {start_state: 0} # g_score tracks the actual cost from each state
    f_score = {start_state: manhattan_distance(start_state)} # f_score stores the g_score + manhattan distance

    open_set_hash = {start_state} # hash set containing the start state

    while open_set:
        current_f, current_g, current_state = heapq.heappop(open_set)
        open_set_hash.remove(current_state)

        if current_state == goal_state:
            # Reconstruct path. This is done once the algorithm finishes reaching the goal state. From here, we backtrack to the start, adding each step to the path dictionary until we reach
            # the start state. We reverse the dictionary to get an ordered list of steps to reach the goal state from the start state.
            path = []
            while current_state in came_from:
                current_state, move = came_from[current_state]
                path.append(move)
            path.reverse()
            return path

        # If we have not reached the goal_state, we skip the previous section and jump to here, where we check the neighbors of the current position of the empty tile
        # to see if we can find valid moves.
        # This is to compare the g_score of the next step with the current g_score, to see if the next step is an optimal path to the goal state. If it is, we add it to
        # the hashed set and heap.
        for neighbor, move in get_neighbors(current_state):
            tentative_g_score = g_score[current_state] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]: #
                came_from[neighbor] = (current_state, move)
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], g_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    return None  # No solution found (shouldn't happen for solvable 8-puzzle)