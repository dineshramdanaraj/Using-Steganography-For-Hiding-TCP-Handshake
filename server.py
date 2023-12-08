import socket
import os
import re
import threading
import time
import struct
import random
import math

def create_tcp_segment(source_port, dest_port, seq_number, ack_number, flags, window_size, data):
    tcp_header = struct.pack('!HHIIBBHHH', source_port, dest_port, seq_number, ack_number, 5 << 4, flags, window_size, 0, 0)
    checksum = calculate_checksum(tcp_header + data)
    tcp_segment = struct.pack('!HHIIBBHHH', source_port, dest_port, seq_number, ack_number, 5 << 4, flags, window_size, checksum, 0) + data
    return tcp_segment

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + (data[i + 1])
        checksum += w

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = ~checksum & 0xffff
    return checksum



def process_ftp(con_soc, addr):
    try:
        print(f'client number:{addr} connected')
        serv = True
       
        while serv:
            msg = 'Enter upload command with filename for uploading file \n Choose get command with filename for downloading File \n ex: get <filename> or upload <filename>\n'
            try:
                con_soc.send(msg.encode())
                code = con_soc.recv(1024).decode()
            except:
                print("Connection Terminated")

            try:
                func = con_soc.recv(63).decode()
            except:
                print("Client has not requested any file transfer")

            try:
                if func == "up":
                    try:
                        size1 = con_soc.recv(1024).decode()
                        id = con_soc.recv(64).decode()
                    except:
                        break
                    id = str(id)
                    size1 = int(size1)
                    x = re.findall("<.+>$", code)
                    file_tup2 = os.path.splitext(x[0][1:-1])
                    name = "new_up" + file_tup2[0] + f'{id}' + file_tup2[1]
                    upload_file = open(name, "wb")
                    li = math.ceil(size1/1024)
                    file_writer = b""
                    for i in range(li):
                        rec = con_soc.recv(1024)
                        file_writer += rec
                    print("writing")
                    upload_file.write(file_writer)
                    upload_file.close()
                    print("Finished Uploading")

                    try:
                        con_soc.send("done".encode())
                    except:
                        break

                elif func == "down":
                    x = re.findall("<.+>$", code)
                    file_name = x[0][1:-1]
                    size = os.path.getsize(x[0][1:-1])
                    print(size)
                    try:
                        con_soc.send(str(size).encode())
                    except:
                        break
                    download = open(file_name, "rb")
                    data2 = download.read(1024)
                    while data2:
                        con_soc.send(data2)
                        data2 = download.read(1024)
                    print("file sent")
                    download.close()
            except:
                break

            print("check")
            try:
                ip1 = con_soc.recv(64).decode()
                if ip1 == "Y":
                    serv = False
                    con_soc.close()
                else:
                    continue
            except:
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        con_soc.close()

def start_server():
    def handle_client(client_socket,addr, is_manipulated):
        addr1 = addr
        try:
            # Receive data from the client
            data = client_socket.recv(1024)

            if data:
                # Simulate processing the received data
                processed_data = f"Server received: {data.decode('utf-8')}"

                # Send the TCP handshake segment
                seq_number = random.randint(1, 10000) if is_manipulated else 12345
                handshake_segment = create_tcp_segment(9090, 5678, seq_number, 0, 0x02, 8192, b"")
                time.sleep(2)
                client_socket.send(handshake_segment)

                # Return the processed data to the client
                time.sleep(2)
                process_ftp(client_socket, addr1)
                return processed_data
            

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    
  


    server_socket_normal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_normal.bind(('localhost', 9090))
    server_socket_normal.listen(5)
    print("Server listening on port 9090 (Normal)...")

    server_socket_manipulated = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_manipulated.bind(('localhost', 9091))
    server_socket_manipulated.listen(5)
    print("Server listening on port 9091 (Manipulated ISN)...")

   

    try:
        while True:
            client_socket_normal, addr_normal = server_socket_normal.accept()
            print(f"Accepted connection on port 9090 from {addr_normal}")

            client_socket_manipulated, addr_manipulated = server_socket_manipulated.accept()
            print(f"Accepted connection on port 9091 from {addr_manipulated}")

  

            # Start threads to handle connections
            thread_normal = threading.Thread(target=handle_client, args=(client_socket_normal,addr_normal, False))
            thread_normal.start()
            thread_manipulated = threading.Thread(target=handle_client, args=(client_socket_manipulated,addr_manipulated,  True))
        
            thread_manipulated.start()
            
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket_normal.close()
        server_socket_manipulated.close()
 

if __name__ == "__main__":
    # Server addresses
    start_server()
 

 
