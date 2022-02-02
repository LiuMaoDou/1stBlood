import contextlib
import os
import socket
import struct
import time
import tkinter as tk
from tkinter import filedialog


def input_file_path():
    window = tk.Tk()
    window.title('(^_^))')
    window.geometry('220x20')

    l = tk.Label(window, text='"Pls Select The File"')
    l.pack()

    inpath = filedialog.askopenfilename(parent=window,
                                        initialdir=os.path.abspath(__file__),
                                        title="Please select a file:",
                                        filetypes=[('all files', '.*')])

    window.destroy()
    return inpath


def input_file_path_directory():
    window = tk.Tk()
    window.title('(^_^))')
    window.geometry('220x20')

    l = tk.Label(window, text='"Pls Select The File"')
    l.pack()

    inpath = filedialog.askdirectory(title="select")

    window.destroy()
    return inpath


class NetworkClient:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = None

    @contextlib.contextmanager
    def connect_server(self):
        """
        上下文管理函数
        作用: 连接,断开Server
        :return:
        """

        print(f"--> 开始连接Server, IP:{self.server_ip}, Port:{self.server_port}...")
        self.client = socket.socket()
        self.client.connect((self.server_ip, self.server_port))
        yield self.client
        self.__send_data(self.client, 'close')
        self.client.close()
        print(f"--> 断开连接Server, IP:{self.server_ip}, Port:{self.server_port}...")
        return

    def register(self):
        with self.connect_server() as client_r:
            while True:
                username = input("--> 请输入要注册的用户名(如果要退出请输入Q/q): ")
                if username.upper() == 'Q':
                    break

                pwd = input("--> 请输入要注册的密码: ")

                if username == "" or pwd == "":
                    print('--> 请输入正确的用户名和密码, 不要直接回车')
                    continue

                dic = {'username': username, 'pwd': pwd}

                content = f'register|{dic}'
                self.__send_data(client_r, content)
                result = self.__recv_data(client_r).decode('utf-8')
                print(result)

    def login(self):
        menu_login = """--> 请选择要使用的功能...
--> [3]输入'3'上传文件...
--> [4]输入'4'下载文件..
--> [ls]输入'ls'查看文件信息..
--> [q/Q] 输入'Q/q'退出程序...
--> 请输入: """

        with self.connect_server() as client_l:
            while True:
                username = input("--> 请输入要登录的用户名(如果要退出请输入Q/q): ")
                if username.upper() == 'Q':
                    break

                pwd = input("--> 请输入要登录的密码: ")

                if username == "" or pwd == "":
                    print('--> 请输入正确的用户名和密码, 不要直接回车')
                    continue

                dic = {'username': username, 'pwd': pwd}
                content = f'login|{dic}'
                self.__send_data(client_l, content)
                result = self.__recv_data(client_l).decode('utf-8')

                if result == '用户认证失败':
                    print('--> 用户登录失败, 请重新登录...')
                    continue

                if result == '用户认证成功':
                    print('--> 用户登录成功, 可以开始使用网盘...')
                    while True:
                        input_result_login = input(menu_login)

                        if input_result_login.upper() == "Q":
                            print("--> 退出登录, 欢迎再次使用...")
                            self.__send_data(client_l, "Q")
                            return

                        if input_result_login == '3':

                            while True:
                                input_upload = input('--> 请选择要上传的文件, 按任意键开始(注意弹窗) (如果要退出请按Q/q)...')
                                if input_upload.upper() == "Q":
                                    print("--> 退出上传, 欢迎再次使用...")
                                    break

                                self.__send_data(client_l, 'upload_file')
                                self.__upload_file(client_l)

                        if input_result_login == '4':

                            while True:
                                input_download_file = input('\n--> 请输入要下载的文件名(如果要退出请按Q/q): ')
                                if input_download_file.upper() == "Q":
                                    print("--> 退出上传, 欢迎再次使用...")
                                    break

                                if input_download_file == "":
                                    print('--> 文件名不能为空, 请重新输入')
                                    continue

                                input('--> 请选择本地文件夹保存文件(注意弹窗), 按任意键继续...')
                                download_dir = input_file_path_directory()

                                self.__send_data(client_l, 'download_file')


                                down_load_file = os.path.join(download_dir, input_download_file)
                                if os.path.exists(down_load_file):
                                    xc_input = input('--> 本地已经存在文件, 续传请输入1, 覆盖请输入2: ')

                                    if xc_input == "1":
                                        file_size = os.stat(down_load_file).st_size
                                        input_download_file_xc = f'{file_size}|{input_download_file}'
                                        self.__send_data(client_l, input_download_file_xc)
                                        xc_result = self.__recv_data(client_l).decode('utf-8')

                                        if xc_result == '文件一样大, 不需要续传':
                                            print(xc_result)

                                        else:
                                            print("--> 开始续传...")
                                            self.__recv_file(client_l, down_load_file)
                                    else:
                                        os.remove(down_load_file)
                                        input_download_file_xc = f'0|{input_download_file}'
                                        self.__send_data(client_l, input_download_file_xc)
                                        self.__recv_data(client_l).decode('utf-8')
                                        self.__recv_file(client_l, down_load_file)
                                else:
                                    input_download_file_xc = f'0|{input_download_file}'
                                    self.__send_data(client_l, input_download_file_xc)
                                    self.__recv_data(client_l).decode('utf-8')
                                    self.__recv_file(client_l, down_load_file)

                        if input_result_login == 'ls':
                            self.__send_data(client_l, input_result_login)
                            print('--> 用户文件如下...')
                            print('------------------')
                            print(self.__recv_data(client_l).decode('utf-8'))
                            print('------------------')
                            input('--> 请按任意键继续...')


    @staticmethod
    def __send_data(conn, content):
        data = content.encode('utf-8')
        header = struct.pack('i', len(data))
        conn.sendall(header)
        conn.sendall(data)

    @staticmethod
    def __recv_data(conn, chunk_size=1024):
        has_read_size = 0
        bytes_list = []

        while has_read_size < 4:
            chunk = conn.recv(4 - has_read_size)
            has_read_size += len(chunk)
            bytes_list.append(chunk)
        header = b"".join(bytes_list)
        data_length = struct.unpack('i', header)[0]

        # 获取数据
        data_list = []
        has_read_data_size = 0

        while has_read_data_size < data_length:
            size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
            chunk = conn.recv(size)
            data_list.append(chunk)
            has_read_data_size += len(chunk)

        data = b"".join(data_list)
        return data

    @staticmethod
    def __recv_file(conn, save_file_path, chunk_size=1024):
        has_read_size = 0
        bytes_list = []
        while has_read_size < 4:
            chunk = conn.recv(4 - has_read_size)
            bytes_list.append(chunk)
            has_read_size += len(chunk)
        header = b"".join(bytes_list)
        data_length = struct.unpack('i', header)[0]

        # 获取数据
        file_object = open(save_file_path, mode='ab')
        has_read_data_size = 0
        while has_read_data_size < data_length:
            size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
            chunk = conn.recv(size)
            file_object.write(chunk)
            file_object.flush()
            has_read_data_size += len(chunk)

            time.sleep(0.0001)
            percent = round((int(has_read_data_size) / int(data_length)) * 100, 3)
            percent_bar = "▋" * int(round(percent / 10, 0))
            print("\r文件总大小为：{}字节，已下载{}字节, 进度{}%: {}".format(data_length, has_read_data_size, percent, percent_bar),
                  end="")
        file_object.close()

    def __upload_file(self, conn):
        file_path = input_file_path()
        file_name = file_path.rsplit('/', maxsplit=1)[-1]

        self.__send_data(conn, file_name)

        print("--> 发送文件信息...")
        print("--------------------------------")
        self.__send_data_file(conn, file_path)
        print("\n--------------------------------")
        print("--> 发送文件完成...")

    @staticmethod
    def __send_data_file(conn, file_path):
        file_size = os.stat(file_path).st_size
        header = struct.pack('i', file_size)
        conn.sendall(header)

        has_send_size = 0
        file_object = open(file_path, mode='rb')
        while has_send_size < file_size:
            chunk = file_object.read(2048)
            conn.sendall(chunk)
            has_send_size += len(chunk)
            time.sleep(0.0001)
            percent = round((int(has_send_size) / int(file_size)) * 100, 3)
            percent_bar = "▋" * int(round(percent / 10, 0))
            print("\r文件总大小为：{}字节，已发送{}字节, 进度{}%: {}".format(file_size, has_send_size, percent, percent_bar), end="")

        file_object.close()


if __name__ == "__main__":
    # IP和端口可以根据实际情况输入
    client = NetworkClient('127.0.0.1', 50000)
    menu = """--> 请选择要使用的功能...
--> [1] 输入'1'注册用户...
--> [2] 输入'2'登录用户...
--> [q/Q] 输入'Q/q'退出程序...
--> 请输入: """

    while True:
        input_result = input(menu)
        if input_result.upper() == "Q":
            print("--> 程序结束, 欢迎再次使用...")
            break

        if input_result == '1':
            client.register()

        if input_result == '2':
            client.login()
