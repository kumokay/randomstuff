from subprocess import call
import sys
sys.path.append('/home/osboxes/github/mininet-wifi')
from mininet.node import RemoteController, Node, Docker
from mininet.log import setLogLevel, info
from mininet_wifi.wifi.node import OVSKernelAP, Station, DockerStation
from mininet_wifi.wifi.cli import CLI_wifi
from mininet_wifi.wifi.net import Mininet_wifi


def topology(is_enable_cli=False):
    """
    create a network.

    mode (str): miminet or containernet
    is_enable_cli (bool): running CLI
    """
    c1 = RemoteController('c1', ip='172.17.20.12', port=6633)
    net = Mininet_wifi(accessPoint=OVSKernelAP)
    info("*** Starting network\n")
    net.build()
    c1.start()
    if is_enable_cli:
        info("*** Running CLI\n")
        CLI_wifi(net)
    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    return_code = call('mn -c', shell=True)
    setLogLevel('debug')
    coord = True if '-c' in sys.argv else False
    topology()
