# client side

import msgpackrpc
import base64
import time

server_ip = some_ip
server_port = some_port
image_data_uint8 = some_image_bytes

myrpcclient = msgpackrpc.Client(
    msgpackrpc.Address(server_ip, server_port))
data = base64.b64encode(image_data_uint8)
ret = myrpcclient.call('push', data, time.time())
print('image sent to {}:{}, ret={}'.format(
    server_ip, server_port, ret))


# server_side

import msgpackrpc
import base64
import time
import subprocess
from PIL import Image

server_ip = some_ip
server_port = some_port

class rpcServer(object):
    def _compute(self, data):
        t1 = time.time()
        yolo_folder = '/home/kumokay/github/darknet'
        image_data = base64.b64decode(data)
        image = Image.open(io.BytesIO(image_data))
        image.save('{}/img.png'.format(yolo_folder), 'PNG')
        proc = subprocess.Popen(
            './darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights img.png',
            stdout=subprocess.PIPE, shell=True, cwd=yolo_folder, )
        result = proc.communicate()[0]
        t2 = time.time()
        return 'exec_time: {}, result:\n{}'.format(t2-t1, result)
        
    def push(self, data, timestamp):
        print("recv result={}; sender_time={}".format(result, timestamp))
        result = self._compute(data)
        if 'car' in result:
            print('we found the car!')
        return result

server = msgpackrpc.Server(rpcServer())
server.listen(msgpackrpc.Address(server_ip, server_port))
server.start()
server.close()
