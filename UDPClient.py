import socket
import packetClass
import math

def packToByte(rawPacket):
    return packetClass.packetClass( int.from_bytes(rawPacket[0:4], "big"),rawPacket[8:len(rawPacket)])
def getSeqNo(packet):
    return packet.seqno
UDP_IP = "127.0.0.1"
UDP_PORT = 5006


sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
packets = list()
expectedPacket = 0
while True:
    sock.settimeout(5)
    
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("Got packet number ", int.from_bytes(data[0:4], "big"))
        if int.from_bytes(data[0:4], "big") == expectedPacket:
            packets.append(packToByte(data))
            sock.sendto(b'1', (UDP_IP, UDP_PORT-1))
            
            expectedPacket+=1;
        else:
            print("Expected", expectedPacket);
            sock.sendto(b'0', (UDP_IP, UDP_PORT-1))
            
        
    except:
        if len(packets) > 0:
            packets.sort(key=getSeqNo)
            fileData = b''
            for val in packets:
                fileData += val.data

            with open("dupe.png", mode="wb") as f:
                print(f.write(fileData))
            packets = list()
            expectedPacket = 0
