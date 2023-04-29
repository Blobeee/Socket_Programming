import socket
import threading


#아래의 함수들에 필요한 정보들인데, 포트나 주소같은것들은 그때그떄 변할수 있는 값들이기 때문에 수정하기 쉽게 먼저 선언함.
IP = socket.gethostbyname(socket.gethostname())
PORT = 1998
ADDR = (IP, PORT)
SIZE = 1003
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT"


#소켓을 여는데 필요한 메인 함수임
def main():
    print("[STARTING] Server is starting")
    #(IPv4,TCP)프로토콜로 소켓을 만듬
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #IP와 PORT를 바인드해줌
    server.bind(ADDR)
    #서버를 열어놓고 클라이언트의 요청을 기다림(클라이언트 코드에서는 필요 없음)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    #DISCONNECT를 입력하기 전까지는 소켓을 유지함
    while (True):
        #클라이언트의 요청이 있으면 새로운 conn소켓을 생성함. 이때 addr에 클라이언트의 IP와 PORT 정보가 저장되어있음
        conn, addr = server.accept()
        #쓰레드를 사용하여 병렬적으로 hanle_client 함수를 사용할수 있게 해줌 이떄 args 는 함수에 입력될 정보임
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        #병렬적인 함수실행중
        thread.start()
        #연결된 클라이언트의 수를 나타내는데, -1을 해주는 이유는 main함수 자체도 thread로 실행되기 때문.
        print(f"[ACTIVE CONNETIONS] {threading.activeCount() -1}")



#쓰레드를 통해서 반복적으로 소켓을 생성해줄 함수임 conn에 소켓 정보가 들어있고, addr에 주소정보가 들어있음.
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    #DISCONNECT 를 입력하기 전에는 무한루프 돌릴꺼임 >> 채팅프로그램 계속됨
    connected = True
    while connected :
        #conn소켓을 통해 수신할 데이터의 크기는 SIZE 이고, 코딩 방식은 FORMAT임
        msg = conn.recv(SIZE).decode(FORMAT)
        #DISCONNECT 입력하면 루프 멈추고 conn.close()실행됨
        if (msg == DISCONNECT_MSG):
            connected = False
        #addr은 main함수에서 받았다시피 클라이언트에 대한 주소정보가 들어있음. ip, port 주소 말고 보기쉽게 닉넴으로 마렵네.
        print(f"[{addr}] : {msg}")
        msg = f"Msg received : {msg}"
        conn.send(msg.encode(FORMAT))

    conn.close()



if __name__ == "__main__":
    main()
 