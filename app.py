import os
import chardet
from functools import lru_cache
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static_files')
static_dir = app.static_folder

@lru_cache(maxsize=128)
def read_file(file_path, start_line=None, end_line=None):
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
        return "Error decoding file with detected encoding: {}".format(detected_encoding)

    if start_line is not None and end_line is not None:
        content_lines = content.split('\n')
        selected_lines = content_lines[start_line:end_line+1]
        content = '\n'.join(selected_lines)
        if not content.strip():
            return "No content found between start line and end line."
        
    return content

@app.route('/', methods=['GET'])
@app.route('/<filename>', methods=['GET'])
def display_file(filename='file1.txt'):
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
        return render_template('error.html', error=str(e))
    except Exception as e:
        return render_template('error.html', error="An error occurred: {}".format(str(e)))


    return render_template('file.html', content=content, filename=filename)

if __name__ == "__main__":
    app.run()
