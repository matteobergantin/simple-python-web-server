from http.server import ThreadingHTTPServer
from web_server import WebServer, setSettingsModule
from sys import exit
import settings
import utils

if __name__ == '__main__':
    setSettingsModule(settings)
    if (not utils.exists(settings.HTDOCS_DIR) or not utils.isdir(settings.HTDOCS_DIR)) and settings.ALLOW_FILE_ACCESS:
        if settings.CONSOLE_LOGGING:
            print('ERROR: No "htdocs" folder found, aborting...')
        exit(1)
    ws = ThreadingHTTPServer((settings.HOSTNAME, settings.PORT), WebServer)
    ws_url = f"http://{settings.HOSTNAME}"
    if settings.PORT != 80:
        ws_url += f":{settings.PORT}"
    ws_url += '/'
    if settings.CONSOLE_LOGGING:
        print(f"Web Server running on {ws_url}")
    try:
        ws.serve_forever()
    except KeyboardInterrupt:
        if settings.CONSOLE_LOGGING:
            print("Shutting down Web Server...")    
        ws.server_close()
    if settings.CONSOLE_LOGGING:
        print("Goodbye!")