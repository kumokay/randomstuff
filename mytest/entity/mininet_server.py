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

    def move(self, t_sent, x, y, z, speed):
        x = float(x)
        y = float(y)
        z = float(z)
        speed = float(speed)
        print('move sta1 to {} {} {}'.format(x, y, z))
        self.topo.move_station('sta1', next_pos=(x, y, z), speed=speed)
        return 'ACK'

    def stop(self, t_sent):
        print('stop')
        self.topo.run_cli()
        self.topo.stop()
        return 'ACK'


def run_server(ip, port):
    print('start MininetServer at {}:{}'.format(ip, port))
    server = msgpackrpc.Server(MininetServer())
    server.listen(msgpackrpc.Address(ip, port))
    server.start()
