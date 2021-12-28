import socket

# addresses: key: id, value: boat/ros addr pair
# addr pair: key : 'S' for ROS, 'R' for phone, value: ip/port addr
addresses = {}

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('',32145))

def str_to_bytes(s):
    return int.to_bytes(len(s),2,'big')+bytes(s,'utf')

def port_to_bytes(port):
    return int.to_bytes(port,4,'big',signed=False)

def addr_to_bytes(addr):
    ip = addr[0]
    port = addr[1]
    return str_to_bytes(ip) + port_to_bytes(port)

ticket = 300_000
def send_addr(addr1,addr2):
    ticket = send_addr.connection_ticket
    ticket_bytes = int.to_bytes(ticket,8,'big',signed=True)
    send_addr.connection_ticket += 1
    command = 'CC'
    command_bytes = str_to_bytes(command)
    payload = addr_to_bytes(addr2)
    packet = ticket_bytes + command_bytes+payload
    sock.sendto(packet,addr1)
    return 5
send_addr.connection_ticket = ticket

data = ''

S = ord('S')
R = ord('R')
both = S^R
while True:
    try:
        data,addr = sock.recvfrom(1024)
    except:
        continue

    if (len(data)>0):
        print(data)
        if (data[0] == S or data[0] == R):
            # PHONe or ROS
            idx = data[1]
            key_sender = chr(data[0])
            key_other = chr(both^data[0]) # if key is S, this assigns R to key_other, and vice versa
            if (idx not in addresses):
                addresses[idx] = {}
            addresses[idx][key_sender] = addr
            if (key_other in addresses[idx]):
                # both connected, send details to one asking
                send_addr(addr,addresses[idx][key_other])
        else :
            if (len(data)>=12):
                # ack phone packets
                ack = 'OK'
                packet = data[:8] + str_to_bytes(ack)
                sock.sendto(packet,addr)


