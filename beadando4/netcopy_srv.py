import socket
import sys
import hashlib

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])
chsum_srv_ip = sys.argv[3]
chsum_srv_port = int(sys.argv[4])
file_id = sys.argv[5]
file = sys.argv[6]

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_address = (srv_ip, srv_port)
srv.bind(srv_address)
srv.listen(1)

chsum_address = (chsum_srv_ip, chsum_srv_port)

#receive file
client, client_addr = srv.accept()

with open(file, 'wb') as f:
    while True:
        data = client.recv(200)
        if not data:
            break
        f.write(data)

client.close()
srv.close()

#connect to chsum_server get chsum
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.connect(chsum_address)

file_data = open(file, 'rb').read()
m = hashlib.md5()
m.update(file_data)
calculated_chsum = m.hexdigest()
print(calculated_chsum)

chsum_message = "KI|"+file_id
srv.send(chsum_message.encode())

received_message = srv.recv(1024)
received_message = received_message.decode()
received_data = received_message.split('|')
print(received_data)

if int(received_data[0]) > 0:
    if received_data[1] == calculated_chsum:
        print('CSUM OK')
    else:
        print('CSUM CORRUPTED')
else:
    print('CSUM CORRUPTED')

srv.close()