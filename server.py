import socket
import threading

# تنظیمات سرور
HOST = '127.0.0.1'  # localhost
PORT = 12345

# لیست کلاینت‌های متصل
clients = []
client_ips = {}

def broadcast(message, sender_socket=None):
    """ارسال پیام به تمام کلاینت‌ها به جز فرستنده"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, addr):
    """مدیریت ارتباط با یک کلاینت"""
    print(f"[NEW CONNECTION] Client {addr} connected.")
    
    # ثبت IP کلاینت
    client_ips[client_socket] = addr[0]
    
    while True:
        try:
            # دریافت پیام از کلاینت
            message = client_socket.recv(1024).decode('utf-8')
            
            if message == '/exit':
                print(f"[DISCONNECTED] Client {addr} disconnected.")
                clients.remove(client_socket)
                client_socket.close()
                broadcast(f"Client {addr[0]} has left the chat.".encode('utf-8'))
                break
            elif message:
                # اضافه کردن IP کلاینت به پیام
                formatted_message = f"{addr[0]}: {message}".encode('utf-8')
                print(f"[MESSAGE] {formatted_message.decode('utf-8')}")
                broadcast(formatted_message)
        except:
            print(f"[ERROR] Client {addr} disconnected unexpectedly.")
            clients.remove(client_socket)
            client_socket.close()
            broadcast(f"Client {addr[0]} has left the chat.".encode('utf-8'))
            break

def main():
    # ایجاد سوکت سرور
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        # پذیرش اتصال جدید
        client_socket, addr = server.accept()
        clients.append(client_socket)
        
        # ایجاد نخ برای مدیریت کلاینت
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
