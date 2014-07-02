# -*-coding:utf8 -*-

import time
from zmq_rpcserver import ZmqXMLRPCServer

class LogServer(object):

    def __init__(self, logpath):
        self.logpath = logpath

    def __time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def debug(self, message):

        debug_tpl = "[DEBUG] %s %s\n" % (self.__time(), message)
        with open(self.logpath,"a+") as logfile:
            logfile.write(debug_tpl)

        return True    

    def error(self, message):
        debug_tpl = "[ERROR] %s %s\n" % (self.__time(), message)
        with open(self.logpath,"a+") as logfile:
            logfile.write(debug_tpl)

        return True    


if __name__ == '__main__':
    server = ZmqXMLRPCServer()
    server.register_instance(LogServer("/tmp/testlogfile.txt"))
    server.serve_forever()
