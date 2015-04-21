# chat_server.py
 
import sys
import socket
import select

HOST = '192.168.7.2' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 12345

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                #print "Client (%s, %s) connected" % addr
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = map(int, sock.recv(13).split())
                    #if data:
                        # there is something in the socket
                    #    print data
                    #else:
                        # remove the socket that's broken    
                    #    if sock in SOCKET_LIST:
                    #        SOCKET_LIST.remove(sock)
                except:
                    continue
    
    server_socket.close()
 
if __name__ == "__main__":
    sys.exit(chat_server())

