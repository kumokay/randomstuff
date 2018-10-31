from mininet.net import Containernet
from mininet.node import Controller, Docker, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Containernet(controller=Controller, link=TCLink)

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )
    d5 = net.addDocker( 'd5', dimage='kumokay/ubuntu_wifi:v6' )
    d6 = net.addDocker( 'd6', dimage='kumokay/ubuntu_wifi:v6' )

    info( '*** Adding switch\n' )
    s3 = net.addSwitch( 's3' )
    s4 = net.addSwitch( 's4' )

    info( '*** Creating links\n' )
    net.addLink( h1, s3 )
    link = net.addLink( s3, s4, delay='100ms' )
    net.addLink( h2, s4 )
    net.addLink( d5, s3 )
    net.addLink( d6, s4 )

    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    link.intf1.config(delay='500ms')
    CLI( net )

    link.intf2.config(delay='300ms')
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
