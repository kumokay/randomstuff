from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import msgpackrpc


class DisplayServer(object):

    def send(self, t_sent, msg):
        t_recv = time.time()
        print('{}: {}, latency={}'.format(t_recv, msg, t_recv - float(t_sent)))
        return 'ACK'


def run_server(ip, port):
    print('start DataForwarder at {}:{}'.format(ip, port))
    server = msgpackrpc.Server(DisplayServer())
    server.listen(msgpackrpc.Address(ip, port))
    server.start()
