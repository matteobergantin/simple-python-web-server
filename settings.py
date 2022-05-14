from pathlib import Path
from os.path import sep as DIRECTORY_SEPARATOR              # i.e. '/' on Linux and '\' on Windows
import views                                                # User code

# TODO: Implement cookie management

HOSTNAME          = "0.0.0.0"
PORT              = 8000
BASE_DIR          = str(Path(__file__).parent.resolve())        # Current directory
HTDOCS_DIR        = BASE_DIR + DIRECTORY_SEPARATOR + "htdocs"   # "htdocs" directory path
READING_SIZE      = 1024*1024                                   # The maximum amount of bytes to read from a file in a single read() function call, set this to -1 to read until EOF
ALLOW_FILE_ACCESS = True                                        # If a file exists in the htdocs folder, should it be possible to access to it directly?
DIRECTORY_LISTING = True                                        # If set to True, this will allow people to have a simple interface to show files in a directory, if the index file of that directory does not exist 
INDEX_FILE_NAME   = "index.html"                                # Index file name, "index.html" by default, used when trying to access directories
CONSOLE_LOGGING   = True                                        # Choose whether to log stuff on the console or not

# Tell the server which function to call when an error occurs
# Keep in mind there is a default behaviour to errors, it's not mandatory to override these methods
# This must contain a list of tuples (int, callable)
# Where "int" is the error code (expressed as an integer) and "callable" a callable object
# "callable" will be called when an error of code "int" occurs
error_handlers = [
    (500, views.handle500),                                 # This is just a test, visit http://HOSTNAME:PORT/send401 to see the behaviour of this function
]

# This must contain a list of tuples (str, callable)
# Where "str" is the path (expressed as a str object) and "callable" a callable object
# "callable" will be called when a request happens on the "str" path
urlpatterns = [
    ("/sayHi", views.sayHi),                          # Visit http://HOSTNAME:PORT/sayHello to call views.sayHello
    ("/sayGoodbye", views.sayGoodbye),                      # Visit http://HOSTNAME:PORT/sayGoodbye to call views.sayGoodbye
    ("/request", views.print_request_data),                 # This will print on python's console any request data given
    ("/send500", views.send500),                            # This will emulate a 500 error code, just to test error handling
]


# Error codes - don't edit
ERROR_POST_NO_CONTENT_TYPE      = 0
ERROR_POST_PARSE_CONTENT_LENGTH = 1
ERROR_POST_NO_BOUNDARY          = 2
ERROR_POST_PARSE_JSON           = 3
ERROR_POST_EMPTY                = 4