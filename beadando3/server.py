import socket
import sys
import select
import struct
import random

host = sys.argv[1]
port = int(sys.argv[2])

packer = struct.Struct('ci')

game_over = False

min = 0
max = 100
number_to_find = random.randint(0, 100)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (host, port)
server.bind(server_addr)
server.listen(16)
inputs = [server]

#print("server up "+str(server_addr[1]))
#print(number_to_find)

while inputs:
    readable, writable, exceptional = select.select(inputs, [], inputs)
    for sock in readable:
        if sock is server:
            connection, client_address = sock.accept()
            connection.setblocking(0)
            inputs.append(connection)
            #print("new client: "+str(client_address[1]))
        else:
            received_data = sock.recv(struct.calcsize(packer.format))
            if received_data:
                received_guess = packer.unpack(received_data)
                #print("Incoming guess: ")
                #print(received_guess)

                if game_over:
                    data = packer.pack(b'V',0)
                    sock.send(data)
                    continue

                response = [b'K',0]
                if received_guess[0] == b'>': #nagyobb
                    if number_to_find > received_guess[1]:
                        response[0] = b'I'
                    else:
                        response[0] = b'N'
                elif received_guess[0] == b'<': #kisebb
                    if number_to_find < received_guess[1]:
                        response[0] = b'I'
                    else:
                        response[0] = b'N'
                elif received_guess[0] == b'=':
                    if number_to_find == received_guess[1]:
                        response[0] = b'Y'
                        game_over = True
                    else:
                        response[0] = b'K'

                data = packer.pack(*response)
                sock.send(data)
            else:
                #print('closing ' + str(sock.getpeername()) + ' after reading no data')
                inputs.remove(sock)
                sock.close()