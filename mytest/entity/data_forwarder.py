from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time

import msgpackrpc


class DataForwarder(object):

    def __init__(self, forward_to_ip, forward_to_port, is_timestamper):
        self.is_timestamper = is_timestamper
        self.forward_to_ip = forward_to_ip
        self.forward_to_port = forward_to_port
        self.client = msgpackrpc.Client(
            msgpackrpc.Address(forward_to_ip, forward_to_port))
        print('forward data to {}:{}'.format(forward_to_ip, forward_to_port))

    def send(self, t_sent, data):
        if self.is_timestamper:
            t_sent = time.time()
        result = self.client.call('send', t_sent, data)
        print('forward data to {}:{}, result={}'.format(
            self.forward_to_ip, self.forward_to_port, result))
        return result


def run_server(ip, port, forward_to_ip, forward_to_port, is_timestamper=False):
    print('start DataForwarder at {}:{}'.format(ip, port))
    server = msgpackrpc.Server(
        DataForwarder(forward_to_ip, forward_to_port, is_timestamper))
    server.listen(msgpackrpc.Address(ip, port))
    server.start()
