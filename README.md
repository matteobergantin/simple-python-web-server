# Introduction
This is a simple Web Server implemented in Python using `TheadingHTTPServer` and inheriting by `BaseHTTPRequestHandler`.

I created this Web Server because I wanted a simple web server, which was both a CGI Server and a File Server, before this project I used django, which is a bit overkill for what I need to do.

The usage is very simple, you can access files by connecting to the web server and specifying the file name in the url path.
For example:
* If I wanted to access the file `test.txt` located in the directory `htdocs` I would need to request the url `http://{SERVER HOSTNAME}:{SERVER PORT}/test.txt`
* If I wanted to access the file `bar.json` located under `htdocs/foo` I would need to request the url `http://{SERVER HOSTNAME}:{SERVER PORT}/foo/bar.json`

To specify a behaviour for specific URL paths, edit the `settings.py` file and add an entry to `urlpatterns` (more information below).

# Project files and folders
* `htdocs`: Folder that contains all the files that can be accessed from the server.
* `abstract_web_server.py`: File that contains an abstract class of the Web Server that will be implented in the `web_server.py` file, is useful to use IntelliSense.
* `settings.py`: A file that contains the settings for the Web Server (more info below).
* `utils.py`: A file that contains useful functions, most of the parsing is implemented here.
* `views.py`: A file which implements the functions contained in the `urlpatterns` list, created in the `settings.py` file.
* `web_server.py`: Where the server is actually implemented, this is also the file to run to start the server.

# Installation
## Required libraries / modules
This project uses the http.server module for Python, it should be installed automatically with any Python3 distribution, so nothing should be installed beforehand.

## Downloading and running the Web Server
* Clone the repository using `git clone ...`
* Browse to the downloaded directory with `cd {directory name}`
* Run the webserver using the command `python3 web_server.py`

# Configuration
To configure the server edit the variables in the `settings.py` file, you can change pretty much everything from there.

## Configuration options:
* `HOSTNAME`: The Web Server hostname, by default 0.0.0.0, for debugging purposes set this variable to localhost or 127.0.0.1
* `PORT`: The Web Server port, by default 8000, change this to 80 if you don't want to specify the port every time you access the Web Server URL on a browser.
* `BASE_DIR`: The path to the directory of the project
* `HTDOCS_DIR`: The path to the directory "htdocs", if you save any file to the directory specified here, the users can access them by specifying the path (unless the ALLOW_FILE_ACCESS variable is set to False)
* `READING_SIZE`: When we want to send a file to the user we need to open it and read it, to do that we must divide the file in chunks, this is the chunk size (in bytes), set it to -1 to read all the file before sending it to the client (Note that this is a terrible idea for files of high dimension)
* `ALLOW_FILE_ACCESS`: If this variable is set to False, no file inside HTDOCS_DIR will be accessed, instead the user will encounter a 401 (Unauthorized) error
* `INDEX_FILE_NAME`: The index file name, used to tell the server where to look for an index file when a directory is requested.
* `error_handlers`: This is a list of `tuple[int, callable]` where `int` is the error code (expressed as an integer) and `callable` a callable object. `callable` will be called when an error of code `int` occurs
* `urlpatterns`: This is a list of `tuple[str, callable]` where `str` is the url path and where `callable` is the function to be called when a request happens on that path