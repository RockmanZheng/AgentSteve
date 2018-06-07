from SocketServer import TCPServer,BaseRequestHandler


class MalmoEndHandler(BaseRequestHandler):
    """
    New handler instance is created every time TCPServer handles a new request
    """

#    def __init__(self,video_reader):
#        self._video_reader = video_reader

    def setup(self):
        """
        Do initialization works here
        """
        pass

    def handle(self):
        # Retrieve data from server
        request = self.request
        client_address = self.client_address
        server = self.server

        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.data.upper())

    def finish(self):
        """
        Cleaning up here
        """
        pass

# Or this way
class MalmoEndHandler(StreamRequestHandler):
    """
    New handler instance is created every time TCPServer handles a new request
    Stream
    """
    def handle(self):
        self.data = self.rfile.readline().strip()
        self.wfile.writeline(self.data.upper())

    

class VideoReader:
    """
    Video stream reader
    Expose interfaces to MalmoEnd for reading in video
    It must prepare video stream for reading
    """
    def __init__(self):
        self.name = "video_stream_reader"

    def next_frame():
        """
        Interface for reading the next frame from stream
        """
        raise NotImplementedError
        
    

class MalmoEnd(TCPServer):
    def __init__(self,addr,video_reader,request_handler=MalmoEndHandler,bind_active,bind_and_activate=True):
        self._handler = MalmoEndHandler(video_reader)
        TCPServer.__init__(self,addr,request_handler)
        raise NotImplementedError

"""
Sample code:
"""
host = "localhost"
port = 8888
malmo_video_server = MalmoEnd(addr=(host,port))
malmo_video_server.serve_forever()

        
        
