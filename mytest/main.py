from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import time

from entity import (
    mininet_server, data_forwarder, color_finder, display_server, client)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('usage: python main.py ENTITY arg1 arg2 ...')
    entity = sys.argv[1]
    print('running entity {}'.format(entity))
    if entity == 'client':
        # python main.py mininet_server 172.17.20.12:18800
        ip, port = sys.argv[2].split(':')
        port = int(port)
        cmd = sys.argv[3]
        arg_list = [time.time()]
        for i in range(4, len(sys.argv)):
            arg_list.append(sys.argv[i])
        client.call(ip, port, cmd, *arg_list)
    elif entity == 'img_client':
        # python main.py mininet_server 172.17.20.12:18800
        ip, port = sys.argv[2].split(':')
        port = int(port)
        path = (
            '/home/kumokay/Documents/image/new_img/'
            '2018-09-22-17-22-10/output_5sec/1537662205.png')
        with open(path, 'r') as fd:
            bytes = fd.read()
        client.call(ip, port, 'send', time.time(), bytes)
    elif entity == 'mininet_server':
        # python main.py mininet_server 172.17.20.12:18800
        ip, port = sys.argv[2].split(':')
        port = int(port)
        mininet_server.run_server(ip, port)
    elif entity == 'data_forwarder':
        # python main.py data_forwarder 172.17.20.12:18900 172.18.0.14:18800
        ip, port = sys.argv[2].split(':')
        port = int(port)
        forward_to_ip, forward_to_port = sys.argv[3].split(':')
        forward_to_port = int(forward_to_port)
        data_forwarder.run_server(ip, port, forward_to_ip, forward_to_port)
    elif entity == 'color_finder':
        # python main.py color_finder 172.17.20.12:18800
        ip, port = sys.argv[2].split(':')
        port = int(port)
        forward_to_ip, forward_to_port = sys.argv[3].split(':')
        forward_to_port = int(forward_to_port)
        color_finder.run_server(ip, port, forward_to_ip, forward_to_port)
    elif entity == 'display_server':
        # python main.py color_finder 172.17.20.12:18800
        ip, port = sys.argv[2].split(':')
        port = int(port)
        display_server.run_server(ip, port)
