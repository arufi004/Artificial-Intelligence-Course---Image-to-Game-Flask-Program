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
from PIL import Image
import random


class PuzzleGame:
    def __init__(self, image_path):
        self.image_path = image_path                    # The image's file path
        self.tile_size = 200  # 600 / 3                 # Our images should be cropped to the same size, to ensure consistency.
        self.board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]  # 8 represents empty space. We chose 8 as the empty space as it's the last index for this list, meaning we can fill the first seven slots
                                                        # in a for loop, and leave the last slot empty.
        self.empty_position = (2, 2)                    # Sets the empty position to the bottom right tile.
        self.solved_board = [row[:] for row in self.board] # What the board's state should look like when the puzzle is completed.
        self.tiles = self.slice_image()

    def slice_image(self):
        # Slice the image into 9 tiles
        img = Image.open(f"static/uploaded_images/{self.image_path}")
        tiles = []
        # This function iterates over three rows and columns to create each image slice, and creates bounding boxes for each tile.
        for i in range(3):
            for j in range(3):
                left = j * self.tile_size
                up = i * self.tile_size
                right = left + self.tile_size
                down = up + self.tile_size

                tile = img.crop((left, up, right, down))
                tiles.append(tile)

        return tiles

    def get_state(self):
        #Return current game state for rendering
        return {
            'board': self.board, # The board state
            'empty_position': self.empty_position, # The position of the empty tile
            'is_solved': self.board == self.solved_board # A boolean for whether the board has been solved or not.
        }

    def move_tile(self, direction):
        #Move a tile in the specified direction
        x, y = self.empty_position

        if direction == 'up' and x < 2:
            self.board[x][y], self.board[x + 1][y] = self.board[x + 1][y], self.board[x][y]
            self.empty_position = (x + 1, y)
        elif direction == 'down' and x > 0:
            self.board[x][y], self.board[x - 1][y] = self.board[x - 1][y], self.board[x][y]
            self.empty_position = (x - 1, y)
        elif direction == 'left' and y < 2:
            self.board[x][y], self.board[x][y + 1] = self.board[x][y + 1], self.board[x][y]
            self.empty_position = (x, y + 1)
        elif direction == 'right' and y > 0:
            self.board[x][y], self.board[x][y - 1] = self.board[x][y - 1], self.board[x][y]
            self.empty_position = (x, y - 1)

    def shuffle(self, moves=100):
        #Shuffle the board with random moves
        directions = ['up', 'down', 'left', 'right']
        for _ in range(moves):
            self.move_tile(random.choice(directions)) # Scranble the image 100 times in order to ensure the puzzle is sufficiently scrambled. Uses the "move" function to ensure the program
                                                      # Does not generate an impossible puzzle.

    def get_flat_board(self):
        #Return the board as a flat list (for solving)
        return [tile for row in self.board for tile in row]

    def apply_flat_board(self, flat_board):
        #Apply a flat board state to the game
        for i in range(3):
            for j in range(3):
                self.board[i][j] = flat_board[i * 3 + j]

        # Update empty position
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 8:  # 8 is empty
                    self.empty_position = (i, j)
                    return