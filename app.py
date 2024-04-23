import os
import chardet
import logging
from functools import lru_cache
from flask import Flask, render_template, request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static_files')
static_dir = app.static_folder

@lru_cache(maxsize=128)
def read_file(file_path, start_line, end_line):
    """
    Read the content of a file with optional start and end line numbers.

    Args:
        file_path (str): The path to the file to read.
        start_line (int, optional): The line number to start reading from. Defaults to None.
        end_line (int, optional): The line number to stop reading at. Defaults to None.

    Returns:
        str: The content of the file between the specified start and end lines, or the entire file content if no lines are specified.
             Returns an error message if the file cannot be read or if there's an issue decoding the file.
    """
    with open(file_path, 'rb') as f:
        # Detect encoding
        detected_encoding = chardet.detect(f.read())['encoding']
        # Go back to the beginning of the file
        f.seek(0)
        # Read file content using the detected encoding
        content_bytes = f.read()

    try:
        content = content_bytes.decode(detected_encoding)
    except UnicodeDecodeError:
        error_msg = "Error decoding file with detected encoding: {}".format(detected_encoding)
        logging.error(error_msg)
        return error_msg

    content_lines = content.split('\n')
    if start_line is None and end_line is None:
        selected_lines = content_lines[:]
    elif start_line is not None and end_line is not None:
        if start_line < 0 or end_line < 0 or start_line > end_line:
            raise ValueError("Invalid start_line or end_line values.")
        selected_lines = content_lines[start_line : end_line + 1]
    elif start_line is None and end_line is not None:
        if end_line < 0:
            raise ValueError("Invalid end_line value.")
        selected_lines = content_lines[:end_line +1]
    elif start_line is not None and end_line is None:
        if start_line < 0:
            raise ValueError("Invalid start_line value.")
        if start_line > len(content_lines):  # Check if start_line is out of range
            raise IndexError("start_line is out of range.")
        selected_lines = content_lines[start_line :]
        
    return '\n'.join(selected_lines)

@app.route('/', methods=['GET'])
@app.route('/<filename>', methods=['GET'])
def display_file(filename='file1.txt'):
    """
    Display the content of a file in the browser.

    Args:
        filename (str, optional): The name of the file to display. Defaults to 'file1.txt'.

    Returns:
        str: The rendered HTML content of the file, or an error message if the file is not found or if there's an issue processing it.
    """
    try:
        file_path = os.path.join(static_dir, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found.")

        start_line = request.args.get('start_line', type=int)
        end_line = request.args.get('end_line', type=int)

        if start_line is not None and start_line < 0:
            raise ValueError("Start line number must be positive.")
        if end_line is not None and end_line < 0:
            raise ValueError("End line number must be positive.")
        if start_line is not None and end_line is not None and start_line > end_line:
            raise ValueError("Start line number cannot be greater than End line number.")

        content = read_file(file_path, start_line, end_line)
    except (FileNotFoundError, ValueError) as e:
        logging.error("Error occurred while processing request: %s", e) 
        return render_template('error.html', error=str(e))
    except Exception as e:
        logging.exception("An error occurred while processing request: %s", e)
        return render_template('error.html', error="An error occurred: {}".format(str(e)))


    return render_template('file.html', content=content, filename=filename)

if __name__ == "__main__":
    app.run()
