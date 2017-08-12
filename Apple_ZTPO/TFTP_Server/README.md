## TFTP Server:

- sudo apt-get install xinetd tftpd tftp
- Configure /etc/xinetd.d/tftp
```
service tftp
{
protocol        = udp
port            = 69
socket_type     = dgram
wait            = yes
user            = nobody
server          = /usr/sbin/in.tftpd
server_args     = /tftpboot
disable         = no
}
```

- sudo mkdir /tftpboot
- sudo chmod -R 777 /tftpboot
- sudo chown -R nobody /tftpboot
- sudo /etc/init.d/xinetd stop
- sudo /etc/init.d/xinetd start

- Configure /etc/network/interfaces
```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.77.55
    netmask 255.255.255.0
    network 192.168.77.0
    broadcast 192.168.77.255
    gateway 192.168.77.250
```

- ssendhil@ubuntu:~$ ls /tftpboot/
jinstall-host-qfx-5-15.1R6.7-domestic-signed.tgz  network.conf

