import msgpackrpc
import base64
import time

for i in range(1, 5):
    filepath = '/home/kumokay/github/placethings/config_line_backup/{}-0.png'.format(i)
    with open(filepath, 'rb') as binary_file:
        # Read the whole file at once
        data = binary_file.read()
    data = base64.b64encode(data)

    t1 = time.time()
    client = msgpackrpc.Client(msgpackrpc.Address("172.17.49.51", 18800))
    result = client.call('rec_img', data)
    t2 = time.time()
    print(result)
    print(t2-t1)
    # time.sleep(3)
