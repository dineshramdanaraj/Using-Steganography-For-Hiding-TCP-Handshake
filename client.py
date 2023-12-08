import socket
import threading
import os
import re
import math
import time

def send_data(server_address, id,  message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    id = id

    try:
        client_socket.send(message.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Response from {server_address}: {response}")
        respons1 = client_socket.recv(1024).decode()
        #print(respons1)
        time.sleep(3)
        perform_ftp(client_socket, id, respons1)  # Perform FTP operations after connection

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()



def perform_ftp(client, id, instruction):
    connection = True
    id = str(id)
 
    while connection:
       
        a = input(instruction)
        up = re.match("\Aupload", a)
        down = re.match("\Aget", a)
        if up or down:
            client.send(a.encode())
            if up:

                client.send("up".encode())
                x = re.findall("<.+>$", a)
                upload = open(x[-1][1:-1], "rb")
                size = os.path.getsize(x[-1][1:-1])
                print(size)
                client.send(str(size).encode())
                client.send(id.encode())
                data0 = upload.read(1024)
                while data0:
                    client.send(data0)
                    data0 = upload.read(1024)

                print("File sent")
                upload.close()
                client.recv(64).decode()
                print("File successfully uploaded")
            elif down:
                print("Started Downloading")
                client.send("down".encode())
                x = re.findall("<.+>$", a)
                file_tup = os.path.splitext(x[0][1:-1])
                name = "new_dl"+file_tup[0]+f'{str(id)}'+file_tup[1]
                download_file = open(name, "wb")
                file_writer = b""
                x = False

                print("PROCESSING")
                size = client.recv(1024).decode()
                size = int(size)
                lim = math.ceil(size/1024)
                for i in range(lim):
                    rec = client.recv(1024)
                    file_writer += rec
                print("writing")
                download_file.write(file_writer)
                print("Finished Downloading")
                download_file.close()
        code1 = input("For termination of connection Enter 'Y'")
        client.send(code1.encode())
        if code1 =="Y":
            connection = False
        else:
            continue


if __name__ == "__main__":
    # Server addresses
    id = 9090
    normal_server_address = ('localhost', id)
     # Message to be sent to servers
    message = "Hello, servers! This is a message from the client."

    # Connect to the servers and perform FTP operations
    try:
        thread_normal = threading.Thread(target=send_data, args=(normal_server_address, id, message))
        thread_normal.start()


    except KeyboardInterrupt:
        print("Client shutting down...")