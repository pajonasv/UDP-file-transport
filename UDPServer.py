import socket
import packetClass
import math
def packToByte(packet):

    toReturn = (packet.seqno).to_bytes(4, "big")
    toReturn += (packet.leng).to_bytes(4, "big")
    toReturn += packet.data
    return toReturn;

def divideIntoPackets(file):

    toReturn = list()
    packNo = 0
    while packNo < math.ceil(len(file)/1024):
        data = bytearray()
        offset = packNo*1016
        end = ((packNo+1)*1016)
        if(end > len(file)):
            end = len(file)
        data = file[offset:end]
        toReturn.append(packetClass.packetClass(packNo,data))
        packNo += 1
    print(packNo)
    return toReturn    
    

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

with open('mrSaturn.png', mode='rb') as f:
    fileContent = f.read()

packets = divideIntoPackets(fileContent)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

for val in packets:
    data = bytes(0)
    while int.from_bytes(data, "big") == 0:
        print("Got Ack 0")
        sock.sendto(packToByte(val), (UDP_IP, UDP_PORT+1))
        print("sent packet ", val.seqno)
        data, addr = sock.recvfrom(1024)
        
    print("Got Ack 1")
    
    
