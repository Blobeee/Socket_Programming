import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 1998
ADDR = (IP, PORT)
SIZE = 1003
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    #서버에 보낼 메세지를 input을 통해 받고, DISCONNECT를 입력하면 서버의 handle_client함수에서 서버를 종료시킴
    while connected :
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if (msg == DISCONNECT_MSG):
            connected = False
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
        

if __name__ == "__main__":
    main()

    #hello
    