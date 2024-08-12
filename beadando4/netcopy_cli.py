import socket
import sys
import hashlib

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])
chsum_srv_ip = sys.argv[3]
chsum_srv_port = int(sys.argv[4])
file_id = sys.argv[5]
file = sys.argv[6]
        

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_address = (srv_ip, srv_port)
chsum_address = (chsum_srv_ip, chsum_srv_port)


#file sending
client.connect(srv_address)

with open(file, 'rb') as f:
    data = f.read(200)
    while data:
        client.sendall(data)
        data = f.read(200)

    client.send("".encode())

client.close()

#chsum sending
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(chsum_address)

file_data = open(file, 'rb').read()
m = hashlib.md5()
m.update(file_data)
chsum = m.hexdigest()

chsum_message = "BE|"+file_id+"|60|"+str(m.digest_size)+"|"+str(chsum)
print('CHSUM SENT')
print(chsum_message)

client.send(chsum_message.encode())

client.close()
