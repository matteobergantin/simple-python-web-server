from http.server import BaseHTTPRequestHandler
from abc import ABC, abstractmethod

# This is an abstract class that we can import to views.py in order to use IntelliSense

class AbstractWebServer(BaseHTTPRequestHandler, ABC):
    last_error = None
    
    @abstractmethod
    def do_GET(self):
        pass
    @abstractmethod
    def do_POST(self):
        pass
    @abstractmethod
    def execute_request(self):
        pass
    @abstractmethod
    def redirect(self, new_location: str):
        pass
    @abstractmethod
    def send_error_code(self, code: int, default):
        pass
    @abstractmethod
    def default404(self):
        pass
    @abstractmethod
    def default400(self):
        pass
    @abstractmethod
    def default500(self):
        pass
    @abstractmethod
    def default401(self):
        pass
    @abstractmethod
    def broadcast_file(self, path: str):
        pass
    @abstractmethod
    def parse_get_data(self):
        pass
    @abstractmethod
    def parse_post_data(self):
        pass