import socket
from main import httpResponse

PORT = 27015
IP = "0.0.0.0"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

server.listen(5)

while True:
    client,addr = server.accept()
    data = b""
    
    while True:
        chunk = client.recv(1024)
        data += chunk
        if len(chunk) < 1024:
            break

    data = data.decode()  
    
    
    requestLine = data.splitlines()[0]
    method, path, version = requestLine.split(" ")
    
    headers = {}
    for line in data.splitlines()[1:]:
        if line and ": " in line:
            key,value = line.split(": ", 1)
            headers[key] = value
    
    print("PATH:", path)
    
    body=""
    contentType = headers.get("Content-Type")
    if contentType == "application/x-www-form-urlencoded":
        body={}
        lines = data.splitlines()[-1].split("&")
        for line in lines:
            key, value = line.split("=")
            body[key] = value
    
    if isinstance(body, dict):
        body = "&".join([f"{key}={value}" for key, value in body.items()])
        
    print(httpResponse(method, body, headers))
    
    client.sendall(httpResponse(200, "Hello World", headers).encode())
    
    client.close()
    
    