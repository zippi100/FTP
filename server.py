from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep
import os, sys

program_name = sys.argv[0]
arguement = sys.argv[1:]
count = len(arguement)

connection_port = int(sys.argv[1])
data_port = connection_port - 1
server_host = "localhost"




def main():
    server_socket = create_server_socket()
    server_socket.listen(5)

    print "server waiting for connection"

    connection_socket, client_address = server_socket.accept()

    while True:

        print "server waiting for data"
        # Keeps track of command requested
        command = connection_socket.recv(20)
        command = command.split()
        print("received command")
        data_socket = create_data_socket()
        data_socket.listen(5)
        if command[0] == "ls":
            print("Read in ls")
            data = ls()
            print(len(data))
            s, a = data_socket.accept()
            s.send(str(len(data)))
	    sleep(0.005)
            send_file(data, s)
	    data_socket.close()
	    s.close()
	    sleep(0.05)
        elif command[0] != "ls":
            s, a = data_socket.accept()
            sleep(0.005)
            if command[0] == "get":
                sleep(0.005)
                data = prepare_file(command[1], s)
                send_file(data, s)
                sleep(0.005)
            elif command[0] == "put":

                data_length = receive_data_length(s)
                data = receive_data(s, data_length)
                print("finished receive")
                write_file(data, command[1])
            print data
            data_socket.close()
            s.close()
            sleep(0.005)

    connection_socket.close()


# Create a server socket for client connection.
def create_server_socket():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((server_host, connection_port))
    return server_socket


# Create a data socket for sending data to and from client.
def create_data_socket():
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    data_socket.bind((server_host, data_port))
    return data_socket


# Receive length of data from client.
def receive_data_length(socket):
    data_length = ""
    data_length += socket.recv(255)
    # data_length = int(data_length)
    return data_length


def receive_data(socket, data_length):
    tmpbuffer = ""
    data = ""

    print("in data length")
    print(data_length)
    while len(data) < float(data_length):
        tmpbuffer = socket.recv(3000)  # Receive 3000 bytes at a time. NEED TO MAKE THIS BIGGER RECEIVE SO IT DOES NOT
        data += tmpbuffer  # THAT IT DOES NOT TAKE TOO LONG FOR BIG FILES
        print("receiving...")
    print("done")
    return data


# Get all the data in the file.
def prepare_file(filename, data_socket):
    file_size = os.stat(filename)
    data_length = file_size.st_size
    data_socket.send(str(file_size.st_size))
    sleep(0.005)
    tmpbuffer = ""
    data = ""
    f = open(filename, "r")
    tmpbuffer = f.readline()

    while tmpbuffer:
        data += tmpbuffer
        tmpbuffer = f.readline()
    return data


# Send the file through the data_socket
def send_file(data, data_socket):
    data_sent = 0
    while data_sent != len(data):
        data_sent += data_socket.send(data[data_sent])


# Gets length of file.
def get_file_length(filename):
    filesize = os.stat(filename)
    return filesize


def write_file(data, filename):
    # buffer = "" #This variable checks for when all data has been written.
    print("writing to file")
    f = open(filename, "w+")
    f.write(data)
    f.close()


def ls():
    data = ""
    dirs = os.listdir(os.curdir)
    for file in dirs:
        data += (file + "\n")
    return data


if __name__ == "__main__":
    main()
