from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import msgpackrpc

from netgen.topogen import Topo


class MininetServer(object):

    def __init__(self):
        self.topo = Topo()
        self.topo.start()
        # self.topo.run_cli()
        # self.topo.stop()

    def move(self, x, y, z, speed):
        self.topo.move_station('sta1', next_pos=(x, y, z), speed=speed)
        return 'ACK'

    def stop(self):
        self.topo.run_cli()
        self.topo.stop()
        return 'ACK'


def run_server(ip, port):
    print('start MininetServer at {}:{}'.format(ip, port))
    server = msgpackrpc.Server(MininetServer())
    server.listen(msgpackrpc.Address(ip, port))
    server.start()
