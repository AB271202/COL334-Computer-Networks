import socket
import threading


IP=socket.gethostbyname(socket.gethostname())
PORT=5566
ADDR=(IP, PORT)
SIZE=1024
FORMAT='utf-8'
DISCONNECT_MSG="!DISCONNECT"

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg=conn.recv(SIZE).decode(FORMAT)
        if msg==DISCONNECT_MSG:
            connected=False
        
        print(f"[{addr}] {msg}")
        msg=f"Msg received: {msg}"
        conn.send(msg.encode(FORMAT))
    conn.close()


def main():
    print("[STARTING] Starting server")
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Listening on port {IP}:{PORT}")
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(args=(conn,addr), target=handle_client)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

if __name__=="__main__":
    main()