from http.server import ThreadingHTTPServer
from web_server import WebServer, defineSettingsModule
from sys import exit
import settings
import includes
import utils
import ssl

if __name__ == '__main__':
    defineSettingsModule(settings)
    if (not utils.exists(settings.HTDOCS_DIR) or not utils.isdir(settings.HTDOCS_DIR)) and settings.ALLOW_FILE_ACCESS:
        if settings.CONSOLE_LOGGING:
            print('ERROR: No "htdocs" folder found, aborting...')
        exit(1)
    ws = ThreadingHTTPServer((settings.HOSTNAME, settings.PORT), WebServer)
    ws_url = f"http{'s' if settings.ENABLE_HTTPS else ''}://{settings.HOSTNAME}"
    if (not settings.ENABLE_HTTPS and settings.PORT != 80) or (settings.ENABLE_HTTPS and settings.PORT != 443):
        ws_url += f":{settings.PORT}"
    ws_url += '/'

    if settings.ENABLE_HTTPS:
        sslctx = ssl.SSLContext(settings.SSL_PROTOCOL)
        sslctx.load_cert_chain(certfile=settings.HTTPS_CERTIFICATE, keyfile=settings.HTTPS_PRIV_KEY)
        ws.socket = sslctx.wrap_socket(ws.socket)

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