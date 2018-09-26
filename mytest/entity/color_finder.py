from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import time

from PIL import Image
import msgpackrpc


def count_r_g_b(img):
    nr, ng, nb = 0, 0, 0
    for pixel in img.getdata():
        r, g, b, _ = pixel
        nr += int(r > 127)
        ng += int(g > 127)
        nb += int(b > 127)
    w, h = img.size
    threshold = w * h / 2
    if nr > threshold:
        return 'red'
    elif ng > threshold:
        return 'green'
    elif nb > threshold:
        return 'blue'
    else:
        return 'a little bit of everything'


class ColorFinder(object):

    def __init__(self, forward_to_ip, forward_to_port):
        self.forward_to_ip = forward_to_ip
        self.forward_to_port = forward_to_port
        self.client = msgpackrpc.Client(
            msgpackrpc.Address(forward_to_ip, forward_to_port))
        print('forward data to {}:{}'.format(forward_to_ip, forward_to_port))

    def send(self, t_sent, bytedata):
        img = Image.open(io.BytesIO(bytedata))
        color = count_r_g_b(img)
        msg = '{}; latency={}'.format(color, time.time() - t_sent)
        result = self.client.call('send', t_sent, msg)
        print('forward data to {}:{}, result={}'.format(
            self.forward_to_ip, self.forward_to_port, result))
        return result


def run_server(ip, port, forward_to_ip, forward_to_port):
    print('start ColorFinder at {}:{}'.format(ip, port))
    server = msgpackrpc.Server(ColorFinder(forward_to_ip, forward_to_port))
    server.listen(msgpackrpc.Address(ip, port))
    server.start()
