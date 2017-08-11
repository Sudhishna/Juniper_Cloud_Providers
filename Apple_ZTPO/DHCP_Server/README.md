##DHCP Server:

- sudo apt-get install isc-dhcp-server

- sudo vi /etc/network/interfaces
'''
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.77.1
    netmask 255.255.255.0
    network 192.168.77.0
    broadcast 192.168.77.255
    gateway 192.168.77.250
'''

- sudo vi /etc/default/isc-dhcp-server
'''
INTERFACES="eth0"
'''

- sudo vi /etc/dhcp/dhcpd.conf
copy content from the attached file

- sudo service isc-dhcp-server restart
