from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import msgpackrpc


def call(ip, port, cmd, *argv):
    client = msgpackrpc.Client(msgpackrpc.Address(ip, port))
    result = client.call(cmd, *argv)
    print('Client call {}, argv={}, result={}'.format(cmd, argv, result))
