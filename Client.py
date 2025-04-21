import socket
import threading

# تنظیمات کلاینت
HOST = '127.0.0.1'
PORT = 12345

# ایجاد سوکت کلاینت
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    """دریافت پیام‌ها از سرور"""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("[ERROR] Connection to server lost.")
            client.close()
            break

def main():
    # شروع نخ برای دریافت پیام‌ها
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        # دریافت ورودی از کاربر
        message = input()
        if message == '/exit':
            client.send(message.encode('utf-8'))
            break
        elif message:
            client.send(message.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()
