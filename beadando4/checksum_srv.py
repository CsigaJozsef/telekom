import socket
import sys
import datetime
import select

ip = sys.argv[1]
port = int(sys.argv[2])

chsum_data = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (ip, port)
server.bind(server_addr)
server.listen(4)
inputs = [server]

def ClearOldData():
    valid_elements = []
    global chsum_data
    for elem in chsum_data:

        delta = datetime.datetime.now() - elem["timestamp"]

        if delta.seconds <= int(elem["valid_time"]):
            valid_elements.append(elem)

    chsum_data = valid_elements

def GetFileById(id):

    for elem in chsum_data:
        if elem["fileid"] == id:
            return elem
    
    return 0



while inputs:
    readable, writable, exceptional = select.select(inputs, [], inputs)
    for sock in readable:
        if sock is server:
            connection, client_address = sock.accept()
            connection.setblocking(0)
            inputs.append(connection)
        else:
            received_data = sock.recv(1024)
            if received_data:
                data = received_data.decode()
                data = data.strip()
                data_arr = data.split('|')
                #print(data_arr)

                if data_arr[0] == "BE":
                    elem = {"fileid" : data_arr[1],
                            "valid_time" : data_arr[2],
                            "chsum_size" : data_arr[3],
                            "chsum" : data_arr[4],
                            "timestamp" : datetime.datetime.now()}
                    chsum_data.append(elem)
                    print('List appended')
                    print(elem)
                elif data_arr[0] == "KI":
                    response = ""
                    ClearOldData()
                    elem = GetFileById(data_arr[1])
                    if elem == 0:
                        response = "0|"
                    else:
                        response = elem["chsum_size"]+"|"+elem["chsum"]

                    print('Responding to "KI"')
                    print(response)
                    sock.send(response.encode())
                else:
                    inputs.remove(sock)
                    sock.close()



            