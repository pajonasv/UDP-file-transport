#Server Control Block: just keeps track of server info
class packetClass:
    def __init__(self, seqno, data):
        self.seqno = seqno #4 bytes
        self.data = data;
        self.leng = 8 + len(data) #4 bytes
