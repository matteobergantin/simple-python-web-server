from pathlib import Path
from os.path import sep as DIRECTORY_SEPARATOR              # i.e. '/' on Linux and '\' on Windows
import ssl                                                  # Needed for SSL integration

HOSTNAME          = "0.0.0.0"
PORT              = 8000
BASE_DIR          = str(Path(__file__).parent.resolve())        # Current directory
HTDOCS_DIR        = BASE_DIR + DIRECTORY_SEPARATOR + "htdocs"   # "htdocs" directory path
READING_SIZE      = 1024*1024                                   # The maximum amount of bytes to read from a file in a single read() function call, set this to -1 to read until EOF
ALLOW_FILE_ACCESS = True                                        # If a file exists in the htdocs folder, should it be possible to access to it directly?
DIRECTORY_LISTING = True                                        # If set to True, this will allow people to have a simple interface to show files in a directory, if the index file of that directory does not exist 
INDEX_FILE_NAME   = "index.html"                                # Index file name, "index.html" by default, used when trying to access directories
CONSOLE_LOGGING   = True                                        # Choose whether to log stuff on the console or not
ENABLE_HTTPS      = False                                       # Choose whether to enable HTTPS on the server

# If ENABLE_HTTPS is True, please set these variables accordingly
HTTPS_PRIV_KEY    = BASE_DIR + DIRECTORY_SEPARATOR + "ssl" + DIRECTORY_SEPARATOR + "privkey.pem"
HTTPS_CERTIFICATE = BASE_DIR + DIRECTORY_SEPARATOR + "ssl" + DIRECTORY_SEPARATOR + "cert.pem"
SSL_PROTOCOL      = ssl.PROTOCOL_TLS_SERVER                     # Default protocol


# EDIT: Please don't change "error_handlers" and "urlpatterns" directly, use the decorators instead

# Tell the server which function to call when an error occurs
# Keep in mind there is a default behaviour to errors, it's not mandatory to override these methods
# This must contain a list of tuples (int, callable)
# Where "int" is the error code (expressed as an integer) and "callable" a callable object
# "callable" will be called when an error of code "int" occurs
error_handlers = [
]

# This must contain a list of tuples (str, callable)
# Where "str" is the path (expressed as a str object) and "callable" a callable object
# "callable" will be called when a request happens on the "str" path
urlpatterns = [
]


# Error codes - don't edit
ERROR_POST_NO_CONTENT_TYPE      = 0
ERROR_POST_PARSE_CONTENT_LENGTH = 1
ERROR_POST_NO_BOUNDARY          = 2
ERROR_POST_PARSE_JSON           = 3
ERROR_POST_EMPTY                = 4
ERROR_COOKIE_HEADERS_CLOSED     = 5
ERROR_COOKIE_CANNOT_CREATE      = 6