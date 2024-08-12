import socket
import sys
import struct
import math

host = sys.argv[1]
port = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (host, port)
client.connect(server_addr)

packer = struct.Struct('ci')

game_over = False

min = 0
max = 100

index = -1
rel = b'<'

while not game_over:
    act_guess = math.floor((max + min) / 2)
    data = packer.pack(rel,act_guess)
    client.send(data)
    #print("data sent: ")
    print(rel)
    print(act_guess)
    #print("\n")

    received_data = client.recv(struct.calcsize(packer.format))
    received_answear = packer.unpack(received_data)
    #print("incoming answear: ")
    print(received_answear)

    if received_answear[0] == b'K' or received_answear[0] == b'V':
        print('L')
        game_over = True
    elif received_answear[0] == b'Y':
        print('W')
        game_over = True
    elif received_answear[0] == b'I':
        if rel == b'>': #nagyobb
            min = act_guess + 1
        else:
            max = act_guess - 1
    elif received_answear[0] == b'N':
        if rel == b'>': #nagyobb
            max = act_guess + 1
            rel = b'<'
        else:
            min = act_guess - 1
            rel = b'>'

    if index == act_guess:
        rel = b'='

    index = act_guess

