def generateRequest(method = "GET", host = "localhost"):
    return f"{method} / HTTP/1.1\r\nHost: {host}"
    
def httpResponse(status_code, status_message, body, headers={}):
    response = f"HTTP/1.1 {status_code} {status_message}\r\n"
    default_headers = {"Content-Type": "text/plain"}
    headers = {**default_headers, **headers}

    body_bytes = body.encode('utf-8')
    content_length = len(body_bytes)

    for key, value in headers.items():
        response += f"{key}: {value}\r\n"

    if "Content-Length" not in headers:
        response += f"Content-Length: {content_length}\r\n"

    response += "\r\n"
    response += body

    return response
