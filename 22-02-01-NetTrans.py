import os
import json
import socket
import struct
import pyperclip
import time
import tkinter as tk
from tkinter import filedialog, messagebox


def input_file_path():
    window = tk.Tk()
    window.title('(^_^))')
    window.geometry('220x20')

    l = tk.Label(window, text='"Pls Select The File"')
    l.pack()

    inpath = filedialog.askopenfilename(parent=window,
                                        initialdir=os.getcwd(),
                                        title="Please select a file:",
                                        filetypes=[('all files', '.*')])

    return inpath


class NetworkServer:
    SERVER_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SERVER')
    if not os.path.exists(SERVER_FILE_PATH):
        os.makedirs(SERVER_FILE_PATH)

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def server_start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen(5)
        print("The Server has been started...")

        while True:
            print("Waiting for a connection...")
            conn, addr = sock.accept()
            print(f"Connection established and the address is from {addr}")

            while True:
                # 获取消息类型
                message_type = self.__recv_data(conn).decode('utf-8')
                if message_type == 'close':  # 四次挥手，空内容。
                    print("关闭连接")
                    break
                # 文件：{'msg_type':'file', 'file_name':"xxxx.xx" }
                # 消息：{'msg_type':'msg'}
                message_type_info = json.loads(message_type)
                if message_type_info['msg_type'] == 'msg':
                    data = self.__recv_data(conn)
                    pyperclip.copy(data.decode('utf-8'))

                else:
                    file_name = message_type_info['file_name']
                    print("接收到文件，要保存到：", file_name)
                    self.__recv_file(conn, file_name)


            conn.close()
        sock.close()

    @staticmethod
    def __recv_data(conn, chunk_size=1024):
        print("开始接收到消息...")
        # 获取头部信息：数据长度
        has_read_size = 0
        bytes_list = []
        print("接收报文头消息...")
        while has_read_size < 4:
            chunk = conn.recv(4 - has_read_size)
            has_read_size += len(chunk)
            bytes_list.append(chunk)
        header = b"".join(bytes_list)
        data_length = struct.unpack('i', header)[0]
        print("--------------------------------")
        print("接收报文头消息完成...")
        
        
        # 获取数据
        data_list = []
        has_read_data_size = 0
        print("接收报文消息...")
        print("--------------------------------")
        while has_read_data_size < data_length:
            size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
            chunk = conn.recv(size)
            data_list.append(chunk)
            has_read_data_size += len(chunk)

        data = b"".join(data_list)
        
        print(data.decode('utf-8'))
        print("--------------------------------")
        print("接收报文消息完毕...")
        return data


    def __recv_file(self, conn, save_file_name, chunk_size=1024):
        save_file_path = os.path.join(self.SERVER_FILE_PATH, save_file_name)
        # 获取头部信息：数据长度
        has_read_size = 0
        bytes_list = []
        while has_read_size < 4:
            chunk = conn.recv(4 - has_read_size)
            bytes_list.append(chunk)
            has_read_size += len(chunk)
        header = b"".join(bytes_list)
        data_length = struct.unpack('i', header)[0]

        # 获取数据
        file_object = open(save_file_path, mode='wb')
        has_read_data_size = 0
        print("File receive started...")
        while has_read_data_size < data_length:
            size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
            chunk = conn.recv(size)
            file_object.write(chunk)
            file_object.flush()
            has_read_data_size += len(chunk)

            percent = round((int(has_read_data_size) / int(data_length)) * 100, 3)
            # time.sleep(0.0001)
            print("\r文件总大小为：{}字节，已下载{}字节, 进度{}%".format(data_length, has_read_data_size, percent), end="")
        file_object.close()
        print("\nFile receive finished...")


class NetworkClient:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    @staticmethod
    def __send_data(conn, content):
        data = content.encode('utf-8')
        header = struct.pack('i', len(data))
        conn.sendall(header)
        conn.sendall(data)


    @staticmethod
    def __send_data_file(conn, file_path):
        file_size = os.stat(file_path).st_size
        header = struct.pack('i', file_size)
        conn.sendall(header)

        has_send_size = 0
        file_object = open(file_path, mode='rb')
        print("File sent started...")
        while has_send_size < file_size:
            chunk = file_object.read(2048)
            conn.sendall(chunk)
            has_send_size += len(chunk)

            percent = round((int(has_send_size) / int(file_size)) * 100, 3)
            # time.sleep(0.0001)
            print("\r文件总大小为：{}字节，已发送{}字节, 进度{}%".format(file_size, has_send_size, percent), end="")

        file_object.close()
        print("\nFile sent finished...")


    def send_text(self):
        client = socket.socket()
        client.connect((self.ip, self.port))

        data = pyperclip.paste()
        print("发送报文头信息...")
        self.__send_data(client, json.dumps({"msg_type": "msg"}))
        print("发送文本信息...")
        self.__send_data(client, data)
        print(data)
        client.close()
        print("发送信息完成...")


    def send_file(self):
        file_path = input_file_path()
        # file_name = file_path.rsplit(os.sep, maxsplit=1)[-1]
        file_name = file_path.rsplit('/', maxsplit=1)[-1]

        client = socket.socket()
        client.connect((self.ip, self.port))

        self.__send_data(client, json.dumps({"msg_type": "file", 'file_name': file_name}))
        self.__send_data_file(client, file_path)

        client.close()




# ######################## Server Side #########################
# from NetTrans import NetworkServer
# server = NetworkServer('127.0.0.1', 12345)
# server.server_start()

# ######################## Client Side #########################
# from NetTrans import NetworkClient

# client = NetworkClient('127.0.0.1', 12345)
# client.send_text()
# client.send_file()


