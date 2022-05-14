# Disclaimer
This project is an extremely simple web server that implements very basic security features, it should not be used in production.

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
* `settings.py`: A file that contains the settings for the Web Server (more info below).
* `utils.py`: A file that contains useful functions, most of the parsing is implemented here.
* `views.py`: A file which implements the functions contained in the `urlpatterns` list, created in the `settings.py` file.
* `web_server.py`: Where the server is actually implemented.
* `main.py`: This the file to run in order to start the server.

# Installation
## Required libraries / modules
This project uses the http.server module for Python, it should be installed automatically with any Python3 distribution, so nothing should be installed beforehand.

If that's not the case please check your Python installation.

## Downloading and running the Web Server
Clone the repository using
```
git clone https://github.com/matteobergantin/simple-python-web-server.git
```
Browse to the downloaded directory with
```
cd simple-python-web-server
```
Run the webserver using the command
```
python3 main.py
```

# Configuration and Usage
To configure the server edit the variables in the `settings.py` file.

## Configuration options:
* `HOSTNAME`: The Web Server hostname, by default 0.0.0.0, for debugging purposes set this variable to localhost or 127.0.0.1
* `PORT`: The Web Server port, by default 8000, change this to 80 if you don't want to specify the port every time you access the Web Server URL on a browser.
* `BASE_DIR`: The path to the directory of the project
* `HTDOCS_DIR`: The path to the directory "htdocs", if you save any file to the directory specified here, the users can access them by specifying the path (unless the ALLOW_FILE_ACCESS variable is set to False)
* `READING_SIZE`: When we want to send a file to the user we need to open it and read it, to do that we must divide the file in chunks, this is the chunk size (in bytes), set it to -1 to read all the file before sending it to the client (Note that this is a terrible idea for files of high dimension)
* `ALLOW_FILE_ACCESS`: If this variable is set to False, no file inside HTDOCS_DIR will be accessed, instead the user will encounter a 401 (Unauthorized) error
* `DIRECTORY_LISTING`: If set to True, users trying to access a directory which DOES NOT have an index file will see a simple File Explorer instead of receiving a 404 error
* `INDEX_FILE_NAME`: The index file name, used to tell the server where to look for an index file when a directory is requested.
* `error_handlers`: This is a list of `tuple[int, callable]` where `int` is the error code (expressed as an integer) and `callable` a callable object. `callable` will be called when an error of code `int` occurs
* `urlpatterns`: This is a list of `tuple[str, callable]` where `str` is the url path and where `callable` is the function to be called when a request happens on that path

## Testing the Web Server

Once downloaded and installed the Web Server go to `http://localhost:8000/` to check if the Web Server is running.

To test backend code you can go to `http://localhost:8000/sayHi` or to `http://localhost:8000/sayGoodbye`, you can find the implementation of these two functions inside the file `views.py` and you can see how to bind a function to a specific URL path inside the `settings.py` file.

Additionally, to check if request parsing works you can perform any requests on `http://localhost/request` and this will print the request data (both GET and POST) on the Python shell.

## Binding a URL path to a custom function
Open the `settings.py` file and add an entry to the `urlpatterns` list object.

An entry is composed of a tuple[str,callable], the "str" refers to the URL path and "callable" refers to a function to call when a connection on that path happens.
The function will get the whole WebServer object as an argument.

Again, you can check the file `views.py` for examples.

## Web Server functions
Here's the list of functions available through the Web Server object:
* `send_directory_listing(dir_path: str)`: This will send a file explorer build with just HTML and CSS to the user, it's the default function that gets called if the `DIRECTORY_LISTING` variable is enable, The `dir_path` variable represents the path of the directory you want to show the user.
* `redirect(new_location: str)`: Redirects the user to `new_location`.
* `send_error_code(code: int, default)`: This triggers an error of code `code` and if there is not user-specified function to handle the error it will execute `default`, which must be a callable object.
* `broadcast_file(file_path: str)`: Sends the user the file specified in the `file_path` variable, the `Content-Type` and `Content-Length` headers are set automatically, this is the default function that gets called if the `ALLOW_FILE_ACCESS` variable is set to True.
* `parse_get_data()`: This function, when called, returns a dict[str,str] that represents the GET data sent to the server.
* `parse_post_data()`: This function, when called, returns a dict[str,mix] that represents the POST data passed to the server, or returns None if there is no POST data, or if an error happened, you can check the last error from the `last_error` variable in the WebServer object.