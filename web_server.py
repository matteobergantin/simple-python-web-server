from http.server import ThreadingHTTPServer
from abstract_web_server import AbstractWebServer
from pathlib import Path
from sys import exit
import settings, utils, cgi

class WebServer(AbstractWebServer):
    last_error = None
    def do_GET(self):
        self.execute_request()
    def do_POST(self):
        self.execute_request()

    def execute_request(self):
        # Removing the GET paramenters
        path_with_no_get_args = self.path.split('?')[0]

        # Checking if the path is mapped
        for path, callback in settings.urlpatterns:
            if path_with_no_get_args == path:
                print(f"Requested path {path_with_no_get_args} handled in function {callback.__name__} located in file {utils.getFunctionSourceFile(callback)}")
                callback(self)
                return None

        if len(path_with_no_get_args) == 0:
            # I don't even think this can happen...
            self.send_error_code(400, self.default400)
            return None

        # Creating a valid file path, not checking for escape sequences (like "..", "." ecc..)
        raw_file_path = utils.urldecode(path_with_no_get_args).replace("/", settings.DIRECTORY_SEPARATOR)

        # Escaping file path, this should be done automatically by HTTPServer / ThreadingHTTPServer
        relative_file_path = str(Path(raw_file_path))
        full_file_path = str(Path(settings.HTDOCS_DIR + settings.DIRECTORY_SEPARATOR + relative_file_path).absolute())

        if path_with_no_get_args[len(path_with_no_get_args)-1] == '/':
            # This is a directory, because the path ends with a '/'
            if utils.isdir(full_file_path):
                # This is a valid directory, check for an index file
                index_file_path = full_file_path + settings.DIRECTORY_SEPARATOR + settings.INDEX_FILE_NAME
                if utils.file_exists(index_file_path):
                    # index file exists, good
                    self.broadcast_file(index_file_path)
                else:
                    # index file does not exist, less good
                    self.send_error_code(404, self.default404)
            else:
                # Directory does not exist - 404
                self.send_error_code(404, self.default404)
            return None

        if utils.file_exists(full_file_path):
            # This is a file, broadcast it
            self.broadcast_file(full_file_path)
        else:
            # This is not a file
            if utils.isdir(full_file_path):
                # This is a directory, redirect
                self.redirect(self.path + "/")
            else:
                # This is NOT a directory NOR a file, therefore 404
                self.send_error_code(404, self.default404)

    def redirect(self, new_location: str):
        self.send_response(301)
        self.send_header('Location', new_location)
        self.end_headers()
    
    def send_error_code(self, code: int, default):
        for error_code, callback in settings.error_handlers:
            if error_code == code:
                print(f"Error {error_code} handled by function: {callback.__name__} located in file {utils.getFunctionSourceFile(callback)}")
                callback(self)
                return None
        default()

    def default404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        html_code = "<h1>404 - NOT FOUND</h1>"
        self.wfile.write(bytes(html_code, 'utf8'))
    
    def default400(self):
        self.send_response(400)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        html_code = "<h1>400 - BAD REQUEST</h1>"
        self.wfile.write(bytes(html_code, 'utf-8'))
    
    def default500(self):
        self.send_response(500)
        self.send_header("Content-Type", 'text/html')
        self.end_headers()
        html_code = "<h1>500 - INTERNAL SERVER ERROR</h1>"
        self.wfile.write(bytes(html_code, 'utf-8'))

    def default401(self):
        self.send_response(401)
        self.send_header("Content-Type", 'text/html')
        self.end_headers()
        html_code = "<h1>401 - UNAUTHORIZED</h1>"
        self.wfile.write(bytes(html_code, 'utf-8'))

    def broadcast_file(self, file_path: str):
        if not settings.ALLOW_FILE_ACCESS:
            # File access disabled
            self.send_error_code(401, self.default401)
            return None
        file_size = utils.filesize(file_path)
        if file_size == -1:
            # File does not exist or is inaccessible
            # We check if the file exists in the execute_request function
            # Therefore the file cannot be accessed
            print("ERROR: REQUESTED FILE DOES NOT EXIST OR CANNOT BE ACCESSED")
            print("--- FILE PATH: " + file_path)
            print("--- SERVER REQUEST PATH: " + self.path)
            self.send_error_code(500, self.default500)
            return None

        print("Reading file: " + file_path)
        self.send_response(200)
        headers = utils.findCorrectHeaders(file_path)
        for header_key, header_value in headers:
            self.send_header(header_key, header_value)
        self.end_headers()

        if file_size == 0:
            # Don't even open the file...
            print(f"Request {self.path} from {self.client_address[0]}: file empty, not opening it")
            return None

        with open(file_path, 'rb') as f:
            while True:
                bytesRead = f.read(settings.READING_SIZE)
                if bytesRead is None or len(bytesRead) == 0:
                    # EOF reached
                    break

                try:
                    self.wfile.write(bytesRead)
                except ConnectionResetError:
                    # Connection interrupted by user
                    print(f'ERROR ON REQUEST {self.path} FROM {self.client_address[0]}: CONNECTION INTERRUPTED BY USER')
                    break
        print(f'Finished reading file {file_path}')

    def parse_get_data(self):
        # GET requests are generally structured like this
        # url_path?get_parameter_key=get_parameter_value&another_get_parameter_key=another_get_parameter_value
        # ? = GET parameter, everything after ? is the GET request data
        # In this case we'll have a dict structured like this:
        # GET_DATA = {
        #       "get_parameter_key": "get_parameter_value",
        #       "another_get_parameter_key": "another_get_parameter_value"
        # }
        # All the data in the GET request will be url encoded

        question_mark_pos = self.path.find("?")
        if question_mark_pos == -1:
            # No GET data
            return {}
        return utils.decode_URL_encoded_data(self.path, question_mark_pos+1)

    def parse_post_data(self):
        # This returns a tuple of type (str, str)
        # The first string represents the Content-Type header
        # The second one represents the actual parsed data
        # If they're both None it means an error happened
        # You can check what kind of error by checking the last_error variable
        if self.headers['Content-Type'] is None:
            self.last_error = settings.ERROR_POST_NO_CONTENT_TYPE
            return (None, None)
        content_length = 0
        try:
            content_length = int(self.headers['Content-Length'])
        except ValueError:
            self.last_error = settings.ERROR_POST_PARSE_CONTENT_LENGTH
            return (None, None)
        content_type, opt_dict = cgi.parse_header(self.headers['Content-Type'])

        if content_type.lower() == 'multipart/form-data':
            try:
                opt_dict['boundary'] = bytes(opt_dict['boundary'], 'ascii')
            except KeyError:
                self.last_error = settings.ERROR_POST_NO_BOUNDARY
                return (None, None)
            raw_post_data = cgi.parse_multipart(self.rfile, opt_dict)

            # cgi.parse_multipart will return dict[str, list]
            # But we want a dict[str, obj] where obj IS NOT a list
            # This happens because if we send something like: {'foo': 'bar', 'foo': 'bar2'}
            # Response would be a dictioray like this:
            # {
            #   'foo': ['bar', 'bar2']
            # }
            # We don't want this, we just want to ignore any element but the last one
            # Again, I'm doing this because of how PHP on Apache implements it
            parsed_post_data = {}
            for post_key in raw_post_data.keys():
                if len(raw_post_data[post_key]) > 0:
                    parsed_post_data[post_key] = raw_post_data[post_key][len(raw_post_data[post_key])-1]
                else:
                    parsed_post_data[post_key] = True
            return (content_type.lower(), parsed_post_data)
        elif content_type.lower() == 'application/x-www-form-urlencoded':
            post_data = self.rfile.read(content_length).decode('ascii')
            if len(post_data) < 1:
                return (content_type.lower(), {})
            # Decoding URL encoded data
            return (content_type.lower(), utils.decode_URL_encoded_data(post_data, starting_index = 0))
        elif content_type.lower() == 'application/json':
            post_data = self.rfile.read(content_length).decode('ascii')
            json_data = utils.json_decode(post_data)
            if json_data is None:
                self.last_error = settings.ERROR_POST_PARSE_JSON
            return (content_type.lower(), json_data)
        elif content_type.lower() == 'text/plain':
            post_data = self.rfile.read(content_length).decode('ascii')
            return (content_type.lower(), post_data)
        self.last_error = settings.ERROR_POST_EMPTY
        return (None, None)

if __name__ == '__main__':
    if (not utils.exists(settings.HTDOCS_DIR) or not utils.isdir(settings.HTDOCS_DIR)) and settings.ALLOW_FILE_ACCESS:
        print('ERROR: No "htdocs" folder found, aborting...')
        exit(1)
    ws = ThreadingHTTPServer((settings.HOSTNAME, settings.PORT), WebServer)
    print(f"Web Server running on http://{settings.HOSTNAME}:{settings.PORT}/")
    try:
        ws.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down Web Server...")    
        ws.server_close()
    print("Goodbye!")
    