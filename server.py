import socket
from main import httpResponse
import json

PORT = 27015
IP = "0.0.0.0"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, )
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
        if line =="":
            break    
        
        if line and ": " in line:
            key,value = line.split(": ", 1)
            headers[key] = value
    
    
    body=""
    bodyData = data.splitlines()[-1]
    contentType = headers.get("Content-Type")
    
    if contentType == "application/x-www-form-urlencoded":
        body={}
        lines = bodyData.split("&")
        for line in lines:
            key, value = line.split("=")
            body[key] = value
            
    if contentType == "application/json":
        print(bodyData)
        try: 
            body = json.loads(bodyData)
        except json.JSONDecodeError:
            body = {"error": "Invalid JSON"}
            
             
        
    if isinstance(body, dict):
        if contentType == "application/x-www-form-urlencoded":
            body = "&".join([f"{key}={value}" for key, value in body.items()])
        elif contentType == "application/json":
            body = json.dumps(body)
        
    status_code = "200"
    status_message = "OK"        
    
    response = httpResponse(status_code, status_message, body, headers)
    print(response)
    print(response.encode())
    client.sendall(response.encode())
    
    client.close()
    
    