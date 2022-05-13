from abstract_web_server import AbstractWebServer

def sayHello(ws: AbstractWebServer):
    ws.send_response(200)
    ws.send_header('Content-Type', 'text/plain')
    ws.end_headers()
    ws.wfile.write(bytes("Hello, World!", 'utf-8'))

def sayGoodbye(ws: AbstractWebServer):
    ws.send_response(200)
    ws.send_header('Content-Type', 'text/plain')
    ws.end_headers()
    ws.wfile.write(bytes("Goodbye, World!", 'utf-8'))

def print_request_data(ws: AbstractWebServer):
    ws.send_response(200)
    ws.send_header('Content-Type', 'text/plain')
    ws.end_headers()
    get_data = ws.parse_get_data()
    post_content_type, post_data = ws.parse_post_data()
    ws.wfile.write(bytes("OK", 'utf-8'))
    print(f"GET DATA  = {get_data}")
    print(f"POST DATA = {post_data} ENCODED AS {post_content_type}")

def handle401(ws: AbstractWebServer):
    ws.send_response(401)                           # We can also override the response code, if we want
    ws.send_header('Content-Type', 'text/plain')
    ws.end_headers()
    ws.wfile.write(bytes("This is what happens when we get a 401 error code", 'utf-8'))

def send401(ws: AbstractWebServer):
    ws.send_error_code(500, ws.default500)          # ws.default500 is the function to call if there is no callback function defined in error_handlers