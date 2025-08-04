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
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)