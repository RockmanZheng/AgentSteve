from socket import *
from threading import *
import time


class MyBaseClient:
    """
    Single-threaded.

    Methods:
    - work: should be overrided in derived class to specify jobs
    """

    Read_Buffer_Size = 1024
    Write_Buffer_Size = 1024

    def __init__(self,server_addr):
        # Create TCP client socket - the parameters here is for TCP socket
        self._socket = socket(AF_INET,SOCK_STREAM)
        self._addr = server_addr
        self._rfile = None
        self._wfile = None

    def start(self):
        """
        Start the client, attempt to connect to server        
        """
        # Try connecting
        try:
            print("Connecting server at {0}:{1}".format(self._addr[0],self._addr[1]))
            self._socket.connect(self._addr)
            # Blocking mode is necessary for using socket with file-like interface
            self._socket.setblocking(1)
            self._rfile = self._socket.makefile("rb",MyBaseClient.Read_Buffer_Size)
            self._wfile = self._socket.makefile("wb",MyBaseClient.Write_Buffer_Size)
        except:
            print("Something went wrong when connecting to {0}:{1}".format(self._addr[0],self._addr[1]))
            raise

    # Need to specify jobs here
    def work(self):
        while True:
            pass

    def run_forever(self):
        """
        Do works forever, until something went wrong.
        """
        try:
            self.work()
        except:
            print("Someting went wrong when working. Exit")
            self.disconnect()
            self.clean()
            raise
            
    def disconnect(self):
        """
        Disconnect from server
        """
        self._socket.close()

    # Cleaning here
    def clean(self):
        pass

    # Communication operation
    def send(self,data):
        """
        Send data to server
        """
        self._wfile.write(data)
        # Flushing the pipe is necessary after you write into it
        # And if the connection is broken, we could know from flushing
        self._wfile.flush()
        
    def get(self):
        """
        Receive data from server
        """
        return self._rfile.readline().strip()

class MySimpleClient(MyBaseClient):
    """
    Simple implementation of client
    Only work method needs to be overrided
    """
    def work(self):
        while True:
            print("From server {0}:{1} - {2}".format(self._addr[0],self._addr[1],self.get()))

if __name__=="__main__":
    """
    Demo run
    """
    host = "localhost"
    port = 8888
    client = MySimpleClient((host,port))
    client.start()
    client.run_forever()
