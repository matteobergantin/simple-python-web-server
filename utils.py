from urllib.parse import unquote as urldecode, quote as urlencode
from os.path import exists, isdir, isfile, basename
from inspect import getsourcefile
from pathlib import Path
import math
import json

def json_decode(data: str):
    result = None
    try:
        result = json.loads(data)
    except (json.decoder.JSONDecodeError, TypeError):
        # None is the value that identifies and error
        pass
    return result

def json_encode(data: dict):
    result = None
    try:
        result = json.dumps(data)
    except TypeError:
        # None is the value that identifies and error
        pass
    return result

def file_exists(path: str):
    return exists(path) and not isdir(path)

def dir_exists(path: str):
    return exists(path) and not isfile(path)

def getFileExt(path: str):
    file_name = basename(path)
    i = len(file_name) - 1
    while i >= 0:
        if file_name[i] == '.':
            return file_name[i:]
        i -= 1
    return file_name

def findCorrectHeaders(path: str):
    # Finding the correct headers based on the file extension
    full_path = str(Path(path).absolute().resolve())
    filename = basename(full_path)
    ext = getFileExt(filename)
    headers = []
    if ext in ['.html', '.css']:
        headers.append(("Content-Type", f"text/{ext[1:]}"))
    elif ext == '.txt':
        # The MIME type text/txt does not exist
        headers.append(("Content-Type", "text/plain"))
    elif ext in ['.js', '.map']:
        headers.append(("Content-Type", "application/javascript"))
    elif ext in ['.mp4', '.ogg', '.mpeg', '.webm']:
        headers.append(("Content-Type", f"video/{ext[1:]}"))
    elif ext == '.avi':
        # The MIME type video/avi does not exist
        headers.append(("Content-Type", 'video/x-msvideo'))
    elif ext == '.ts':
        # The MIME type video/ts does not exist
        headers.append(("Content-Type", 'video/mp2t'))
    elif ext in ['.gif', '.png', '.webp', '.jpeg', '.bmp', '.tiff']:
        headers.append(("Content-Type", f"image/{ext[1:]}"))
    elif ext == '.jpg':
        # The MIME type image/jpg does not exist 
        headers.append(("Content-Type", "image/jpeg"))
    elif ext == '.svg':
        # The MIME type image/svg does not exist
        headers.append(("Content-Type", "image/svg+xml"))
    elif ext == '.ico':
        # The MIME type image/ico does not exist
        headers.append(("Content-Type", "image/x-icon"))
    elif ext == '.xhtml':
        headers.append(("Content-Type", 'application/xhtml+xml'))
    else:
        # Unknown file ext, send it as a raw binary stream
        headers.append(("Content-Type", "application/octet-stream"))
        headers.append(("Content-Disposition", f"attachment; filename={filename}"))
    # Appending file size
    file_size = filesize(path)
    if file_size == -1:
        headers.append(('Content-Length', '0'))
    else:
        headers.append(('Content-Length', str(file_size)))
    return headers

def filesize(path: str):
    file_size = 0
    try:
        file_size = Path(path).stat().st_size
    except OSError:
        # File does not exist or is inaccessible
        file_size = -1
    return file_size

def getFunctionSourceFile(callable):
    result = ""
    try:
        result = getsourcefile(callable)
    except TypeError:
        result = "BUILT-IN FUNCTION"
    except Exception as ex:
        result = f"ERROR OCCURED WHILE LOCATING FUNCTION {callable.__name__}\nERROR INFO:\n{str(ex)}"
    return result

def decode_URL_encoded_data(path: str, starting_index: int):
    if starting_index >= len(path):
        return {}
    url_decoded_data = {}
    raw_data = path[starting_index:].split("&")
    for raw_element in raw_data:
        if raw_element == "":
            # Ignore empty strings
            # This happens if someone requests things like /path?a=b&&c=d
            continue
        equal_sign_index = raw_element.find('=')
        if equal_sign_index == -1:
            # No equal sign found, the value will be set to an empty string
            url_decoded_data[urldecode(raw_element)] = ""
        else:
            # At least on equal sign specified, setting the correct value
            # If we have multiple equal signs we care only about the first one
            # (That's how it's implemented in Apache)
            url_decoded_data[urldecode(raw_element[:equal_sign_index])] = urldecode(raw_element[equal_sign_index+1:])
    return url_decoded_data

def parseFileSize(file_size: int, normalize: int = 2):
    if file_size < 0:
        return "NaN"
    dims = ['bytes', 'KiB', 'MiB', 'GiB']
    size_scale_factor = 1000
    i = 0
    while i < len(dims) and file_size >= size_scale_factor:
        file_size /= 1024
        i += 1
    file_size = math.floor(file_size * (10**normalize)) / (10**normalize)
    return f"{file_size} {dims[i]}"