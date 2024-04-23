# Flask File Viewer Application

## Overview
This Flask application is designed to read the content of text files and render it properly in an HTML page. It provides a single GET route that accepts the following parameters:

1. File Name: The target file name is an optional variable part of the URL and defaults to file1.txt.

2. Start Line Number and End Line Number: Optional URL query parameters to specify the range of lines to display. If not provided, the application returns all lines of the file.

3. The application preserves any markup in the files and can handle various encodings, including files with non-English content (e.g., Chinese).


## Usage

To use the application:

1. Clone the repository:
https://github.com/sannalavamsi/Flask_FileViewer.git

2. Create a virtual environment: Navigate to your project directory and run:
python3 -m venv myenv

3. Activate the virtual environment(On Windows, run):
myenv\Scripts\activate

4. Navigate to the cloned directory:
cd [FileViewer]

5. Install the required packages:
pip install -r requirements.txt

6. Start the server with the following command:
flask run

7. based on start and end endpoint: 
http://localhost:5000/file2.txt?start_line=1&end_line=3


## Endpoints

# GET /

. Displays the content of file1.txt by default.
. Renders the content in an HTML page with any markup preserved.
. Optional query parameters (start_line and end_line) can be used to specify the range of lines to display.

Example:
http://127.0.0.1:5000/ - Displays all lines of file1.txt.

http://127.0.0.1:5000/file2.txt?start_line=1&end_line=3 - Displays lines 1 to 3 of file2.txt.


# GET /samplefilename.txt

. Displays the content of the specified file.
. Renders the content in an HTML page with any markup preserved.
. Optional query parameters (start_line and end_line) can be used to specify the range of lines to display.

Example:
http://127.0.0.1:5000/file3.txt - Displays all lines of file3.txt.


# Error Handling
1. The application gracefully handles exceptions in the logic.
2. If an exception occurs, an error page with details of the exception is displayed.

# Chardet
. The chardet library is a Python library used for character encoding detection. It can automatically detect the character encoding of text files, which is particularly useful when working with files that have unknown or variable encodings.

Features:
1. Automatic Encoding Detection: chardet can analyze the byte sequences of text files and infer the most likely encoding used.
2. Wide Range of Supported Encodings: It supports a wide range of character encodings, including ASCII, UTF-8, UTF-16, ISO-8859, and many others.
