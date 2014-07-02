import zmq
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

class ZmqXMLRPCServer(SimpleXMLRPCDispatcher):
    def __init__(self):
        SimpleXMLRPCDispatcher.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5556")


    def serve_forever(self):
        while 1:
            try:
                request = self.socket.recv()
                response = self._marshaled_dispatch(request)
                # print response
                self.socket.send(response)
            except:
                break

        self.socket.close()    


def hello(name):
    return "hello %s" % name

def add(x, y):
    return x+y


if __name__ == '__main__':
    server = ZmqXMLRPCServer()
    server.register_function(hello)
    server.register_function(add)
    server.serve_forever()
