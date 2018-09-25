from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io

from PIL import Image
import msgpackrpc


def has_red_obj(img):
    w, h = img.size
    n_red = 0
    for pixel in img.getdata():
        r, g, b, _ = pixel
    if r > 80 and b < 40 and g < 40:
        n_red += 1
    return n_red / w * h > 0.3


class ColorFinder(object):

    def __init__(self, forward_to_ip, forward_to_port):
        self.forward_to_ip = forward_to_ip
        self.forward_to_port = forward_to_port
        self.client = msgpackrpc.Client(
            msgpackrpc.Address(forward_to_ip, forward_to_port))
        print('forward data to {}:{}'.format(forward_to_ip, forward_to_port))

    def send(self, t_sent, bytedata):
        img = Image.open(io.BytesIO(bytedata))
        if has_red_obj(img):
            msg = 'found red objects in picture'
        else:
            msg = 'nothing found'
        result = self.client.call('send', t_sent, msg)
        print('forward data to {}:{}, result={}'.format(
            self.forward_to_ip, self.forward_to_port, result))
        return result


def run_server(ip, port, forward_to_ip, forward_to_port):
    print('start ColorFinder at {}:{}'.format(ip, port))
    server = msgpackrpc.Server(ColorFinder(forward_to_ip, forward_to_port))
    server.listen(msgpackrpc.Address(ip, port))
    server.start()
