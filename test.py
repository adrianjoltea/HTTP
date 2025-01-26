import socket
import subprocess
import time
import pytest

HOST = "localhost"
PORT = 27015

@pytest.fixture(scope="module")
def server():
    """Start the server as a subprocess and stop it after tests."""
    server_process = subprocess.Popen(["python", "server.py"])
    time.sleep(1)  
    yield
    server_process.terminate()
    server_process.wait()


def send_request(request):
    """Helper function to send a request to the server and get the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(request.encode())
        response = client.recv(4096).decode()
    return response


def test_application_json(server):
    """Test JSON content-type payload."""
    request = (
        "POST / HTTP/1.1\r\n"
        "Host: localhost:27015\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 36\r\n\r\n"
        '{"key1": "value1", "key2": "value2"}'
    )
    response = send_request(request)

    assert "200 OK" in response
    assert "Content-Type: application/json" in response
    assert '{"key1": "value1", "key2": "value2"}' in response

    
def test_urlencoded(server):
    """Test JSON content-type payload."""
    request = (
        "POST / HTTP/1.1\r\n"
        "Host: localhost:27015\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 23\r\n\r\n"
        "key1=value1&key2=value2"
    )
    response = send_request(request)

    assert "200 OK" in response
    assert "Content-Type: application/x-www-form-urlencoded" in response
    assert "key1=value1&key2=value2" in response