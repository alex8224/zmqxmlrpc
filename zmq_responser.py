import zmq
import sys
import time
import requests
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

class ZmqXMLRPCServer(SimpleXMLRPCDispatcher):
    def __init__(self):
        SimpleXMLRPCDispatcher.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.connect("tcp://127.0.0.1:5560")
        self.dispatchcount = 0


    def serve_forever(self):
        while 1:
            try:
                request = self.socket.recv()
                self.dispatchcount +=1
                sys.stdout.write("\r%d times" % self.dispatchcount)
                sys.stdout.flush()
                response = self._marshaled_dispatch(request)
                self.socket.send(response)
            except:
                break

        self.socket.close()    


def hello(name):
    return "hello %s" % name

def add(x, y):
    time.sleep(1)
    return x+y

def header(url):
    return dict(requests.head(url).headers)

if __name__ == '__main__':
    server = ZmqXMLRPCServer()
    server.register_function(hello)
    server.register_function(add)
    server.register_function(header)
    server.serve_forever()
