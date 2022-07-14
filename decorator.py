from settings import error_handlers, urlpatterns

def WebServerPath(path: str):
    def __inner(callable):
        global urlpatterns
        urlpatterns.append((path, callable))
    return __inner

def WebServerErrorHandler(error_code: int):
    def __inner(callable):
        global error_handlers
        error_handlers.append((error_code, callable))
    return __inner