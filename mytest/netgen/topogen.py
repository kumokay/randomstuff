from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
sys.path.append('/home/kumokay/github/mininet-wifi')
from math import sqrt
from time import sleep, time

from future.utils import iteritems
from mininet import log
from mininet.node import RemoteController, Node, Docker
from mininet_wifi.wifi.node import OVSKernelAP, Station, DockerStation
from mininet_wifi.wifi.cli import CLI_wifi
from mininet_wifi.wifi.net import Mininet_wifi


log.setLogLevel('debug')


class Topo(object):

    def __init__(self):
        self.ap_dict = {}
        self.sw_dict = {}
        self.host_dict = {}
        self.sta_dict = {}
        self.net = Mininet_wifi(accessPoint=OVSKernelAP)
        self.net.propagationModel(model="logDistance", exp=5)
        self.c1 = RemoteController('c1', ip='172.17.20.12', port=6633)
        self.add_nodes()

    def start(self):
        log.info("*** Starting network\n")
        # self.net.plotGraph(max_x=200, max_y=200)
        self.ts_netstart = time()
        # trigger attachment
        for sta_name, sta_obj in iteritems(self.sta_dict):
            self.net.startMobility(time=0, repetitions=1)
            self.net.mobility(sta_obj, 'start', time=1, position='0,0,0')
            self.net.mobility(sta_obj, 'stop', time=2, position='0,0,0')
            self.net.stopMobility(time=3)
        self.net.build()
        self.c1.start()
        for ap_name, ap_obj in iteritems(self.ap_dict):
            ap_obj.start([self.c1])
        sleep(3)  # wait for setup
        # TODO: clean this shit
        result = self.exec_cmd(
            'h1',
            'python main.py color_finder 10.0.0.11:18800 10.0.0.13:18800')
        log.info(result)
        result = self.exec_cmd(
            'sta1',
            'python main.py data_forwarder 172.18.0.3 10.0.0.11:18800')
        log.info(result)
        result = self.exec_cmd(
            'sta2',
            'python main.py display_server 10.0.0.13:18800')
        log.info(result)

    def run_cli(self):
        log.info("*** Running CLI\n")
        CLI_wifi(self.net)

    def stop(self):
        log.info("*** Stopping network\n")
        self.net.stop()

    def exec_cmd(self, node_name, cmd):
        if node_name in self.sta_dict:
            node = self.sta_dict[node_name]
        elif node_name in self.host_dict:
            node = self.host_dict[node_name]
        else:
            assert False, 'no such node {}'.format(node_name)
        return node.cmd(cmd)

    def move_station(self, sta_name, next_pos=None, speed=None):
        assert sta_name in self.sta_dict
        sta = self.sta_dict[sta_name]
        if 'position' in sta.params:
            cur_x, cur_y, cur_z = sta.params['position']
            cur_x, cur_y, cur_z = float(cur_x), float(cur_y), float(cur_z)
        else:
            cur_x, cur_y, cur_z = 0.0, 0.0, 0.0
        if not next_pos:
            next_x, next_y, next_z = cur_x, cur_y, cur_z
        else:
            next_x, next_y, next_z = next_pos
        if not speed:
            duration = 1
        else:
            duration = int(sqrt(
                (next_x - cur_x)**2 + (next_y - cur_y)**2
                + (next_z - cur_z)**2) / speed)
        log.info(
            '[I] move {} from ({} {} {}) to ({} {} {}), dur={}\n'.format(
                sta_name,
                cur_x, cur_y, cur_z,
                next_x, next_y, next_z,
                duration))
        while duration > 0:
            sta.setPosition('{}, {}, {}'.format(next_x, next_y, next_z))
            duration -= 1

    def add_nodes(self, mode='containernet'):
        """
        add nodes to net.
        Args:
            mode (str): miminet or containernet
        Returns:
            ap_dict, sw_dict, host_dict, sta_dict
        """
        log.info("*** Creating nodes\n")
        if mode == 'mininet':
            h1 = self.net.addHost(
                'h1', cls=Node, mac='00:00:00:00:00:01', ip='10.0.0.11/8')
            sta1 = self.net.addStation(
                'sta1', cls=Station, mac='00:00:00:00:00:02', ip='10.0.0.12/8')
            sta2 = self.net.addStation(
                'sta2', cls=Station, mac='00:00:00:00:00:03', ip='10.0.0.13/8')
        else:
            dimage_name = 'kumokay/ubuntu_wifi:v3'
            h1 = self.net.addHost(
                'h1', cls=Docker, dimage=dimage_name,
                mac='00:00:00:00:00:01', ip='10.0.0.11/8')
            sta1 = self.net.addStation(
                'sta1', cls=DockerStation, dimage=dimage_name,
                mac='00:00:00:00:00:02', ip='10.0.0.12/8')
            sta2 = self.net.addStation(
                'sta2', cls=DockerStation, dimage=dimage_name,
                mac='00:00:00:00:00:03', ip='10.0.0.13/8')
        ap1 = self.net.addAccessPoint(
            'ap1', ssid='new-ssid', mode='g', channel='1',
            position='0,0,0', range=60)
        self.net.addController(self.c1)

        # add all nodes to dict
        self.ap_dict['ap1'] = ap1
        self.host_dict['h1'] = h1
        self.sta_dict['sta1'] = sta1
        self.sta_dict['sta2'] = sta2

        log.info("*** Configuring wifi nodes\n")
        self.net.configureWifiNodes()

        log.info("*** Associating and Creating links\n")
        self.net.addLink(ap1, h1, delay='5ms')


def test():
    topo = Topo()
    topo.start()
    # topo.move_station('sta1', next_pos=(20.0, 40.0, 0.0), speed=1)
    topo.move_station('sta2', next_pos=(30.0, 20.0, 0.0), speed=10)
    topo.run_cli()
    topo.stop()
