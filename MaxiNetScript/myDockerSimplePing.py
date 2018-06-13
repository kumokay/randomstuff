#!/usr/bin/env python2
""" A small example showing the usage of Docker containers.
"""

import time
import trollius as asyncio

from MaxiNet.Frontend import maxinet
from MaxiNet.Frontend.container import Docker
from mininet.topo import Topo
from mininet.node import OVSSwitch
from mininet.link import TCLink

@asyncio.coroutine
def exec_cmd(exp, node_name, command):
    node = exp.get_node(node_name)
    print('[{}] {} ======'.format(node_name, command))
    node.cmd(command)
    print('[{}] complete, ret:'.format(node_name))
    #print ret

    


topo = Topo()

d1 = topo.addHost("d1", cls=Docker, ip="10.0.0.251", dimage="kumokay/ubuntu14:latest")
d2 = topo.addHost("d2", cls=Docker, ip="10.0.0.252", dimage="kumokay/ubuntu14:latest")

s1 = topo.addSwitch("s1")
s2 = topo.addSwitch("s2")
topo.addLink(d1, s1, cls=TCLink, delay='20ms')
topo.addLink(s1, s2)
topo.addLink(d2, s2, cls=TCLink, delay='20ms')

cluster = maxinet.Cluster()
exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch)
exp.setup()

try:
    print(exp.get_node("d1").cmd("ifconfig"))
    print(exp.get_node("d2").cmd("ifconfig"))

    print('waiting 5 seconds for routing algorithms on the controller to converge')
    time.sleep(5)

    #print exp.get_node("d1").cmd("ping -c 5 10.0.0.252")
    #print exp.get_node("d2").cmd("ping -c 5 10.0.0.251")

#    loop = asyncio.get_event_loop()
#    tasks = [
#        asyncio.ensure_future(exec_cmd(exp, 'd1', 'cd /opt/github/sharescript/airsim && git pull && python hello_drone.py 172.17.109.3 0')),
#        asyncio.ensure_future(exec_cmd(exp, 'd2', 'cd /opt/github/sharescript/airsim && git pull && python hello_drone.py 172.17.109.3 1'))]
#    loop.run_until_complete(asyncio.wait(tasks))
#    loop.close()
    #print exp.get_node("d1").cmd("ping -c 5 172.17.109.100")
    #print exp.get_node("d1").cmd("ping -c 5 172.17.109.100")


    #print exp.get_node("d1").cmd("cd /opt && git clone https://github.com/kumokay/sharescript.git")
    #print exp.get_node("d2").cmd("cd /opt && git clone https://github.com/kumokay/sharescript.git")
    #time.sleep(5)
    print exp.get_node("d1").sendCmd("python hello_drone.py 172.17.109.3 0")
    print exp.get_node("d2").sendCmd("python hello_drone.py 172.17.109.3 1")

    time.sleep(10)    
    
    #print exp.get_node("d1").cmd("ping -c 5 172.17.109.100")
    #print exp.get_node("d2").cmd("ping -c 5 172.17.109.100")

finally:
    exp.stop()
