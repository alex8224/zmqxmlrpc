# -*-coding:utf8 -*-

import xmlrpclib
from xmlrpclib import _Method, loads
import zmq


class ZmqTransport(xmlrpclib.Transport):

    def __init__(self, uri):
        xmlrpclib.Transport.__init__(self)
        self.context = zmq.Context()
        self.connection = self.context.socket(zmq.REQ)
        self.connection.connect(uri)


    def request(self, requestbody):
        self.connection.send(requestbody)
        response = self.connection.recv()
        returnvalue, methodname = loads(response)
        return returnvalue

    def __close(self):
        print "close~"
        self.connection.close()

class ZmqProxy(object):

    def __init__(self, uri):

        self.uri = uri
        self.__transport = ZmqTransport(self.uri)


    def __request(self, methodname, params):

        body = xmlrpclib.dumps(params, methodname)
        response = self.__transport.request(body)
    
        if len(response) == 1:
            response = response[0]

        return response    


    def __getattr__(self, name):
        return _Method(self.__request, name)


    def __call__(self, attr):
        if attr == "close":
            return self.__transport.close()
        if attr == "transport":
            return self.__transport

        raise AttributeError("Attribute %r not found" % (attr, ))

    def __repr__(self):
        return ("<ZmqProxy for %s>" % (self.uri))


def callremote():
    proxy = ZmqProxy("tcp://127.0.0.1:5559")
    print str(proxy)
    print proxy.header("http://mail.qq.com")


if __name__ == '__main__':
    import multiprocessing
    tasklist = []
    import time
    s = time.time()
 
    for pindex in range(4):
        process = multiprocessing.Process(target=callremote, args=())
        process.start()
        tasklist.append(process)

    for task in tasklist:
        task.join()

    print(time.time() -s)    
