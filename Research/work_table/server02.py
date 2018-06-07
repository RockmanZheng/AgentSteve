from socket import *
from Queue import *
from threading import *
import time

class MyBaseServer:
    """
    This server will provide every client the same service
    It is originally designed for video stream feed
    1 main thread
    1 acceptance thread
    Each connected client per service thread, providing same content
    """
    Client_Pool_Capacity = 100
    Accept_Sleep_Time = 10
    Read_Buffer_Size = 1024
    Write_Buffer_Size = 1024

    class Client:
        """
        More like a struct. Make data easier to access
        """
        def __init__(self,conn,addr):
            self.conn = conn
            self.addr = addr
            # Ensure the socket is in blocking mode, in order to use makefile
            self.conn.setblocking(1)
            # Make file interface for socket communication
            self.rfile = self.conn.makefile("rb",MyBaseServer.Read_Buffer_Size)
            self.wfile = self.conn.makefile("wb",MyBaseServer.Write_Buffer_Size)

        # Properties
        @property
        def conn(self):
            return self.conn

        @property
        def addr(self):
            return self.addr

        @property
        def rfile(self):
            return self.rfile

        @property
        def wfile(self):
            return self.wfile

    def __init__(self,addr):
        """
        addr: (host,port) pair
        """
        self._addr = addr
        # Create TCP server socket - the parameters here is for TCP socket
        self._socket = socket(AF_INET,SOCK_STREAM)
        # Set reusable socket
        # To avoid "Address already in use" error when binding
        self._socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        print("Bindding {0}:{1}".format(addr[0],addr[1]))
        self._socket.bind(self._addr)
        print("Listening {0}:{1}, client capacity: {2}".format(addr[0],addr[1],MyBaseServer.Client_Pool_Capacity))
        self._socket.listen(MyBaseServer.Client_Pool_Capacity)
        # Client connection list, should not excceed Client_Pool_Capacity
        # Python list is thread safe. But data in list is not, which should be noted
        self._clients = []
        # Each client will have a service for it
        self._services = []
        # Pass in server instance to acceptance thread
        self._accept_thread = MyBaseServer.AcceptThread(self)
        self._has_disconnect = Event()

    @property
    def socket(self):
        return self._socket

    @property
    def clients(self):
        return self._clients

    @property
    def services(self):
        return self._services

    @property
    def has_disconnect(self):
        return self._has_disconnect

    class AcceptThread(Thread):
        """
        A thread class wrapper for acceptance job.
        Blockingly accept every incoming connect request, until we reach client pool capacity.
        Assign the same service for every connected client, by creating a new Service thread
        If we reach client pool capacity, wait until someone disconnect
        """
        def __init__(self,server):
            Thread.__init__(self)
            self._server=server

        def run(self):
            server = self._server
            while True:
                if len(server.clients)<MyBaseServer.Client_Pool_Capacity:
                    # Blocking accept
                    # conn is a new socket for this connection
                    print("Waiting for connection request...")
                    conn,addr = server.socket.accept()
                    print("Got {0}:{1} connection".format(addr[0],addr[1]))
                    this_client = MyBaseServer.Client(conn,addr)
                    server.clients.append(this_client)
                    # Assign service for this client
                    print("Assigning service for this client...")
                    this_service = MyBaseServer.Service(server,this_client)
                    this_service.start()
                    server.services.append(this_service)
                else:
                    print("Reached client pool capacity")
                    # Wait for someone disconnects
                    server.has_disconnect.wait(MyBaseServer.Accept_Sleep_Time)
                    # Reset disconnect flag
                    server.has_disconnect.clear()

    # This is where you write specific job for server
    def serve(self,client):
        """
        Server particular client
        """
        while True:
            pass

    # No need to override
    class Service(Thread):
        """
        Thread wrapper for service.
        If exception raised in serving, we will disconnect this client
        """
        def __init__(self,server,client):
            Thread.__init__(self)
            self._client = client
            self._server = server

        def run(self):
            client = self._client
            addr = client.addr
            conn = client.conn
            server = self._server
            try:
                server.serve(client)
            except:
                print("{0}:{1} Something went wrong, disconnect!".format(addr[0],addr[1]))
                conn.close()
                # Clear this client from client pool
                server.clients.remove(client)
                # Trigger has disconnect event
                server.has_disconnect.set()
                raise
            

    def start(self):
        """
        start the server
        """
        # Start accepting connection
        print("Starting accepting thread...")
        self._accept_thread.start()
        

    ## Communication operation
    def send(self,client,data):
        """
        Send data to specific client
        """
        wfile = client.wfile
        wfile.write(data)
        # Flushing the pipe is necessary after we done writing data into it
        # If the pipe is broken, flush will throw an exception, so we will konw it from here
        wfile.flush()

    def get(self,client):
        """
        Receive and read blockingly (as set in __init__ of Client class) from this particular client
        Read data seperated by newline character
        """
        rfile = client.rfile
        return rfile.readline().strip()

    def serve_forever(self):
        """
        Serve forever, untile something went wrong in acceptance thread
        """
        try:
            # Block until this thread terminates
            self._accept_thread.join()
        except:
            raise

class MySimpleServer(MyBaseServer):
    """
    Simple server implementation
    Only need to override serve method
    """
    def serve(self,client):
        """
        Server particular client
        """
        while True:
            # Consistently send message
            self.send(client,"HEY YOU\n")
            # Wait a sec
            time.sleep(1)

if __name__=="__main__":
    """
    Demo run
    """
    host = "localhost"
    port = 8888
    server = MySimpleServer((host,port))
    server.start()
    server.serve_forever()
