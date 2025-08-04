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
import sys
import uuid
from PIL import Image
import os


def handle_uploaded_image(file, upload_folder):
    # Get base path depending on executable or dev mode
    base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")

    # Create full upload path
    upload_path = os.path.join(base_path, upload_folder)
    os.makedirs(upload_path, exist_ok=True)

    # Save file
    filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    filepath = os.path.join(upload_path, filename)
    file.save(filepath)

    # Process image
    img = Image.open(filepath)
    img = img.resize((600, 600))
    img.save(filepath)

    return filename