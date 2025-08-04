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
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import sys
from uploadImage import handle_uploaded_image
from puzzle import PuzzleGame
from solver import solve_puzzle

# Determine if running as executable
is_exe = getattr(sys, 'frozen', False)

if is_exe:
    template_dir = os.path.join(sys._MEIPASS, 'templates')
    static_dir = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(sys.executable), 'static/uploaded_images')
else:
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'static/uploaded_images'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



#Global variable to track the current game state
current_game = None


@app.route('/', methods=['GET', 'POST'])
def index():
    global current_game

    if request.method == 'POST': # Handle POST requests
        if 'image' in request.files: # Image upload handler
            file = request.files['image']
            if file.filename != '':
                image_path = handle_uploaded_image(file, app.config['UPLOAD_FOLDER']) # Save and Process image
                current_game = PuzzleGame(image_path) # Initialize the game using the now sliced image
                return render_template('index.html',
                                       game=current_game.get_state(),
                                       image_path=image_path)

        elif 'move' in request.form: # Tile movement handler
            direction = request.form['move']
            if current_game:
                current_game.move_tile(direction) # Move the tile into the direction the player presses, and rerender the game.
                return render_template('index.html',
                                       game=current_game.get_state(),
                                       image_path=current_game.image_path)

        elif 'shuffle' in request.form: # Shuffle the puzzle. Calls the shuffle function and rerenders the game.
            if current_game:
                current_game.shuffle()
                return render_template('index.html',
                                       game=current_game.get_state(),
                                       image_path=current_game.image_path)

        elif 'solve' in request.form: # Generates a list of steps based on the calculated solution created by the A* algorithm.
            if current_game:
                solution = solve_puzzle(current_game)
                return render_template('index.html',
                                       game=current_game.get_state(),
                                       image_path=current_game.image_path,
                                       solution=solution)

    return render_template('index.html', game=None, image_path=None) # Default Get request handler

# Route to serve all uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)